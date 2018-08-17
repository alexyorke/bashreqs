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

# adds the package and path to the installedViaApt variable, which will print
# a report at the end
def addToInstalledApt(command, path):
	if (command in installedViaApt):
		installedViaApt[command].append(path)
	else:
		if (len(path.strip()) == 0):
			installedViaApt[command] = []
		else:
			installedViaApt[command] = [path]

for command in commands:
	# if it's unlikely to be a command, skip it
	if not special_match(command):
		continue

	# try to see if the package name is the same as the executable
	result = subprocess.run(['apt-cache', 'policy', command], stdout=subprocess.PIPE)
	finalResult = result.stdout.decode('utf-8')
	if (len(finalResult.strip()) == 0) or ("Installed: (none)" in finalResult):
		# package does not exist in apt, or not installed via apt-get
		# might be installed in another package (e.g. coreutils) which provides
		# other executables under a different package name

		# try to find apt-get package for executable
		# https://stackoverflow.com/questions/31683320/
		dpkgResults = subprocess.run(['dpkg', '-S', command], stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'))
		dpkgResults = dpkgResults.stdout.decode('utf-8')

		# try to find path to executable
		whereIsItInstalled = subprocess.run(['which', command], stdout=subprocess.PIPE)
		whereIsItInstalled = whereIsItInstalled.stdout.decode('utf-8').strip()

		# if there are no dpkg results, then just list where the executable is
		if (len(dpkgResults.strip()) == 0):
			installedOther.append(whereIsItInstalled)
		else:
			# otherwise, try to find the package it came from
			dpkgResultsLines = dpkgResults.split("\n")
			for aPath in dpkgResultsLines:
				if (len(whereIsItInstalled) != 0) and (whereIsItInstalled == aPath.split(": ")[1]):
					# found the executable's path associated with package name
					# grab the package name and add it to packages
					package = aPath.split(":")[0]
					addToInstalledApt(package + "==" + getAptPackageVersion(package), whereIsItInstalled)
					break
	else:
		# the executable's name is same as apt package; just add to requirements
		finalResult = finalResult.split("\n")
		package = finalResult[0]
		packageVersion = finalResult[1].split("Installed: ")[1]
		addToInstalledApt(package[:-1] + "==" + packageVersion, "")



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
