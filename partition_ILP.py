from gurobipy import *
import numpy as np
from ctTests import *
from miscs import *

def RMsort(tasks, criteria):
    return sorted(tasks, key=lambda item:item[criteria])

class task (dict):
    def __init__(self, sharedR, period, deadline, exclusiveR):
        dict.__setitem__(self, "shared-R", float (sharedR))
        dict.__setitem__(self, "period", float (period))
        dict.__setitem__(self, "deadline", float (deadline))
        dict.__setitem__(self, "exclusive-R", float (exclusiveR))

def partition(taskset, algoopt='carryin'):

    #this sorted task set will be used
    tmpTasks=RMsort(taskset, 'period')

    assignCount = 0
    #preprocessiing are required for some cases
    if algoopt == 'inflation':
        tmpTasks = sorted(tmpTasks, key=utiliAddE, reverse=True)
        for i in tmpTasks:
            if utiliAddE(i) > np.log(3/(2+utiliAddE(i))):
                tmpTasks.pop(0)
                assignCount +=1

    if algoopt == 'blocking':
        for i in tmpTasks:
            if (i['exclusive-R']+i['shared-R']) >= np.log(2):
                tmpTasks.pop(0)
                assignCount +=1

    m = Model("Partition Algorithm ILP")
    m.setParam('OutputFlag', False)
    y = m.addVars(len(tmpTasks), vtype=GRB.BINARY, name="allocation")
    x = m.addVars(len(tmpTasks), len(tmpTasks), vtype=GRB.BINARY, name="resourcej")
    #minimization
    m.setObjective((quicksum(y[j] for j in range(len(tmpTasks)))), GRB.MINIMIZE)

    #condition ilp-resource-single-b
    m.addConstrs((quicksum(x[i,j] for j in range(len(tmpTasks))) == 1 for i in range(len(tmpTasks))), "ilp-resource-single-b")

    #condition ilp-resource-single-c
    m.addConstrs((x[i,j]  <= y[j] for i in range(len(tmpTasks)) for j in range(len(tmpTasks))), "ilp-resource-single-c")

    #Schedulability conditions
    c = 0
    for kid, taskk in enumerate(tmpTasks): #i is the k task
        hpTasks = tmpTasks[:c]
        #ILP ilp-carryin-ubound
        if algoopt == 'carryin':
            m.addConstrs((quicksum( x[tid, j] * utili( i ) for tid, i in enumerate(hpTasks)) <= ( 1 - x[kid,j] ) + x[kid,j] * np.log(3/(utiliAddE(taskk)+2)) for j in range (len(tmpTasks))) , "ilp-carryin-ubound")
        #ILP ilp-blocking-ubound
        elif algoopt == 'blocking':
            F = 1+quicksum((i['shared-R']+min(i['shared-R'], i['exclusive-R']))/i['period'] for i in tmpTasks)
            m.addConstrs((utiliAddE( taskk )*x[kid, j]+quicksum((utili(i) + qfunc(i)/taskk['period'])*x[tid, j] for tid, i in enumerate(hpTasks) ) <= x[kid,j]*np.log(2)+(1-x[kid,j])*F for j in range(len(tmpTasks))), "ilp-blocking-ubound")
            m.addConstrs((utiliAddE( taskk )*x[kid, j] <= x[kid,j]*np.log(2) for j in range(len(tmpTasks))), "Cond") #(sk+ek)/pk leq ln2
            #m.addConstrs((taskk['shared-R']+x[kid, j]*taskk['exclusive-R']+quicksum(x[tid, j]*qfunc(i) for tid, i in enumerate(hpTasks) )/taskk['period'] <=np.log(2) for j in range(len(tmpTasks))), "Cond") #(Sk+Bk)/Pk leq ln2
        #ILP ilp-k2q
        elif algoopt == 'k2q':
            m.addConstrs(( utiliAddE( taskk )*x[kid, j]+quicksum((utili(i) + vfunc(i)/taskk['period'])*x[tid, j] for tid, i in enumerate(hpTasks) ) <= len(tmpTasks)*(1-x[kid, j])+x[kid,j] for j in range (len(tmpTasks))) , "ilp-k2q")

        c+=1
    #ILP Inflation
    if algoopt == 'inflation':
        UB = np.log(3/(2+max(utiliAddE(i) for i in tmpTasks)))
        '''
        UB = 1.0
        if np.log(3/(2+utiliAddE(taskk))) < UB:
            UB = np.log(3/(2+utiliAddE(taskk)))
        print "UB="+ str(UB)
        '''
        m.addConstrs((quicksum(utili(i)*x[tid, j] for tid, i in enumerate(tmpTasks) ) <= UB for j in range (len(tmpTasks))), "inflation")

    m.update()
    m.optimize()


    if m.status == GRB.Status.INF_OR_UNBD:
    # Turn presolve off to determine whether model is infeasible
    # or unbounded
        m.setParam(GRB.Param.Presolve, 0)
        m.optimize()

    if m.status == GRB.Status.OPTIMAL:
        print('ILP + '+algoopt+' is feasible')
        '''
        for v in m.getVars():
            print('%s %g' % (v.varName, v.x))
        print('Obj: %g' % m.objVal)
        '''
        print ('Obj+pop: '+str(m.objVal+assignCount))
        #validate results for all tasks respectively
        c = 0
        for kid, taskk in enumerate(tmpTasks): #i is the k task
            hpTasks = tmpTasks[:c]
            if algoopt == 'carryin':
                #k2u-first-carryin-ubound
                if k2uFirstCarryinUbound(taskk, hpTasks) is False:
                    print 'Task '+str(kid)+' is infesible with k2u-first-carryin-ubound.'
            elif algoopt == 'blocking':
                #k2u-second-blocking-ubound2
                if k2uSecondBlockingUbound(taskk, hpTasks) is False:
                    print 'Task '+str(kid)+' is infesible with k2u-second-blocking-ubound2.'
            elif algoopt == 'k2q':
                #k2q-jitter-bound
                if k2qJitterBound(taskk, hpTasks) is False:
                    print 'Task '+str(kid)+' is infesible with k2q-jitter-bound.'
            elif algoopt == 'inflation':
                #inflation
                if inflation(taskk, hpTasks, tmpTasks) is False:
                    print 'Task '+str(kid)+' is infesible with inflation.'
                pass
            c+=1

        m.write('model.sol')
    elif m.status == GRB.Status.INFEASIBLE:
        #print('Optimization was stopped with status %d' % m.status)
    # Model is infeasible - compute an Irreducible Inconsistent Subsystem (IIS)
        print('ILP + '+algoopt+' is infeasible')
        m.computeIIS()
        m.write("model.ilp")
        print("IIS written to file 'model.ilp'")
        return -1
    # prepare readable solution
    '''
    mapped = [var for var in m.getVars() if var.varName.find('allocation') != -1 and var.x != 0]
    procs = [[] for amount in range(taskset)]
    for task_map in mapped:
        parsed = re.findall("[0-9]+,[0-9]+", task_map.varName)[0].split(',')
        taskID = int(parsed[0])
        procID = int(parsed[1])
        procs[procID].append(tskset[taskID])
    '''

    return m.objVal
