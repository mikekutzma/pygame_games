import sys
import re

def read_rle(filename):
	with open(filename) as f:
		filetext = [x.lstrip().rstrip('\n') for x in f.readlines()]
	filetext = list(filter(lambda x: not x[0]=="#",filetext))
	mx = re.search("(?<=(x = ))\w+",filetext[0])
	my = re.search("(?<=(y = ))\w+",filetext[0])
	x,y = [int(a) for a in [mx.group(0),my.group(0)]]
	patternstring = "".join(filetext[1:])
	patternlines = patternstring.rstrip("!").split("$")
	grid = []
	for line in patternlines:
		grid.append(parseline(line,x))
	return grid

def parseline(line,l):
	row = []
	cellgroups = ["".join(x) for x in re.findall("(\d*b)|(\d*o)",line)]
	for cellgroup in cellgroups:
		row+=parsegroup(cellgroup)
	for i in range(l-len(row)):
		row.append(0)
	return row

def parsegroup(cellgroup):
	x = re.findall("\d+",cellgroup)
	if(len(x)==0):
		n=1
	else:
		n = int(x[0])
	ch = re.findall("\D",cellgroup)[0]
	if(ch=='b'):
		c=0
	else:
		c=1
	grouparr = []
	for i in range(n):
		grouparr.append(c)
	return grouparr
