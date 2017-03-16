#!/usr/bin/env python3
# -*- coding: Utf-8 -*-
# new.py -i workfile.txt -x treedata.xml -s recordstruct.txt

import argparse
import shlex
import csv
import sys
import xml.etree.ElementTree as ET
import random
import os
import time

for i in range(10000) :
	tim = str(int(time.time())).split(',')[0]
	print(tim)