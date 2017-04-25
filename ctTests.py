from __future__ import division
from gurobipy import *
from miscs import *
import numpy as np

#following Tests are prepared for double checking
def k2uFirstCarryinUbound(k, rest):
    tmpSum = 0.0
    for i in rest:
        tmpSum += utili(i)
    if tmpSum <= np.log(3/(utiliAddE(k)+2)):
        #print quicksum(utili(i) for i in rest)
        #print np.log(3/(utiliAddE(k)+2))
        return True
    else:
        return False
def k2uSecondBlockingUbound(k, rest):
    #print (k['shared-R']+k['exclusive-R']+quicksum(min(i['shared-R'], i['exclusive-R']) for i in rest))/k['period']+quicksum(utili(i) for i in rest)
    #print (len(rest)+1)
    #print (2**(1/(len(rest)+1))-1)
    tmpSum = 0.0
    for i in rest:
        tmpSum += min(i['shared-R'], i['exclusive-R'])
    if (k['shared-R']+k['exclusive-R']+tmpSum)<=(len(rest)+1)*(2**(1/(len(rest)+1))-1):
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
    if utiliAddE(k)+tmpSum/k['period']+tmpSumP<=1 and tmpSumP <1:
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

