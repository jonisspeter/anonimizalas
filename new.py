#!/usr/bin/env python3
# -*- coding: Utf-8 -*-
# new.py -i tesztdata.txt -x treedata.xml -s recordstruct.txt

import argparse
import shlex
import csv
import sys
import xml.etree.ElementTree as ET
import os
import time
import msvcrt

parser = argparse.ArgumentParser(description='Example for arguments.')
#parser.add_argument('-n','--NAME', help='A keresztnev, amit a cimtarban keresni kell .', type=str, required=True)
parser.add_argument('-i','--INFILE', help='A bemeneti fajl eleresi utja.', type=str, required=False, default='tesztdata.txt')
parser.add_argument('-x','--XMLFILE', help='Az xml bemeneti fajl eleresi utja.', type=str, required=False, default = 'treedata.xml')
parser.add_argument('-s','--STRUCTFILE', help='A rekordstruktúra bemeneti fajl eleresi utja.', type=str, required=False, default = 'recordstruct.txt')
parser.add_argument('-w','--WOKRDIR', help='A munkakönyvtár ahova az ideiglenes fájlokat rakja.', type=str, required=False, default='worktempdir')
parser.add_argument('-d','--DATADIR', help='Az temp könyvtár ahova az készfájlokat rakja.', type=str, required=False, default='datadir')
parser.add_argument('-c','--CONFIGDIR', help='A config könyvtár ahol az beállító fájlok vannak.', type=str, required=False, default='configDir')
parser.add_argument('-o','--OUTDIR', help='A kimeneti könyvtár ahova az anonim fájlok kerülnek.', type=str, required=False, default='outdir')



args = parser.parse_args()

#inicializálás
structList = {}
inputList = []
anonymList = []
wasAlgorithm = False

kAnonym = 2

scriptDir = ''
scriptDir = os.path.dirname(os.path.abspath(__file__))
anonimData = {} # a kulcsok a sorok, azokból hány azonos van

# könyvtár létrehozása ha kell
outDir = os.path.join(scriptDir, args.OUTDIR)
try:
    os.makedirs(outDir)
except OSError:
    pass # already exists

# könyvtár létrehozása ha kell
workDir = os.path.join(scriptDir, args.WOKRDIR)
try:
    os.makedirs(workDir)
except OSError:
    pass # already exists


# könyvtár létrehozása ha kell
dataDir = os.path.join(scriptDir, args.DATADIR)
try:
    os.makedirs(dataDir)
except OSError:
    pass # already exists

configDir = os.path.join(scriptDir, args.CONFIGDIR)

# a fa feldolgozása a nemzetiségek általánosításához
path = os.path.join(configDir, args.XMLFILE)
tree = ET.parse(path)
root = tree.getroot()
	
# adatstruktúra beolvasása listákba
if args.STRUCTFILE is not None :
	
	try:
		path = os.path.join(configDir, args.STRUCTFILE)
		#print(path)
		structfile = open(path, "r")
		for line in structfile : 
			items = line.split(",")
			#print(items)
			for i in range(len(items)) :
				#print(items[i])
				structList[i + 1] = items[i]
		#print(inputList)
	except IOError as e:
		errno, strerror = e.args
		print("ERROR: be/kimeneti hiba({0}): {1}".format(errno,strerror))
		sys.exit(0)
	except:
		print("ERROR: egyéb hiba:", sys.exc_info()[0])
		sys.exit(0)
		#print('structList')
		#print(structList[1])
structfile.close()


# a csoportok beolvasása  anonimData
try:
	path = os.path.join(configDir, 'anonimData.txt')
	#print(path)
	anonimsetfile = open(path, "r")
	for line in anonimsetfile : 
		items = line.strip().split(",")
		#print(items)
		anonimData[items[0]] = int(items[1])
except :
	pass
			
#print(anonimData)
algorithm = []

