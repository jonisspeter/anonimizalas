#!/usr/bin/env python3
# -*- coding: Utf-8 -*-
# generatedata.py -w workdir -d datadir

import argparse
import shlex
import csv
import sys
import xml.etree.ElementTree as ET
import random
import os
import time
import msvcrt

parser = argparse.ArgumentParser(description='Example for arguments.')
parser.add_argument('-w','--WOKRDIR', help='A munkakönyvtár ahova az ideiglenes fájlokat rakja.', type=str, required=False, default='workdir')
parser.add_argument('-d','--DATADIR', help='Az adatkönyvtár ahova az kész fájlokat rakja.', type=str, required=False, default='datadir')


TIMEOUT = 60

args = parser.parse_args()

workdir = args.WOKRDIR
datadir = args.DATADIR


scriptDir = ''
scriptDir = os.path.dirname(os.path.abspath(__file__))

# könyvtár létrehozása ha kell
workDir = os.path.join(scriptDir, workdir)
try:
    os.makedirs(workDir)
except OSError:
    pass # already exists


	# könyvtár létrehozása ha kell
dataDir = os.path.join(scriptDir, datadir)
try:
    os.makedirs(dataDir)
except OSError:
    pass # already exists
	

nationality = ['American','Russian','French','Indian','Japanese']
diseases = ['Heart','Viral','Cancer']
linenum = 0



def GenerateRow( ):
	'''1 sornyi tesztadatot generál véletlenszerűen'''
	line = []
	id = []
	tmp = 0
	tmpstr = ''
	line.append('Test Citizen' + str(random.randint(0,100000)))
	id.append(str(random.randint(1,999)).rjust(3,'0'))
	id.append(str(random.randint(1,99)).rjust(2,'0'))
	id.append(str(random.randint(1,9999)).rjust(4,'0'))
	line.append('-'.join(id))
	line.append('1' + str(random.randint(1000,9999)))
	line.append(str(random.randint(1,99)))
	
	line.append(nationality[random.randint(0,len(nationality) - 1)])
	line.append(diseases[random.randint(0,len(diseases) - 1)])
	return ';'.join(line)




while True:
	file_name = 'workfile' + str(int(time.time())) + '.txt'
	dataPath = os.path.join(dataDir, file_name)
	workPath = os.path.join(workDir, file_name)
	f = open(workPath, 'w')
	while linenum < 1000 :
		fileline = GenerateRow()
		f.write( fileline + '\n')
		linenum = linenum + 1
			
	f.close()
	os.rename(workPath, dataPath)	
	# várunk 1 percet az új fájl létrehozásig vagy gombnyomásra kilépünk
	i = 0
	print('file done')
	while i < 100 and not msvcrt.kbhit():
		time.sleep(0.1)	
		i = i + 1
	if i < 	100 :
		break 
		
