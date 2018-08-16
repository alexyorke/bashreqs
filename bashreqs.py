import bashlex
import itertools
import json
import subprocess
import sys

commands = set()

with open(sys.argv[1]) as f:
    newCommand = f.readlines()

def parseLine(aLine):
    parts = bashlex.parse(aLine)

    output = parts[0].dump()
    output = output.split("\n")

    commandNodePrev = False
    for line in output:
	    # ugly hack: print the nodes and then parse them via string interpretation
            if "WordNode" in line and commandNodePrev:
                    commands.add(line.split("word='")[1][:-3])
            if "CommandNode" in line:
                    commandNodePrev = True
            else:
                    commandNodePrev = False

for line in newCommand:
    # parser cannot handle comments with single quotes in them, so just
    # nuke all comments
	if (len(line) > 0 and line[0] != "#"):
		try:
        		parseLine(line.strip())
		except:
			pass # ignore exceptions because lines may contain errors; still in beta stage
			     # and bashlex may get confused with some lines
installedViaApt = []
installedOther = []
for command in commands:
	result = subprocess.run(['apt-cache', 'policy', command], stdout=subprocess.PIPE)
	finalResult = result.stdout.decode('utf-8')
	if (len(finalResult) == 0):
		# package not installed via apt-get
		whereIsItInstalled = subprocess.run(['which', command], stdout=subprocess.PIPE)
		installedOther.append(whereIsItInstalled.stdout.decode('utf-8'))
	else:
		installedViaApt.append(finalResult)

print("Installed via APT:")
for apt in installedViaApt:
	print(apt)

print("Installed via other methods:")
for other in installedOther:
	if (len(other.strip()) != 0):
		print(other.strip())
