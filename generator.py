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

def UUniFast_Discard(n,U_avg, sstype):
    while 1:
        sumU=U_avg
        for i in range(n-1):
            nextSumU=sumU*math.pow(random.random(), 1/(n-i))
            USet.append(sumU-nextSumU)
            sumU=nextSumU
        USet.append(sumU)

        if sstype == 'S':
            if max(USet) < 1:
                break
        elif sstype == 'M':
            if max(USet) < 0.9:
                break
        elif sstyep == 'L':
            if max(USet) < 0.7:
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

            PSet.append(task(i*p, p, p, suspension))
            res.append((i*p+suspension)/p)
	    j=j+1;
        return res

def init():
	global USet,PSet
	USet=[]
	PSet=[]

def taskGeneration(numTasks, uTotal, sstype):
    random.seed()
    while 1:
        init()
        UUniFast_Discard(numTasks,uTotal/100, sstype)
        res = CSet_generate_sss(1,2,sstype)
        if max(res) <1:
            #print numTasks, uTotal
            break
    fo = open(ofile, "wb")
    print >>fo, json.dumps(PSet)
    return PSet
'''
def generate_taskset(util_max = 1.0, runnable_min = 600, runnable_max = 800, max_trials = 1, period_pdf = [0.18, 0.02, 0.02, 0.25, 0.25, 0.03, 0.2, 0.01, 0.04]):
    trials = 0
    while True:
        trials += 1
        taskset = []
        dist = stats.rv_discrete(name='periods', values = ([1,2,5,10,20,50,100,200,1000], period_pdf))
        runnables = int(np.random.uniform(runnable_min, runnable_max))

        sys_runnable_periods = dist.rvs(size=runnables)

        sys_runnables_period_0001_amount = 0
        sys_runnables_period_0002_amount = 0
        sys_runnables_period_0005_amount = 0
        sys_runnables_period_0010_amount = 0
        sys_runnables_period_0020_amount = 0
        sys_runnables_period_0050_amount = 0
        sys_runnables_period_0100_amount = 0
        sys_runnables_period_0200_amount = 0
        sys_runnables_period_1000_amount = 0

        for period in sys_runnable_periods:
            if period == 1:
                sys_runnables_period_0001_amount += 1
            if period == 2:
                sys_runnables_period_0002_amount += 1
            if period == 5:
                sys_runnables_period_0005_amount += 1
            if period == 10:
                sys_runnables_period_0010_amount += 1
            if period == 20:
                sys_runnables_period_0020_amount += 1
            if period == 50:
                sys_runnables_period_0050_amount += 1
            if period == 100:
                sys_runnables_period_0100_amount += 1
            if period == 200:
                sys_runnables_period_0200_amount += 1
            if period == 1000:
                sys_runnables_period_1000_amount += 1

        # build tasks from runnables (PERIOD = 1)
        amounts = runnables_per_tasks(sys_runnables_period_0001_amount)
        for amount in amounts:
            # C_i = sum of acet(runnable), runnable assigned to task i

            taskset.append(task(sum(sample_runnable_acet(1, amount)), 1, 1))

        # build tasks from runnables (PERIOD = 2)
        amounts = runnables_per_tasks(sys_runnables_period_0002_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(2, amount)), 2, 2))

            # build tasks from runnables (PERIOD = 5)
        amounts = runnables_per_tasks(sys_runnables_period_0005_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(5, amount)), 5, 5))

            # build tasks from runnables (PERIOD = 10)
        amounts = runnables_per_tasks(sys_runnables_period_0010_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(10, amount)), 10, 10))

            # build tasks from runnables (PERIOD = 20)
        amounts = runnables_per_tasks(sys_runnables_period_0020_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(20, amount)), 20, 20))

            # build tasks from runnables (PERIOD = 50)
        amounts = runnables_per_tasks(sys_runnables_period_0050_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(50, amount)), 50, 50))

            # build tasks from runnables (PERIOD = 100)
        amounts = runnables_per_tasks(sys_runnables_period_0100_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(100, amount)), 100, 100))

            # build tasks from runnables (PERIOD = 200)
        amounts = runnables_per_tasks(sys_runnables_period_0200_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(200, amount)), 200, 200))

            # build tasks from runnables (PERIOD = 1000)
        amounts = runnables_per_tasks(sys_runnables_period_1000_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(1000, amount)), 1000, 1000))

        if is_valid(taskset, util_max):
            return taskset
        else:
            if trials >= max_trials:
                raise ValueError("amount of runnables is inappropriate for given max utilization")
            continue
            return taskset

def is_valid(taskset, util_max):
    util = 0.0
    for task in taskset:
        util += task['shared-R']/task['period']+task['exclusive-R']/task['period']
    if util > util_max:
        return False
    return True
'''
