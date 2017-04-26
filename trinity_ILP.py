from gurobipy import *
import numpy as np
from ctTests import *
from miscs import *
import re


class task (dict):
    def __init__(self, sharedR, period, deadline, exclusiveR):
        dict.__setitem__(self, "shared-R", float (sharedR))
        dict.__setitem__(self, "period", float (period))
        dict.__setitem__(self, "deadline", float (deadline))
        dict.__setitem__(self, "exclusive-R", float (exclusiveR))

def partition(taskset):

    #this sorted task set will be used
    tmpTasks=RMsort(taskset, 'period')

    m = Model("Partition Algorithm Trinity-ILP")
    m.setParam('OutputFlag', False)
    m.setParam('TimeLimit', 5*60)
    m.setParam('BestObjStop', len(tmpTasks)/2)
    y = m.addVars(len(tmpTasks), vtype=GRB.BINARY, name="allocation")
    x = m.addVars(len(tmpTasks), len(tmpTasks), vtype=GRB.BINARY, name="resourcej")
    z = m.addVars(len(tmpTasks), len(tmpTasks), 3, vtype=GRB.BINARY, name="trinity")
    #minimization
    m.setObjective((quicksum(y[j] for j in range(len(tmpTasks)))), GRB.MINIMIZE)

    #condition trinity
    m.addConstrs((quicksum(z[i,j,l] for l in range(3)) >= x[i,j] for i in range(len(tmpTasks)) for j in range(len(tmpTasks))),"trinitylimit")


    #condition ilp-resource-single-b
    m.addConstrs((quicksum(x[i,j] for j in range(len(tmpTasks))) == 1 for i in range(len(tmpTasks))), "ilp-resource-single-b")


    #condition ilp-resource-single-c
    m.addConstrs((x[i,j]  <= y[j] for i in range(len(tmpTasks)) for j in range(len(tmpTasks))), "ilp-resource-single-c")


    #Schedulability conditions
    c = 0
    for kid, taskk in enumerate(tmpTasks): #i is the k task
        hpTasks = tmpTasks[:c]
        #ILP ilp-carryin-ubound
        m.addConstrs((quicksum( z[tid, j, 0] * utili( i ) for tid, i in enumerate(hpTasks)) <= ( 1 - z[kid,j,0] ) + z[kid,j,0] * np.log(3/(utiliAddE(taskk)+2)) for j in range (len(tmpTasks))) , "ilp-carryin-ubound")
        #ILP ilp-blocking-ubound
        F = 1
        for i in tmpTasks:
            F+=(i['shared-R']+min(i['shared-R'], i['exclusive-R']))/i['period']
        m.addConstrs((utiliAddE( taskk )*z[kid, j, 1]+quicksum((utili(i) + qfunc(i)/taskk['period'])*x[tid, j] for tid, i in enumerate(hpTasks) ) <= z[kid,j,1]*np.log(2)+(1-z[kid,j,1])*F for j in range(len(tmpTasks))), "ilp-blocking-ubound")
        #ILP ilp-k2q
        m.addConstrs(( utiliAddE( taskk )*z[kid,j,2]+quicksum((utili(i) + vfunc(i)/taskk['period'])*z[tid, j, 2] for tid, i in enumerate(hpTasks) ) <= len(tmpTasks)*(1-z[kid,j,2])+z[kid,j,2] for j in range (len(tmpTasks))) , "ilp-k2q")

        c+=1
    m.update()
    m.write("model.lp")
    m.optimize()


    if m.status == GRB.Status.INF_OR_UNBD:
    # Turn presolve off to determine whether model is infeasible
    # or unbounded
        m.setParam(GRB.Param.Presolve, 0)
        m.optimize()

    if m.status == GRB.Status.OPTIMAL:
        #print('ILP is feasible')

        for v in m.getVars():
            print('%s %g' % (v.varName, v.x))
        print('Obj: %g' % m.objVal)
        print (' Obj+pop: '+str(m.objVal+assignCount))

        m.write('model.sol')
    elif m.status == GRB.Status.INFEASIBLE:
        #print('Optimization was stopped with status %d' % m.status)
    # Model is infeasible - compute an Irreducible Inconsistent Subsystem (IIS)
        print('ILP is infeasible')
        m.computeIIS()
        m.write("model.ilp")
        print("IIS written to file 'model.ilp'")
        return -1

    mapped = [var for var in m.getVars() if var.varName.find('resourcej') != -1 and var.x != 0]
    res = [[] for amount in range(len(taskset))]

    for task_map in mapped:
        #print task_map.varName
        parsed = re.findall("[0-9]+,[0-9]+", task_map.varName)[0].split(',')
        taskID = int(parsed[0])
        procID = int(parsed[1])
        res[procID].append(tmpTasks[taskID])
    #now each resource has the assigned tasks in the corresponding list
    for i, setOnRes in enumerate(res):
    # verify with ctTests per resource
        c = 0
        if len(setOnRes) == 0:
            continue
        #print 's:'+str(setOnRes)
        for kid, taskk in enumerate(setOnRes):
            hpTasks = setOnRes[:c]
            if k2uFirstCarryinUbound(taskk, hpTasks) or k2uSecondBlockingUbound(taskk, hpTasks) or k2qJitterBound(taskk, hpTasks):
                pass
            else:
                print 'Task '+str(kid)+' is totally infeasible among three tests.'
            c+=1

    return int(m.objVal)
