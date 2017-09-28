from __future__ import division
from scipy import stats
import numpy as np
import random
from scipy.stats import exponweib
import math
import sys, getopt
import json

ofile = "taskset-p.txt"
USet=[]
class task (dict):
    def __init__(self, sharedR, period, deadline, execlusiveR, resource, block):
        dict.__setitem__(self, "shared-R", float (sharedR))
        dict.__setitem__(self, "period", float (period))
        dict.__setitem__(self, "deadline", float (deadline))
        dict.__setitem__(self, "exclusive-R", float (execlusiveR))
        dict.__setitem__(self, "resource", int (resource))
        dict.__setitem__(self, "block", int (block))

def UUniFast(n,U_avg):
    global USet
    sumU=U_avg
    for i in range(n-1):
        nextSumU=sumU*math.pow(random.random(), 1/(n-i))
        USet.append(sumU-nextSumU)
        sumU=nextSumU
    USet.append(sumU)

def UUniFast_Discard(n,U_avg, sstype):
    while 1:
        sumU=U_avg
        for i in range(n-1):
            nextSumU=sumU*math.pow(random.random(), 1/(n-i))
            if sstype == 'S':
                if sumU-nextSumU < 1:
                    USet.append(sumU-nextSumU)
                else:
                    break
            elif sstype == 'M':
                if sumU-nextSumU < 0.9:
                    USet.append(sumU-nextSumU)
                else:
                    break
            elif sstype == 'L':
                if sumU-nextSumU < 0.7:
                    USet.append(sumU-nextSumU)
                else:
                    break
            sumU=nextSumU
        USet.append(sumU)

        if len(USet) == n:
            break
        del USet[:]

def UniDist(n,U_min,U_max):
	for i in range(n-1):
	    uBkt=random.uniform(U_min, U_max)
	    USet.append(uBkt)

def CSet_generate_sss_z(Pmin,numLog, sstype=0, btype=0):
	global USet,PSet
	j=0
        # the number of SSS
        res = []
	for i in USet:
	    thN=j%numLog
	    p=random.uniform(Pmin*math.pow(10, thN), Pmin*math.pow(10, thN+1))
            if sstype == 0: #S
                suspension = random.uniform(0.01*(p-i*p), 0.1*(p-i*p))
            elif sstype == 1: #M
                suspension = random.uniform(0.1*(p-i*p), 0.3*(p-i*p))
            else: #L
                suspension = random.uniform(0.3*(p-i*p), 0.45*(p-i*p))
            #generate the blocking time for \sigma*B
            if btype == 0:
                block = 0
            elif btype == 1: #S
                block = 0.2*Pmin*math.pow(10, thN)
            elif btype == 2: #M
                block = 0.5*Pmin*math.pow(10, thN)
            else: #L
                block = 0.75*Pmin*math.pow(10, thN)
            #generate the number of required resources
            requiredres = random.sample([1,2,4,6,8,10],1)
            PSet.append(task(i*p, p, p, suspension, requiredres[0], block))
            res.append((i*p+suspension)/p)
	    j=j+1;
        return res

def CSet_generate_sss(Pmin,numLog, sstype=0, btype=0):
	global USet,PSet
	j=0
        # the number of SSS
        res = []
	for i in USet:
	    thN=j%numLog
	    p=random.uniform(Pmin*math.pow(10, thN), Pmin*math.pow(10, thN+1))
            if sstype == 0: #S
                suspension = random.uniform(0.01*(p-i*p), 0.1*(p-i*p))
            elif sstype == 1: #M
                suspension = random.uniform(0.1*(p-i*p), 0.3*(p-i*p))
            else: #L
                suspension = random.uniform(0.3*(p-i*p), 0.45*(p-i*p))

            #generate the blocking time for \sigma*B
            if btype == 0:
                block = 0
            elif btype == 1: #S
                block = 0.2*Pmin*math.pow(10, thN)
            elif btype == 2: #M
                block = 0.5*Pmin*math.pow(10, thN)
            else: #L
                block = 0.75*Pmin*math.pow(10, thN)
            PSet.append(task(i*p, p, p, suspension, 0, block))
            res.append((i*p+suspension)/p)
	    j=j+1;
        return res

def init():
	global USet,PSet
	USet=[]
	PSet=[]

def taskGeneration(numTasks, uTotal, sstype, resource, btype):
    random.seed()
    while 1:
        init()
        UUniFast_Discard(numTasks,uTotal/100, sstype)
        if resource == 0:
            res = CSet_generate_sss(1,2,sstype, btype)
        else:
            res = CSet_generate_sss_z(1,2,sstype, btype)
        if max(res) <1:
            #print numTasks, uTotal
            break
    fo = open(ofile, "wb")
    print >>fo, json.dumps(PSet)
    return PSet

