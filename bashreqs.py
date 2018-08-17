import bashlex
import itertools
import json
import subprocess
import sys
import re
import os

commands = set()

with open(sys.argv[1]) as f:
    newCommand = f.readlines()

def parseLine(aLine):
    parts = bashlex.parse(aLine)

    output = parts[0].dump()
    output = output.split("\n")

    commandNodePrev = False
    for line in output:
            if "WordNode" in line and commandNodePrev:
                    commands.add(line.split("word='")[1][:-3])
            if "CommandNode" in line:
                    commandNodePrev = True
            else:
                    commandNodePrev = False

# find packages which were installed from .deb file, or cannot be installed anymore
obsoletePackagesReport = []

obsoletePackages = subprocess.run(['aptitude', 'search', '?obsolete'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
obsoletePackages = obsoletePackages.stdout.decode('utf-8').strip()
for obsoletePackage in obsoletePackages.split("\n"):
	# https://askubuntu.com/questions/98223/how-do-i-get-a-list-of-obsolete-packages
	obsoletePackage = obsoletePackage.strip()
	if (len(obsoletePackage) != 0):
		if (obsoletePackage[0] == "i"): # "meaning that the package is installed"
			obsoletePackagesReport.append(obsoletePackage[3:].strip().split(" ")[0])

def getAptPackageVersion(package):
	result = subprocess.run(['apt-cache', 'policy', package], stdout=subprocess.PIPE)
	result = result.stdout.decode('utf-8')
	if (len(result.strip()) == 0):
		return "null"
	else:
		result = result.split("\n")
		return result[1].split("Installed: ")[1]

for line in newCommand:
    # parser cannot handle comments with single quotes in them, so just
    # nuke all comments
	if (len(line) > 0 and line[0] != "#"):
		try:
        		parseLine(line.strip())
		except:
			pass # ignore exceptions because lines may contain errors; still in beta stage
			     # and bashlex may get confused with some lines
installedViaApt = {}
installedOther = []

# checks if a string only contains A-Z, a-z, 0-9, periods and underscores
# (allowed characters for 99.99% of terminal commands.)
# this reduces false positives when extracting commands
def special_match(strg, search=re.compile(r'[^a-zA-Z0-9._]').search):
	return not bool(search(strg))
		
def checkIfPackageIsObsolete(package):
	if (package in obsoletePackagesReport):
			print("# warning: " + package + " is obsolete and cannot be installed.")
			
# adds the package and path to the installedViaApt variable, which will print
# a report at the end
def addToInstalledApt(command, version, path):
	checkIfPackageIsObsolete(command)
	command = command + "==" + version
	if (command in installedViaApt):
		installedViaApt[command].append(path)
	else:
		if (len(path.strip()) == 0):
			installedViaApt[command] = []
		else:
			installedViaApt[command] = [path]

def checkForExecCalls(pathToExec):
	if (len(pathToExec.strip()) == 0):
		return []

	foundCalls = []
	execCalls = ["execl", "execle", "execlp", "execv", "execve", "execvp", "vfork"]

	# find all system calls in executable with nm. Hide all errors due to permissions,
	# or if the file is not an executable (e.g. a script)
	result = subprocess.run(['nm', '-Dp', pathToExec], stdout=subprocess.PIPE, stderr=open('os.devnull', 'w')).stdout.decode('utf-8')
	for syscall in result.split("\n"):
		for execCall in execCalls:
			if ("U " + execCall) in syscall:
				foundCalls.append(execCall)
	return foundCalls

def printFoundExecCalls(pathToExec):
	# check executables for calls to exec, which means that they could call another
	# program, meaning that bashreq may not have found another requirement
	possibleExecCalls = checkForExecCalls(whereIsItInstalled)
	if len(possibleExecCalls) != 0:
		print("# warning: " + pathToExec + " calls " + ", ".join(possibleExecCalls) + " which could cause missing req")

			
for command in commands:
	# if it's unlikely to be a command, skip it
	if not special_match(command):
		continue

	# try to see if the package name is the same as the executable
	result = subprocess.run(['apt-cache', 'policy', command], stdout=subprocess.PIPE)
	finalResult = result.stdout.decode('utf-8')

	# try to find path to executable (try)
	whereIsItInstalled = subprocess.run(['which', command], stdout=subprocess.PIPE)
	whereIsItInstalled = whereIsItInstalled.stdout.decode('utf-8').strip()

	if (len(finalResult.strip()) == 0) or ("Installed: (none)" in finalResult):
		# package does not exist in apt, or not installed via apt-get
		# might be installed in another package (e.g. coreutils) which provides
		# other executables under a different package name

		# try to find apt-get package for executable
		# https://stackoverflow.com/questions/31683320/
		dpkgResults = subprocess.run(['dpkg', '-S', command], stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))
		dpkgResults = dpkgResults.stdout.decode('utf-8')

		# if there are no dpkg results, then just list where the executable is
		if (len(dpkgResults.strip()) == 0):
			printFoundExecCalls(whereIsItInstalled)
			installedOther.append(whereIsItInstalled)
		else:
			# otherwise, try to find the package it came from
			dpkgResultsLines = dpkgResults.split("\n")
			for aPath in dpkgResultsLines:
				if (len(whereIsItInstalled) != 0) and (whereIsItInstalled == aPath.split(": ")[1]):
					# found the executable's path associated with package name
					# grab the package name and add it to packages
					package = aPath.split(":")[0]

					# check executables for calls to exec, which means that they could call another
					# program, meaning that bashreq may not have found another requirement
					addToInstalledApt(package, getAptPackageVersion(package), whereIsItInstalled)
					break
	else:
		# the executable's name is same as apt package; just add to requirements
		finalResult = finalResult.split("\n")
		package = finalResult[0]
		packageVersion = finalResult[1].split("Installed: ")[1]
		addToInstalledApt(package[:-1], packageVersion, "")

	printFoundExecCalls(whereIsItInstalled)

# print reports
for package, paths in sorted(installedViaApt.items()):
	if len(paths) != 0:
		print(package + " # because of " + ", ".join(paths))
	else:
		print(package)

if len("".join(installedOther).strip()) != 0:
	print("# Installed via other methods:")
	for other in installedOther:
		if (len(other.strip()) != 0):
			print("# " + other.strip())

