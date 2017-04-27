from __future__ import division
from gurobipy import *
from miscs import *
import numpy as np

#following Tests are prepared for double checking
def CTbaseline(k, rest):
    tmpSum = 0.0
    for i in rest:
        tmpSum +=utiliAddE(i)
    tmpSum = utiliAddE(k)+tmpSum
    #print tmpSum
    if tmpSum <= np.log(2):
        return True
    else:
        return False

def k2uFirstCarryinhypo(k, rest):
    tmpSum = 1.0
    for i in rest:
        tmpSum*=(utili(i)+1)
    tmpSum = (utiliAddE(k)+2)*tmpSum
    #print tmpSum
    if tmpSum <= 3:
        return True
    else:
        return False
def k2uFirstCarryinUbound(k, rest):
    tmpSum = 0.0
    for i in rest:
        tmpSum += utili(i)
    #print tmpSum
    #print np.log(3/(utiliAddE(k)+2))
    #print ""
    if tmpSum <= np.log(3/(utiliAddE(k)+2)):
        return True
    else:
        return False
def k2uSecondBlockinghypo(k, rest):
    tmpSum = 0.0
    tmpSumP = 1.0
    for i in rest:
        tmpSum += min(i['shared-R'], i['exclusive-R'])
        tmpSumP *= utili(i)+1
    res = ((k['shared-R']+tmpSum+k['exclusive-R'])/k['period']+1)
    if res * tmpSumP <= 2:
        return True
    else:
        return False

def k2uSecondBlockingUbound(k, rest):
    tmpSum = 0.0
    tmpSumP = 0.0
    for i in rest:
        tmpSum += min(i['shared-R'], i['exclusive-R'])
        tmpSumP += utili(i)

    #print (k['shared-R']+k['exclusive-R']+tmpSum)/k['period']+tmpSumP
    #print (len(rest)+1)
    #print (2**(1/(len(rest)+1))-1)
    if ((k['shared-R']+k['exclusive-R']+tmpSum)/k['period'])+tmpSumP<=(len(rest)+1)*(2**(1/(len(rest)+1))-1):
        return True
    else:
        return False
def k2qJitterBound(k, rest):
    tmpSum = 0.0
    tmpSumP = 0.0
    for i in rest:
        tmpSum += vfunc(i)
        tmpSumP += utili(i)
    #if (k['shared-R']+k['exclusive-R']+tmpSum)/1-tmpSumP <= k['period']:
    if utiliAddE(k)+tmpSum/k['period']+tmpSumP<=1 and tmpSumP <=1:
        return True
    else:
        return False
def inflation(k, rest, alltasks):
    tmpSum = 0.0
    for i in rest:
        tmpSum += utili(i)
    if utili(k)+tmpSum <= np.log(3/(2+max(utiliAddE(j) for j in alltasks))):
        return True
    else:
        return False

