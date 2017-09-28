from gurobipy import *
import numpy as np
from ctTests import *
from miscs import *
import re

class task (dict):
    def __init__(self, sharedR, period, deadline, execlusiveR, resource, block):
        dict.__setitem__(self, "shared-R", float (sharedR))
        dict.__setitem__(self, "period", float (period))
        dict.__setitem__(self, "deadline", float (deadline))
        dict.__setitem__(self, "exclusive-R", float (execlusiveR))
        dict.__setitem__(self, "resource", int (resource))
        dict.__setitem__(self, "block", int (block))

def partition(taskset):

    #this sorted task set will be used
    tmpTasks=RMsort(taskset, 'period')

    m = Model("Partition Algorithm Combo-ILP")
    m.setParam('OutputFlag', False)
    m.setParam('TimeLimit', 1*60)
    #m.setParam('TimeLimit', 1)
    #m.setParam('BestObjStop', len(tmpTasks)/2)
    y = m.addVars(len(tmpTasks), vtype=GRB.BINARY, name="allocation")
    x = m.addVars(len(tmpTasks), len(tmpTasks), vtype=GRB.BINARY, name="resourcej")
    eta = m.addVars(len(tmpTasks), len(tmpTasks), 3, vtype=GRB.BINARY, name="combo")
    #minimization
    m.setObjective((quicksum(y[j]*taskj['resource'] for j, taskj in enumerate(tmpTasks))), GRB.MINIMIZE)

    #condition combo
    m.addConstrs((quicksum(eta[i,j,l] for l in range(3)) >= x[i,j] for i in range(len(tmpTasks)) for j in range(len(tmpTasks))),"combolimit")

    #condition ILP-M-one-resource-per-task
    m.addConstrs((quicksum(x[i,j] for j in range(len(tmpTasks))) == 1 for i in range(len(tmpTasks))), "ILP-M-one-resource-per-task")

    #condition ILP-M-task-allocated-to-resources
    m.addConstrs((x[i,j]*tmpTasks[i]['resource'] <= y[j]*tmpTasks[j]['resource'] for i in range(len(tmpTasks)) for j in range(len(tmpTasks))), "ILPM")
    #condition ILP-M-one-to-one
    m.addConstrs((x[j,j] == y[j] for i in range(len(tmpTasks)) for j in range(len(tmpTasks))), "ILP-M-one-to-one")

    #Schedulability conditions
    c = 0
    for kid, taskk in enumerate(tmpTasks): #i is the k task
        hpTasks = tmpTasks[:c]
        #ILP ilp-carryin-ubound
        m.addConstrs((quicksum( x[tid, j] * utili( i ) for tid, i in enumerate(hpTasks)) <= ( 1 - eta[kid,j,0] ) + eta[kid,j,0] * np.log(3/(utiliAddE(taskk)+2)) for j in range (len(tmpTasks))) , "ilp-carryin-ubound")
        #ILP ilp-blocking-ubound
        F = 1
        for i in tmpTasks:
            F+=(i['shared-R']+min(i['shared-R'], i['exclusive-R']))/i['period']
        m.addConstrs(((utiliAddE( taskk )-np.log(2))*eta[kid, j, 1]+quicksum((utili(i) + qfunc(i)/taskk['period'])*x[tid, j] for tid, i in enumerate(hpTasks) ) <= (1-eta[kid,j,1])*F for j in range(len(tmpTasks))), "ilp-blocking-ubound")
        #ILP ilp-k2q
        m.addConstrs(( utiliAddE( taskk )*eta[kid,j,2]+quicksum((utili(i) + vfunc(i)/taskk['period'])*x[tid, j] for tid, i in enumerate(hpTasks) ) <= len(tmpTasks)*(1-eta[kid,j,2])+eta[kid,j,2] for j in range (len(tmpTasks))) , "ilp-k2q")

        c+=1
    m.update()
    m.write("model.lp")
    m.optimize()

    infeasible = 0
    if m.status == GRB.Status.INF_OR_UNBD:
    # Turn presolve off to determine whether model is infeasible
    # or unbounded
        m.setParam(GRB.Param.Presolve, 0)
        m.optimize()
    elif m.status == GRB.Status.OPTIMAL:
        #print('ILP is feasible')

        for v in m.getVars():
            #print('%s %g' % (v.varName, v.x))
        #print('Obj: %g' % m.objVal)
        #print (' Obj+pop: '+str(m.objVal))
            pass
        m.write('model.sol')
    elif m.status == GRB.Status.INFEASIBLE:
        #print('Optimization was stopped with status %d' % m.status)
    # Model is infeasible - compute an Irreducible Inconsistent Subsystem (IIS)
        print('ILP is infeasible')
        m.computeIIS()
        m.write("model.ilp")
        print("IIS written to file 'model.ilp'")
        return -1
    elif m.status == GRB.Status.TIME_LIMIT:
        if m.objVal < len(taskset):
            pass #do nothing but use the intermediate results
        else:
            timeout = 1 #infeasible flag
    else:
        #exception case, dump out this input
        print ("BUG: fatal exception in ILP")
        return -2


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
                return -3
            c+=1
    if infeasible == 0:
        return int(m.objVal)
    else:
        return len(taskset)
