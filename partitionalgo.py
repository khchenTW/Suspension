from gurobipy import *
import numpy as np
import re

def RMsort(tasks, criteria):
    return sorted(tasks, key=lambda item:item[criteria])

class task (dict):
    def __init__(self, sharedR, period, deadline, exclusiveR):
        dict.__setitem__(self, "shared-R", float (sharedR))
        dict.__setitem__(self, "period", float (period))
        dict.__setitem__(self, "deadline", float (deadline))
        dict.__setitem__(self, "exclusive-R", float (exclusiveR))

def partition(taskset, algoopt=13):
    #following Tests are prepared for double checking
    def test5b(k, rest):
        if quicksum(utili(i) for i in rest) <= np.log(3/(utiliAddE(k)+2)):
            return True
        else:
            return False
    def test6c(k, rest):
        if (k['shared-R']+k['exclusive-R']+quicksum(min(i['shared-R'], i['exclusive-R']) for i in rest))/k['period']+quicksum(utili(i) for i in rest)<=(len(rest)+1)*(2**(1/(len(rest)+1))-1):
            return True
        else:
            return False
    def test7(k, rest):
        if (k['shared-R']+k['exclusive-R']+quicksum(vfunc(i) for i in rest))/1-quicksum(utili(i) for i in rest) <= k['period']:
            return True
        else:
            return False

    #mapping function for a quick use
    def utili(task):
        return float(task['shared-R']/task['period'])

    def utiliAddE(task):
        return float((task['shared-R']+task['exclusive-R'])/task['period'])

    def vfunc(task):
        return float(2*task['shared-R']-task['shared-R']*task['shared-R']/task['period'])

    def qfunc(task):
        return float(min(task['shared-R'],task['exclusive-R'])/task['period'])

    #this sorted task set will be used
    tmpTasks=RMsort(taskset, 'period')
    m = Model("Partition Algorithm ILP")
    m.setParam('OutputFlag', False)
    y = m.addVars(len(tmpTasks), vtype=GRB.BINARY, name="allocation")
    x = m.addVars(len(tmpTasks), len(tmpTasks), vtype=GRB.BINARY, name="resourcej")
    #minimization
    m.setObjective((quicksum(y[j] for j in range(len(tmpTasks)))), GRB.MINIMIZE)

    #condition 9b
    m.addConstrs((quicksum(x[i,j] for j in range(len(tmpTasks))) == 1 for i in range(len(tmpTasks))), "9b")

    #condition 9c
    m.addConstrs((x[i,j]  <= y[j] for i in range(len(tmpTasks)) for j in range(len(tmpTasks))), "9c")

    #Schedulability conditions
    c = 0
    for kid, taskk in enumerate(tmpTasks): #i is the k task
        hpTasks = tmpTasks[:c]
        #ILP Eq10
        if algoopt == 10:
            m.addConstrs((quicksum( x[tid, j] * utili( i ) for tid, i in enumerate(hpTasks)) <= ( 1 - x[kid,j] ) + x[kid,j] * np.log(3/(utiliAddE(taskk)+2)) for j in range (len(tmpTasks))) , "Eq10")
        #ILP Eq11
        elif algoopt == 11:
            F = 1+quicksum((i['shared-R']+min(i['shared-R'], i['exclusive-R']))/i['period'] for i in tmpTasks)
            m.addConstrs((quicksum(utiliAddE( taskk )*x[kid, j]+ (utili(i) + qfunc(i))*x[tid, j] for tid, i in enumerate(hpTasks) ) <= x[kid,j]*np.log(2)+(1-x[kid,j])*F for j in range(len(tmpTasks))), "eq11")
            m.addConstr((quicksum((taskk['shared-R']+x[kid, j]*taskk['exclusive-R']+x[tid, j]*min(i['exclusive-R'], i['shared-R']))/taskk['period'] for tid, i in enumerate(hpTasks) for j in range(len(tmpTasks)))<=np.log(2)), "Cond") #(Sk+Bk)/Pk leq ln2
        #ILP Eq13
        elif algoopt == 13:
            m.addConstrs(( quicksum(utiliAddE( taskk )*x[kid, j]+(utili(i) + vfunc(i)/taskk['period'])*x[tid, j] for tid, i in enumerate(hpTasks) ) <= 1 for j in range (len(tmpTasks))) , "eq13")
        c+=1

    m.update()
    m.optimize()


    if m.status == GRB.Status.INF_OR_UNBD:
    # Turn presolve off to determine whether model is infeasible
    # or unbounded
        m.setParam(GRB.Param.Presolve, 0)
        m.optimize()

    if m.status == GRB.Status.OPTIMAL:
        print('ILP + Eq.'+str(algoopt)+' is feasible')
        for v in m.getVars():
            print('%s %g' % (v.varName, v.x))
        print('Obj: %g' % m.objVal)
        #validate results for all tasks respectively
        c = 0
        for kid, taskk in enumerate(tmpTasks): #i is the k task
            hpTasks = tmpTasks[:c]
            if algoopt == 10:
                #Eq.5b
                if test5b(taskk, hpTasks) is False:
                    print 'Task '+str(kid)+' is infesible with Eq5b.'
            elif algoopt == 11:
                #Eq.6c
                if test6c(taskk, hpTasks) is False:
                    print 'Task '+str(kid)+' is infesible with Eq6c.'
            elif algoopt == 13:
                #Eq.7
                if test7(taskk, hpTasks) is False:
                    print 'Task '+str(kid)+' is infesible with Eq7.'
            c+=1

        m.write('model.sol')
    elif m.status == GRB.Status.INFEASIBLE:
        print('Optimization was stopped with status %d' % m.status)
    # Model is infeasible - compute an Irreducible Inconsistent Subsystem (IIS)
        print('')
        print('Model is infeasible')
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
