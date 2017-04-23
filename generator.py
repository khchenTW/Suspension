from __future__ import division
from scipy import stats
import numpy as np
import random
from scipy.stats import exponweib
import math
import analysis
import sys, getopt
import json

ofile = "taskset-p.txt"
USet=[]
class task (dict):
    def __init__(self, execution, period, deadline, suspension):
        dict.__setitem__(self, "execution", float (execution))
        dict.__setitem__(self, "period", float (period))
        dict.__setitem__(self, "deadline", float (deadline))
        dict.__setitem__(self, "suspension", float (suspension))

def UUniFast(n,U_avg):
    global USet
    sumU=U_avg
    for i in range(n-1):
        nextSumU=sumU*math.pow(random.random(), 1/(n-i))
        USet.append(sumU-nextSumU)
        sumU=nextSumU
    USet.append(sumU)

def UniDist(n,U_min,U_max):
	for i in range(n-1):
	    uBkt=random.uniform(U_min, U_max)
	    USet.append(uBkt)

def CSet_generate(Pmin,numLog, p, sstype=0):
	global USet,PSet
	j=0
        # the number of SSS
        x = len(USet) * p
	for i in USet:
	    thN=j%numLog
	    p=random.uniform(Pmin*math.pow(10, thN), Pmin*math.pow(10, thN+1))
            if x != 0:
                if sstype == 0: #S
                    suspension = random.uniform(0.01*(p-i*p), 0.1*(p-i*p))
                elif sstype == 1: #M
                    suspension = random.uniform(0.1*(p-i*p), 0.6*(p-i*p))
                else: #L
                    suspension = random.uniform(0.6*(p-i*p), (p-i*p))
                x-=1
            else:
                suspension = 0
            PSet.append(task(i*p, p, p, suspension))
	    j=j+1;

def init():
	global USet,PSet
	USet=[]
	PSet=[]

def taskGeneration(numTasks, uTotal, sstype, propotion):
    random.seed()
    init()
    UUniFast(numTasks,uTotal/100)
    CSet_generate(1,2, propotion, sstype)
    fo = open(ofile, "wb")
    print >>fo, json.dumps(PSet)
    return PSet

