from gurobipy import *
from miscs import *
import numpy as np

#following Tests are prepared for double checking
def k2uFirstCarryinUbound(k, rest):
    if quicksum(utili(i) for i in rest) <= np.log(3/(utiliAddE(k)+2)):
        return True
    else:
        return False
def k2uSecondBlockingUbound(k, rest):
    if (k['shared-R']+k['exclusive-R']+quicksum(min(i['shared-R'], i['exclusive-R']) for i in rest))/k['period']+quicksum(utili(i) for i in rest)<=(len(rest)+1)*(2**(1/(len(rest)+1))-1):
        return True
    else:
        return False
def k2qJitterBound(k, rest):
    if (k['shared-R']+k['exclusive-R']+quicksum(vfunc(i) for i in rest))/1-quicksum(utili(i) for i in rest) <= k['period']:
        return True
    else:
        return False
def inflation(k, rest, alltasks):
    if utili(k)+quicksum(utili(i) for i in rest) <= np.log(3/(2+max(utiliAddE(j) for j in alltasks))):
        return True
    else:
        return False