try:
	algPath = os.path.join(configDir, 'algorithm.txt')
	f = open(algPath, 'r')
	for line in f :
		tmp = line.strip().split(',')
		algorithm.append([int(tmp[0]), int(tmp[1])])
	f.close()
	wasAlgorithm = True
except FileNotFoundError as e:
	algorithm = [[i,0] for i in range(len(structList) + 1)] # az eddigi anonimizáló algoritmus [[oszlop, iteráció]]	
	pass

#print(wasAlgorithm)

def GetParent( node, child):
	if node.find(child) != None :
		return node
	else:
		for f in node :
			found = GetParent( f, child)
			if found != None :
				return found
			
		

def SuppressData( dataList ):    # write Fibonacci series up to n
	"""Print a Fibonacci series up to n."""
	toHash = ""
	supprData = []
	retData = []
	for data in dataList :
		toHash = toHash + data
		#supprData.append(data)
		supprData.append('*')
	#print(toHash)
	retData.append(hash(toHash))
	retData = retData + supprData
	return retData
	

def GeneralizeDataByTruncating( data , n ):    # write Fibonacci series up to n
	retData = data[:len(data)-n] + "*"*n
	return retData


def GeneralizeDataByCategorizingInt( data = 0, n = 1, max = 100 ):    # write Fibonacci series up to n
	dataInt = 0
	if '..' in data :
		items = data.split("<")
		#print('////////////////items')
		#print(items)
		dataInt = (int(items[0]) + int(items[2]) ) / 2
		#print(dataInt)
	elif '<' in data:
		return data
	else :
		dataInt = int(data)
	if int(max) < dataInt :
		return max + "< "
	#print(2**(n-1))
	step = 2**(n-1) * 10
	curStep = 0
	prevStep = curStep
	while curStep < dataInt :
		prevStep = curStep
		curStep = curStep + step
	retData = '{}<..<{}'.format(prevStep,curStep)
	return retData


def GeneralizeDataByCategorizingTree( data, n ):    # write Fibonacci series up to n
	i = 0
	#print('node')
	while i < n :
		node = GetParent(root,data)
		data = node.tag
		#print(data)
		i = i + 1
	
	#print(data)
	return data
	

# statisztika a megfelelő csoportok létrehozására, k anonimitás ellenőrzésére
def Statistics( dataListStat ):    # write Fibonacci series up to n
	result = []
	#print(len(dataListStat))
	statData = [set() for i in range(len(dataListStat[0]))] # melyik oszlopban mennyi különböző érték van
	line = str
	anonimDataTemp = {}
	for k in anonimData :
		anonimDataTemp[k] = anonimData[k]
	
	for dataLine in dataListStat :
		line = ''.join(dataLine[3:len(dataLine) - 1])
		if not( line in anonimDataTemp) :
			anonimDataTemp[line] = 1
		else :
			anonimDataTemp[line] = anonimDataTemp[line] + 1
		for i in range(len(dataLine)) :
			statData[i].add(dataLine[i])
			
			
			
			#if not(dataLine[i] in statData[i]) :
			#	statData[i] = statData[i].add(dataLine[i])
	anonymity = 0
	for k,v in anonimDataTemp.items() :
		if v < anonymity or anonymity == 0 :
			anonymity = v
	#print(statData)
	#print('#####################################')
	#for i in range(len(statData)) :
	#	print(len(statData[i]))
	#print('#####################################')
	#print(anonimData)
	result.append(anonymity)
	result.append(statData)
	result.append(anonimDataTemp)

	return result 
	
