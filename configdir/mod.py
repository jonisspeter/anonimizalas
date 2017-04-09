import os
import xml.etree.ElementTree as ET

# a fa feldolgozása a nemzetiségek általánosításához

scriptDir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(scriptDir, 'treedata.xml')
tree = ET.parse(path)
root = tree.getroot()


def Hash( data) :  
	return hash(data)

def SuppressData( data, hashData ):    
	
	toHash = ''
	toHash = str(hashData)
	supprData = []
	retData = []
	toHash = toHash + data
	supprData.append('*')
	retData.append(toHash)
	retData = retData + supprData
	return retData

def SuppressData2( data, n ):    
	return '*'
	
def GeneralizeDataByTruncating( data , n ):    
	retData = data[:len(data)-n] + "*"*n
	return retData


def GeneralizeDataByCategorizingInt( data = 0, n = 1, max = 100 ):    
	dataInt = 0
	if '..' in data :
		items = data.split("<=")
		dataInt = (int(items[0]) + int(items[2]) ) / 2
	elif '<' in data:
		return data
	else :
		dataInt = int(data)
	step = 2**(n-1) * 10
	
	if int(max) < dataInt or step > int(max):
		return str(max) + "< "
	
	curStep = 0
	prevStep = curStep
	while curStep <= dataInt :
		prevStep = curStep + 1
		curStep = curStep + step
	retData = '{}<=..<={}'.format(prevStep,curStep)
	return retData
	
def GetParent( node, child):
	if node.find(child) != None :
		return node
	else:
		for f in node :
			found = GetParent( f, child)
			if found != None :
				return found

def GeneralizeDataByCategorizingTree( data, n ):    
	i = 0
	while i < n :
		node = GetParent(root,data)
		
		data = node.tag
		i = i + 1
	
	return data