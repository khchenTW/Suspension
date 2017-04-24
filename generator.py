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
    def __init__(self, sharedR, period, deadline, execlusiveR):
        dict.__setitem__(self, "shared-R", float (sharedR))
        dict.__setitem__(self, "period", float (period))
        dict.__setitem__(self, "deadline", float (deadline))
        dict.__setitem__(self, "exclusive-R", float (execlusiveR))

def UUniFast(n,U_avg):
    global USet
    sumU=U_avg
    for i in range(n-1):
        nextSumU=sumU*math.pow(random.random(), 1/(n-i))
        USet.append(sumU-nextSumU)
        sumU=nextSumU
    USet.append(sumU)

def UUniFast_Discard(n,U_avg):
    while 1:
        sumU=U_avg
        for i in range(n-1):
            nextSumU=sumU*math.pow(random.random(), 1/(n-i))
            USet.append(sumU-nextSumU)
            sumU=nextSumU
        USet.append(sumU)

        if max(USet) < 1:
            break
        del USet[:]

def UniDist(n,U_min,U_max):
	for i in range(n-1):
	    uBkt=random.uniform(U_min, U_max)
	    USet.append(uBkt)

def CSet_generate_sss(Pmin,numLog, sstype=0):
	global USet,PSet
	j=0
        # the number of SSS
	for i in USet:
	    thN=j%numLog
	    p=random.uniform(Pmin*math.pow(10, thN), Pmin*math.pow(10, thN+1))
            if sstype == 0: #S
                suspension = random.uniform(0.01*(p-i*p), 0.1*(p-i*p))
            elif sstype == 1: #M
                suspension = random.uniform(0.1*(p-i*p), 0.3*(p-i*p))
            else: #L
                suspension = random.uniform(0.3*(p-i*p), 0.6*(p-i*p))
            if (i*p+suspension)>p:
                return -1
            PSet.append(task(i*p, p, p, suspension))
	    j=j+1;
        return 0

def init():
	global USet,PSet
	USet=[]
	PSet=[]

def taskGeneration(numTasks, uTotal, sstype):
    random.seed()
    init()
    UUniFast(numTasks,uTotal/100)
    while 1:
        res = CSet_generate_sss(1,2,sstype)
        if res == 0:
            break
    fo = open(ofile, "wb")
    print >>fo, json.dumps(PSet)
    return PSet

