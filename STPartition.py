import numpy as np
from ctTests import *
from miscs import *
from TDA import *

def STPartition(tasks, fit = 'first'):
    if len(tasks) == 0:
        return -1
    RMTasks = RMsort(tasks, 'period')
    #print RMTasks
    pi = [] #index is j in the paper
    feasible = []
    r = 1 #at least required one resource

    tmplist = []
    for i in range(len(RMTasks)):
        tmplist.append(0)
    #now tmplist has n of 0 in the list
    for i in range(len(RMTasks)):
        feasible.append(tmplist)
    #now there is a nxn array
    feasible[0][0] = 1

    tmplist = []
    tmplist.append(RMTasks.pop(0))
    pi.append(tmplist)
    c = 0
    for kid, taskk in enumerate(RMTasks):
        print kid+1
        hpTasks = RMTasks[:c]
        for j in range(r): #resource j
            #print pi
            #if k2qJitterBound(taskk, pi[j]):#schedulability test
            if TDAjit(taskk, pi[j]):#schedulability test
                feasible[kid+1][j] = 1
        print feasible[kid+1]
        feasibleNum = sum( feasible[kid+1] )
        #print feasibleNum
        if feasibleNum != 0:
            #first fit
            for ind, j in enumerate(feasible[kid+1]):
                #print j
                if j != 0:
                    pi[ind].append(taskk)
            #Last fit
            #for j in range(feasibleNum):

            #Worst fit
        else:
            r += 1
            tmplist = []
            tmplist.append(taskk)
            pi.append(tmplist)
        c+=1
    print 'res:'+str(r)
    for i in feasible:
        print i
'''
STPartition(
[{"shared-R": 2.0443475322945925, "deadline": 6.861600432579902, "period": 6.861600432579902, "exclusive-R": 2.7261659519166805}, {"shared-R": 24.25520218000318, "deadline": 55.772549357391995, "period": 55.772549357391995, "exclusive-R": 10.222532713918365}, {"shared-R": 0.7164016222203693, "deadline": 9.682821897301267, "period": 9.682821897301267, "exclusive-R": 4.928094836233472}, {"shared-R": 29.414679114852536, "deadline": 81.53182820417044, "period": 81.53182820417044, "exclusive-R": 29.063469993703407}, {"shared-R": 0.7500844156024209, "deadline": 8.99136453403796, "period": 8.99136453403796, "exclusive-R": 3.0331140091879027}, {"shared-R": 0.0899800750889231, "deadline": 18.62049692441711, "period": 18.62049692441711, "exclusive-R": 9.883332445405344}, {"shared-R": 0.17866975406815405, "deadline": 7.359352887914846, "period": 7.359352887914846, "exclusive-R": 2.171644146361121}, {"shared-R": 1.9452210160355607, "deadline": 62.954263698392154, "period": 62.954263698392154, "exclusive-R": 30.837333983880704}, {"shared-R": 0.6028648395758406, "deadline": 5.023935538769254, "period": 5.023935538769254, "exclusive-R": 2.187035936626036}, {"shared-R": 2.415324679725312, "deadline": 35.01894926157891, "period": 35.01894926157891, "exclusive-R": 17.31061300852794}])
'''