def CreateAnonymWOAlg ( dataSet ) :
	curAnonymity = 0 # jelenlegi anonimitás szintje
	maxItems = 0 # a legnagyobb elemszámú csoport, amit anonimizálni kell
	statResult = [] # statisztika gyűjtés végeredménye
	anonymDataSet = dataSet # anonimizált adathalmaz
	statResult = Statistics( anonymDataSet )
	curAnonymity = statResult[0]  
	anonymCol = 0 # anonimizálandó oszlop
	#print('kAnonym')
	#print(kAnonym)
	
	#print('algorithm')
	#print(algorithm)
	while curAnonymity < kAnonym :
		maxItems = 0
		#print('----------------------statresult')
		#print(statResult)
		for i in range(3,len(statResult[1]) - 1):  # itt majd a beégetett cuccok helyett lehetne változót csinálni
			#print(len(statResult[1][i]))
			#print(statResult[1][i])
			if maxItems == 0 or len(statResult[1][i]) > maxItems :
				maxItems = len(statResult[1][i])
				anonymCol = i 
		#print('anonymCol')
		#print(anonymCol)
		#print(structList[anonymCol])
		algorithm[anonymCol][1] = algorithm[anonymCol][1] + 1
		for i in range(len(anonymDataSet)) :
			if structList[anonymCol] == 'intcat' :
				#print('intcat')
				#print(anonymDataSet[i][anonymCol])
				anonymDataSet[i][anonymCol] = GeneralizeDataByCategorizingInt(anonymDataSet[i][anonymCol],algorithm[anonymCol][1],100)
				#print(anonymDataSet[i][anonymCol])
			elif  structList[anonymCol] == 'treecat' :
				#print('treecat')
				#print(anonymDataSet[i][anonymCol])
				#print(algorithm[anonymCol][1])
				anonymDataSet[i][anonymCol] = GeneralizeDataByCategorizingTree(anonymDataSet[i][anonymCol],1)
				#print(anonymDataSet[i][anonymCol])
			elif  structList[anonymCol] == 'inttr' :
				#print('inttr')
				#print(anonymDataSet[i][anonymCol])
				anonymDataSet[i][anonymCol] = GeneralizeDataByTruncating(anonymDataSet[i][anonymCol],algorithm[anonymCol][1])
				#print(anonymDataSet[i][anonymCol])
			
		#
		# run anonimizálás
		#for line in statResult[1] :
		#	anonym.write(str(len(line)) + ',  ' + ', '.join(map(str, line)) + '\n')
			
		#for line in anonymDataSet :
		#	anonym.write(', '.join(map(str, line)) + '\n')
			
		statResult = Statistics( anonymDataSet )
		#print(statResult)
		#print(anonimData)
		curAnonymity = statResult[0]
		#print('?????????????????????????')
		#print(curAnonymity)
		time.sleep(1)
		#print(anonymDataSet)
		#print('--------------------------')
		#print(algorithm)
		#print(statResult[2])
		#curAnonymity = kAnonym
	#print('VEGE')	
	#print(anonymDataSet)
	for k in statResult[2]:
		anonimData[k] = statResult[2][k]
	#print(anonimData)
	return anonymDataSet

# A már meglévő algoritmus használata
def CreateAnonymWAlg ( dataSet ) :

	anonymDataSet = dataSet # anonimizált adathalmaz
	anonymCol = 0 # anonimizálandó oszlop
	#print('kAnonym')
	#print(kAnonym)
	
	#print('algorithm')
	#print(algorithm)
	statResult = [] # statisztika gyűjtés végeredménye
	for j in range(1,len(algorithm)) :
		for i in range(len(anonymDataSet)) :
			if structList[j] == 'intcat' :
				#print('intcat')
				#print(anonymDataSet[i][anonymCol])
				anonymDataSet[i][j] = GeneralizeDataByCategorizingInt(anonymDataSet[i][j],algorithm[j][1],100)
				#print(anonymDataSet[i][anonymCol])
			elif  structList[j] == 'treecat' :
				#print('treecat')
				#print(anonymDataSet[i][anonymCol])
				#print(algorithm[anonymCol][1])
				anonymDataSet[i][j] = GeneralizeDataByCategorizingTree(anonymDataSet[i][j],algorithm[j][1])
				#print(anonymDataSet[i][anonymCol])
			elif  structList[j] == 'inttr' :
				#print('inttr')
				#print(anonymDataSet[i][anonymCol])
				anonymDataSet[i][j] = GeneralizeDataByTruncating(anonymDataSet[i][j],algorithm[j][1])
				#print(anonymDataSet[i][anonymCol])
			
		#
		# run anonimizálás
		#for line in statResult[1] :
		#	anonym.write(str(len(line)) + ',  ' + ', '.join(map(str, line)) + '\n')
			
		#for line in anonymDataSet :
		#	anonym.write(', '.join(map(str, line)) + '\n')
			
		
		#print('?????????????????????????')
		#print(curAnonymity)
		#print(anonymDataSet)
		#print(algorithm)
		#curAnonymity = kAnonym
	#print('VEGE')	
	#print(anonymDataSet)
	statResult = Statistics( anonymDataSet )
	for k in statResult[2]:
		anonimData[k] = statResult[2][k]
	return anonymDataSet
	
