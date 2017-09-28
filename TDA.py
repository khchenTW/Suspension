import math
from ctTests import *
from miscs import *

class task (dict):
    def __init__(self, sharedR, period, deadline, execlusiveR, resource, block):
        dict.__setitem__(self, "shared-R", float (sharedR))
        dict.__setitem__(self, "period", float (period))
        dict.__setitem__(self, "deadline", float (deadline))
        dict.__setitem__(self, "exclusive-R", float (execlusiveR))
        dict.__setitem__(self, "resource", int (resource))
        dict.__setitem__(self, "block", int (block))

def Workload_Contrained(T,C,t):
    return C*math.ceil((t)/T)

def TDA(task,HPTasks):
    C=task['shared-R']+task['exclusive-R']
    R=C
    D=task['deadline']

    while True:
        I=0
        for itask in HPTasks:
            I=I+Workload_Contrained(itask['period'],itask['shared-R']+itask['exclusive-R'],R)
        if R>D:
            return R
        if R < I+C:
            R=I+C
        else:
            return R

def Workload_Jitter(T,D,C,t):
    return max(0,C*math.ceil((t+(T-C))/T))

def TDAjit(task,HPTasks):
    C=task['shared-R']+task['exclusive-R']
    R=C
    D=task['deadline']
    B=task['block']

    while True:
        I=0
        for itask in HPTasks:
            I=I+Workload_Jitter(itask['period'],itask['deadline'],itask['shared-R'],R)
        if R>D:
            return R
        if R < I+C+B:
            R=I+C+B
        else:
            return R

def Workload_Blocking(T, C, t):
    return max(0,C*(math.ceil(t/T)))

def TDAblock(task,HPTasks):
    C=task['shared-R']
    B=task['exclusive-R']
    for i in HPTasks:
        B+=min(i['exclusive-R'], i['shared-R'])
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
    B=task['block']

    while True:
        I=0
        for itask in HPTasks:
            I=I+Workload_Carry(itask['period'],itask['shared-R'],R)+B
        if R>D:
            return R
        if R < I+C+B:
            R=I+C+B
        else:
            return R

def Workload_JitBlock(T, C, t, Q, y):
    # y is y_i and Q is calcualed beforehand
    return max(0,C*math.ceil((t+Q+(1-y)*(T-C))/T))

#def Workload_Jitter(T,D,C,t):
#    return max(0,C*math.ceil((t+(T-C))/T))

def TDAjitblock(task,HPTasks):
    vecY = [0 for i in range(len(HPTasks)+1)]
    C=task['shared-R']+task['exclusive-R']
    R=C
    D=task['deadline']
    #decide the vector vec(y)
    Q = 0.0
    yk = 0
    for itask, y in zip(HPTasks, vecY):
        if itask['exclusive-R'] <= itask['shared-R']:
            y = 1
        else:
            y = 0
        Q+=itask['exclusive-R']*y
    if task['exclusive-R'] < task['shared-R']:
        yk = 0
    while True:
        I=0
        for itask in HPTasks:
            I=I+Workload_JitBlock(itask['period'],itask['shared-R'],R, Q, yk)
        if R>D:
            return R
        if R < I+C:
            R=I+C
        else:
            return R


#check if returned value is larger than D
