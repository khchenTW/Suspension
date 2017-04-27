from gurobipy import *
import numpy as np
from ctTests import *
from miscs import *
import re


class task (dict):
    def __init__(self, sharedR, period, deadline, execlusiveR, resource):
        dict.__setitem__(self, "shared-R", float (sharedR))
        dict.__setitem__(self, "period", float (period))
        dict.__setitem__(self, "deadline", float (deadline))
        dict.__setitem__(self, "exclusive-R", float (execlusiveR))
        dict.__setitem__(self, "resource", float (resource))

def partition(taskset, algoopt='carryin'):

    #this sorted task set will be used
    tmpTasks=RMsort(taskset, 'period')

    assignCount = 0
    #preprocessiing are required for some cases
    filTasks = []
    if algoopt == 'inflation' :
        tmpTasks = sorted(tmpTasks, key=utiliAddE, reverse=True)
        for i in tmpTasks:
            if utiliAddE(i) > np.log(3/(2+utiliAddE(i))):
                assignCount +=1
            else:
                filTasks.append(i)
        tmpTasks = filTasks

    if algoopt == 'blocking' or algoopt == 'ilpbaseline':
        for i in tmpTasks:
            if (utiliAddE(i)) > np.log(2):
                assignCount +=1
            else:
                filTasks.append(i)
        tmpTasks = filTasks

    m = Model("Partition Algorithm Hete-ILP")
    m.setParam('OutputFlag', False)
    m.setParam('TimeLimit', 1*30)
    #m.setParam('BestObjStop', len(tmpTasks)/2)
    y = m.addVars(len(tmpTasks), vtype=GRB.BINARY, name="allocation")
    x = m.addVars(len(tmpTasks), len(tmpTasks), vtype=GRB.BINARY, name="resourcej")
    z = m.addVars(len(tmpTasks), vtype=GRB.BINARY, name="resourcez")
    #minimization
    m.setObjective((quicksum(y[j]*z[j] for j in range(len(tmpTasks)))), GRB.MINIMIZE)

    #condition ILP-M-one-resource-per-task
    m.addConstrs((quicksum(x[i,j] for j in range(len(tmpTasks))) == 1 for i in range(len(tmpTasks))), "ILP-M-one-resource-per-task")

    #condition ILP-M-task-allocated-to-resources
    m.addConstrs((x[i,j]*z[j]  <= y[j]*z[j] for i in range(len(tmpTasks)) for j in range(len(tmpTasks))), "ILP-M-task-allocated-to-resources")

    #condition ILP-M-one-to-one
    m.addConstrs((x[j,j] == y[j] for i in range(len(tmpTasks)) for j in range(len(tmpTasks))), "ILP-M-one-to-one")

    #Schedulability conditions
    c = 0
    for kid, taskk in enumerate(tmpTasks): #i is the k task
        hpTasks = tmpTasks[:c]
        #ILP ilp-carryin-ubound
        if algoopt == 'carryin':
            m.addConstrs((quicksum( x[tid, j] * utili( i ) for tid, i in enumerate(hpTasks)) <= ( 1 - x[kid,j] ) + x[kid,j] * np.log(3/(utiliAddE(taskk)+2)) for j in range (len(tmpTasks))) , "ilp-carryin-ubound")
        #ILP ilp-blocking-ubound
        elif algoopt == 'blocking':
            F = 1
            for i in tmpTasks:
                F+=(i['shared-R']+min(i['shared-R'], i['exclusive-R']))/i['period']
            m.addConstrs((utiliAddE( taskk )*x[kid, j]+quicksum((utili(i) + qfunc(i)/taskk['period'])*x[tid, j] for tid, i in enumerate(hpTasks) ) <= x[kid,j]*np.log(2)+(1-x[kid,j])*F for j in range(len(tmpTasks))), "ilp-blocking-ubound")
        #ILP ilp-k2q
        elif algoopt == 'k2q':
            m.addConstrs(( utiliAddE( taskk )*x[kid, j]+quicksum((utili(i) + vfunc(i)/taskk['period'])*x[tid, j] for tid, i in enumerate(hpTasks) ) <= len(tmpTasks)*(1-x[kid, j])+x[kid,j] for j in range (len(tmpTasks))) , "ilp-k2q")

        c+=1
    #ILP Inflation
    UB = 1.0
    if algoopt == 'inflation':
        if len(tmpTasks) != 0:
            UB = np.log(3/(2+max(utiliAddE(i) for i in tmpTasks)))
        m.addConstrs((quicksum(utili(i)*x[tid, j] for tid, i in enumerate(tmpTasks) ) <= UB for j in range (len(tmpTasks))), "inflation")
    if algoopt == 'ilpbaseline':
        m.addConstrs((quicksum(utiliAddE(i)*x[tid, j] for tid, i in enumerate(tmpTasks) ) <= np.log(2) for j in range (len(tmpTasks))), "inflation")

    m.update()
    m.write("model.lp")
    m.optimize()

    infeasible=0
    if m.status == GRB.Status.INF_OR_UNBD:
    # Turn presolve off to determine whether model is infeasible
    # or unbounded
        m.setParam(GRB.Param.Presolve, 0)
        m.optimize()
    elif m.status == GRB.Status.OPTIMAL:
        #print('ILP + '+algoopt+' is feasible')
        '''
        for v in m.getVars():
            print('%s %g' % (v.varName, v.x))
        print('Obj: %g' % m.objVal)
        print (algoopt+' Obj+pop: '+str(m.objVal+assignCount))
        '''
        m.write('model.sol')
    elif m.status == GRB.Status.INFEASIBLE:
        #print('Optimization was stopped with status %d' % m.status)
    # Model is infeasible - compute an Irreducible Inconsistent Subsystem (IIS)
        print('BUG:ILP + '+algoopt+' is infeasible')
        m.computeIIS()
        m.write("model.ilp")
        print("IIS written to file 'model.ilp'")
        return -1
    elif m.status == GRB.Status.TIME_LIMIT:
        if m.objVal < len(taskset):
            pass #do nothing but use the intermediate results
        else:
            timeout = 1 #infeasible flag
    elif m.status == GRB.Status.USER_OBJ_LIMIT:
        print ("BUG: LIMIT feature is disable")
        return -2
    else:
        #exception case, dump out this input
        print ("BUG: fatal exception in ILP"+algoopt)
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
            if algoopt == 'carryin':
                #k2u-first-carryin-ubound
                if k2uFirstCarryinUbound(taskk, hpTasks) is False:
                    print 'Task '+str(kid)+' is infesible with k2u-first-carryin-ubound.'
                    return -3
            elif algoopt == 'blocking':
                #k2u-second-blocking-ubound2
                if k2uSecondBlockingUbound(taskk, hpTasks) is False:
                    print 'Task '+str(kid)+' is infesible with k2u-second-blocking-ubound2.'
                    return -3
            elif algoopt == 'k2q':
                #k2q-jitter-bound
                if k2qJitterBound(taskk, hpTasks) is False:
                    print 'Task '+str(kid)+' is infesible with k2q-jitter-bound.'
                    return -3
            elif algoopt == 'inflation':
                #inflation
                if inflation(taskk, hpTasks, tmpTasks) is False:
                    print 'Task '+str(kid)+' is infesible with inflation.'
                    return -3
            c+=1
    if infeasible == 0:
        return int(m.objVal+assignCount)
    else:
        sumZ = 0
        for i in taskset:
            sumZ += i['resource']
        return sumZ