# főprogi

def SaveAnonimData( ):    # 
	path = os.path.join(configDir, 'anonimData.txt')
	f = open(path, 'w')
	#print(anonimData)
	for k, v in anonimData.items():
	    f.write(str(k) +',' + str(v) + '\n')
	f.close()
	


# adatok beolvasása listákba
paths = [os.path.join(dataDir,fn) for fn in next(os.walk(dataDir))[2]]
fileNum = 0
for file in paths : 
	inputList = []
	try:
		infile = open(file, "r")
		for line in infile : 
			inputList.append(line.split(";"))

		#print(inputList)
	except IOError as e:
		errno, strerror = e.args
		print("ERROR: be/kimeneti hiba({0}): {1}".format(errno,strerror))
		sys.exit(0)
	except:
		print("ERROR: egyéb hiba:", sys.exc_info()[0])
		sys.exit(0)
	infile.close()

	# mindenek előtt elrejtjük az azonosítókat
	anonymList = []
	for data in inputList :
		anonymLine = SuppressData( [ data[0], data[1]])
		anonymLine.extend(data[2:])
	#anonymLine.append(GeneralizeDataByTruncating(data[2],2))
	#anonymLine.append(GeneralizeDataByCategorizingInt(int(data[3]),3,100))
	#GeneralizeDataByCategorizingTree( data[4],3)
	#print('anonymline ############################')
	#print(anonymLine)
		anonymList.append(anonymLine)
	#,data[3],data[4],data[5],data[6]]
#print('anonymlist ############################')
#print(anonymList)
	if wasAlgorithm :
		anonymList = CreateAnonymWAlg(anonymList)
		#pass
	else :
		anonymList = CreateAnonymWOAlg(anonymList)	
		
	#print('anonymList')
	#print(anonymList)
	#print('wasAlgorithm:' + str(wasAlgorithm))
	#print(algorithm)
	if wasAlgorithm == False :
		algPath = os.path.join(configDir, 'algorithm.txt')
		f = open(algPath, 'w')
		tmp = []
		for line in algorithm :
			tmp.append('{0},{1}\n'.format(line[0], line[1]))
			#print(tmp)
		f.writelines(tmp)
		f.close()
		wasAlgorithm = True

	
	file_name = 'outfile' + str(time.time()).replace('.','') + '.txt'
	outpath = os.path.join(outDir, file_name)
	anonym = open(outpath, 'w')
	time.sleep(1)	
	#print('------------------' + outpath)
	#print(outpath)
	#print(anonymList)
	for line in anonymList :
		#print(', '.join(map(str, line)))
		anonym.write(', '.join(map(str, line)))
	anonym.close()
	fileNum = fileNum + 1
	SaveAnonimData()
	if fileNum == len(paths) :
		break
	#os.remove(file, *, dir_fd=None)   COCC 3
 

#	 x for x in lst if
#	 
