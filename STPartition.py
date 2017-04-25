import numpy as np
from ctTests import *
from miscs import *
from TDA import *

def STPartition(tasks, opt, fit = 'first'):
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
            #if k2qJitterBound(taskk, pi[j]):#schedulability test
            #print TDAcarry(taskk, pi[j])
            #print TDAblock(taskk, pi[j])
            #print TDAjit(taskk, pi[j])
            #print 'Deadline:'+str(taskk['period'])

            #schedulability test
            if opt == 'carry':
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
            elif opt == 'CTcarry':
                if k2uFirstCarryinUbound(taskk, pi[j]):
                    feasible[kid+1][j] = 1
                else:
                    feasible[kid+1][j] = 0
            elif opt == 'CTblock':
                if k2uSecondBlockingUbound(taskk, pi[j]):
                    feasible[kid+1][j] = 1
                else:
                    feasible[kid+1][j] = 0
            elif opt == 'CTjit':
                if k2qJitterBound(taskk, pi[j]):
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
                for ind, j in enumerate(feasible[kid+1]):
                    if j != 0:
                        pi[ind].append(taskk)
                        readPi[ind].append(kid+1)
                        break

            #Best-Fit
            elif fit == 'best':
                for ind, j in enumerate(feasible[kid+1]):
                    if j != 0:
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
    return r
