import numpy as np
from ctTests import *
from miscs import *
from TDA import *

def STPartition(tasks, opt, fit = 'first', btype='N'):
    if len(tasks) == 0:
        return -1
    RMTasks = RMsort(tasks, 'period')
    #print RMTasks
    r = 1 #at least required one resource

    tmplist = []
    for i in range(len(RMTasks)):
        tmplist.append(0)
    #now tmplist has n of 0 in the list
    feasible = []
    for i in range(len(RMTasks)):
        feasible.append(tmplist)
    #now there is a nxn array
    feasible[0][0] = 1

    pi = [] #index is j in the paper
    readPi = [] #show the assignment
    tmplist = []
    tmplist.append(RMTasks.pop(0))
    pi.append(tmplist)
    readPi.append([0])
    c = 0
    for kid, taskk in enumerate(RMTasks):
        for j in range(r): #resource j

            #TDA-based tests
            if opt == 'tda':
                if TDA(taskk, pi[j]) <= taskk['period']:
                    feasible[kid+1][j] = 1
                else:
                    feasible[kid+1][j] = 0
            elif opt == 'carry':
                if TDAcarry(taskk, pi[j]) <= taskk['period']:
                    feasible[kid+1][j] = 1
                else:
                    feasible[kid+1][j] = 0
            elif opt == 'block':
                if TDAblock(taskk, pi[j]) <= taskk['period']:
                    feasible[kid+1][j] = 1
                else:
                    feasible[kid+1][j] = 0
            elif opt == 'jit':
                if TDAjit(taskk, pi[j]) <= taskk['period']:
                    feasible[kid+1][j] = 1
                else:
                    feasible[kid+1][j] = 0
            elif opt == 'jitblock':
                if TDAjitblock(taskk, pi[j]) <= taskk['period']:
                    feasible[kid+1][j] = 1
                else:
                    feasible[kid+1][j] = 0
            elif opt == 'tdamix':
                if btype == 'N':
                    if TDAcarry(taskk, pi[j]) <= taskk['period'] or TDAblock(taskk, pi[j]) <= taskk['period'] or  TDAjit(taskk, pi[j]) <= taskk['period'] or TDAjitblock(taskk, pi[j]) <= taskk['period']:
                        feasible[kid+1][j] = 1
                    else:
                        feasible[kid+1][j] = 0
                else:
                    if TDAcarry(taskk, pi[j]) <= taskk['period'] or  TDAjit(taskk, pi[j]) <= taskk['period']:
                        feasible[kid+1][j] = 1
                    else:
                        feasible[kid+1][j] = 0

            #constant time tests
            elif opt == 'CTbaseline':
                if CTbaseline(taskk, pi[j]):
                    feasible[kid+1][j] = 1
                else:
                    feasible[kid+1][j] = 0
            elif opt == 'CTcarry':
                if k2uFirstCarryinhypo(taskk, pi[j]):
                    feasible[kid+1][j] = 1
                else:
                    feasible[kid+1][j] = 0
            elif opt == 'CTblock':
                if k2uSecondBlockinghypo(taskk, pi[j]):
                    feasible[kid+1][j] = 1
                else:
                    feasible[kid+1][j] = 0
            elif opt == 'CTjit':
                if k2qJitterBound(taskk, pi[j]):
                    feasible[kid+1][j] = 1
                else:
                    feasible[kid+1][j] = 0
            elif opt == 'CTmix':
                if btype == 'N':
                    if k2uFirstCarryinhypo(taskk, pi[j]) or k2uSecondBlockinghypo(taskk, pi[j]) or k2qJitterBound(taskk, pi[j]):
                        feasible[kid+1][j] = 1
                    else:
                        feasible[kid+1][j] = 0
                else:
                    if k2uFirstCarryinhypo(taskk, pi[j]) or k2qJitterBound(taskk, pi[j]):
                        feasible[kid+1][j] = 1
                    else:
                        feasible[kid+1][j] = 0


        #print feasible[kid+1]
        feasibleNum = sum( feasible[kid+1] )
        #print feasibleNum
        if feasibleNum != 0:
            #First-fit
            if fit == 'first':
                for ind, j in enumerate(feasible[kid+1]):
                    if j != 0:
                        pi[ind].append(taskk)
                        readPi[ind].append(kid+1)
                        break
            #Last-fit
            elif fit == 'last':
                for ind, j in reversed(list(enumerate(feasible[kid+1]))):
                    if j != 0:
                        pi[ind].append(taskk)
                        readPi[ind].append(kid+1)
                        break
            #Worst-fit
            elif fit == 'worst':
                ulist = []
                for ind, i in enumerate(feasible[kid+1]):
                    if i == 1:
                        sumU = 0.0
                        for u in pi[ind]:
                            sumU += utili(u)
                        ulist.append(sumU)
                    else:
                        ulist.append(100)
                for ind, j in enumerate(ulist):
                    if j == min(ulist):
                        pi[ind].append(taskk)
                        readPi[ind].append(kid+1)
                        break
            #Best-Fit
            elif fit == 'best':
                ulist = []
                for ind, i in enumerate(feasible[kid+1]):
                    if i == 1:
                        sumU = 0.0
                        for u in pi[ind]:
                            sumU += utili(u)
                        ulist.append(sumU)
                    else:
                        ulist.append(-1)
                #print ulist
                for ind, j in enumerate(ulist):
                    if j == max(ulist):
                        pi[ind].append(taskk)
                        readPi[ind].append(kid+1)
                        break
        else:
            r += 1
            tmplist = []
            tmplist.append(taskk)
            pi.append(tmplist)
            readPi.append([kid+1])
        c+=1
    #print opt+'-res: '+str(r)
    #print readPi
    return (r, readPi)
