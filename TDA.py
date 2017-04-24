import math
from gurobipy import *
from ctTests import *
from miscs import *
class task (dict):
    def __init__(self, sharedR, period, deadline, exclusiveR):
        dict.__setitem__(self, "shared-R", float (sharedR))
        dict.__setitem__(self, "period", float (period))
        dict.__setitem__(self, "deadline", float (deadline))
        dict.__setitem__(self, "exclusive-R", float (exclusiveR))

def Workload_Jitter(T,D,C,t):
    return max(0,C*math.ceil((t+(T-C))/T))

def TDAjit(task,HPTasks):
    C=task['shared-R']+task['exclusive-R']
    R=C
    D=task['deadline']

    while True:
        I=0
        for itask in HPTasks:
            I=I+Workload_Jitter(itask['period'],itask['deadline'],itask['shared-R'],R)
        if R>D:
            return R
        if R < I+C:
            R=I+C
        else:
            return R

def Workload_Blocking(T, C, t):
    return max(0,C*(math.ceil(t/T)))

def TDAblock(task,HPTasks):
    C=task['shared-R']
    B=task['exclusive-R']+quicksum(min(i['exclusive-R'], i['shared-R']) for i in HPTasks)
    R=C
    D=task['deadline']

    while True:
        I=0
        for itask in HPTasks:
            I=I+Workload_Blocking(itask['period'],itask['shared-R'],R)
        if R>D:
            return R
        if R < I+C+B:
            R=I+C+B
        else:
            return R

def Workload_Carry(T, C, t):
    return max(0,C*(math.ceil(t/T)+1))

def TDAcarry(task,HPTasks):
    C=task['shared-R']+task['exclusive-R']
    R=C
    D=task['deadline']

    while True:
        I=0
        for itask in HPTasks:
            I=I+Workload_Carry(itask['period'],itask['shared-R'],R)
        if R>D:
            return R
        if R < I+C:
            R=I+C
        else:
            return R
#check if returned value is larger than D
