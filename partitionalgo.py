from gurobipy import *
import numpy as np
import re

def RMsort(tasks, criteria):
    return sorted(tasks, key=lambda item:item[criteria])

class task (dict):
    def __init__(self, execution, period, deadline):
        dict.__setitem__(self, "execution", float (execution))
        dict.__setitem__(self, "period", float (period))
        dict.__setitem__(self, "deadline", float (deadline))
        dict.__setitem__(self, "suspension", float (suspension))

def partition(taskset, algoopt=13):
    '''
    if analysis.cumulative_utilisation(taskset) > processors:
        raise ValueError("utilisation is too large")
    '''
    def test5b(k, rest):
        if quicksum(utili(i) for i in rest) <= np.log(3/(utiliAddE(k)+2)):
            return True
        else:
            return False
    def test6c(k, rest):
        if (k['suspension']+k['execution']+quicksum(min(i['execution'], i['suspension']) for i in rest))/k['period']+quicksum(utili(i) for i in rest)<=(len(rest)+1)(2**(1/len(rest)+1)-1):
            return True
        else:
            return False
    def test7(k, rest):
        if (k['execution']+k['suspension']+quicksum(vfunc(i) for i in rest))/1-quicksum(utili(i) for i in rest) <= k['period']:
            return True
        else:
            return False

    def utili(task):
        return float(task['execution']/task['period'])

    def utiliAddE(task):
        return float(task['execution']+task['suspension']/task['period'])

    def vfunc(task):
        return float(2*task['suspension']-task['suspension']*task['suspension']/task['period'])

    def qfunc(task):
        return float(min(task['execution'],task['suspension'])/task['period'])

    # index the tasks once to keep track of task ids during paritioning into subsets of equal periods
    tskset = {}
    for tid, task in enumerate(taskset):
        tskset[tid] = task

    m = Model("Partition Algorithm ILP")
    y = m.addVars(len(taskset), vtype=GRB.BINARY, name="allocation")
    x = m.addVars(len(taskset), len(taskset), vtype=GRB.BINARY, name="resourcej")
    #minimization
    m.setObjective((quicksum(y[j] for j in range(len(taskset)))), GRB.MINIMIZE)

    #condition 9b
    m.addConstrs((quicksum(x[i,j] for j in range(len(taskset))) == 1 for i in range(len(taskset))), "9b")

    #condition 9c
    m.addConstrs((quicksum(x[i,j] for i in range(len(taskset))) <= y[j] for j in range(len(taskset))), "9c")

    #Schedulability conditions
    c = 0
    #here need RM sorting
    tmpTasks=RMsort(taskset, 'period')
    for kid, taskk in enumerate(tmpTasks): #i is the k task
        hpTasks = tmpTasks[:c]
        #ILP Eq10
        if algoopt == 10:
            m.addConstrs((quicksum( x[tid, j] * utili( i ) for tid, i in enumerate(hpTasks)) <= ( 1 - x[kid,j] ) + x[kid,j] * np.log(3/(utiliAddE(taskk)+2)) for j in range (len(taskset))) , "eq10")
        #ILP Eq11
        elif algoopt == 11:
            F = quicksum(1+i['suspension']+min(i['execution'], i['suspension'])/i['period'] for i in taskset)
            m.addConstrs((quicksum(utiliAddE( taskk )*x[kid, j]+ (utili(i) + qfunc(i))*x[tid, j] for tid, i in enumerate(hpTasks) ) <= x[kid,j]*np.log(2)+(1-x[kid,j])*F for j in range(len(taskset))), "eq11")
            m.addConstr((quicksum((taskk['suspension']+x[kid, j]*taskk['execution']+x[tid, j]*min(i['execution'], i['suspension'])/taskk['period']) for tid, i in enumerate(hpTasks) for j in range(len(taskset)))<=np.log(2)), "Cond") #(Sk+Bk)/Pk leq ln2
        #ILP Eq13
        elif algoopt == 13:
            m.addConstrs(( quicksum(utiliAddE( taskk )*x[kid, j]+utili(i) + vfunc(i)/taskk['period']*x[tid, j] for tid, i in enumerate(hpTasks) ) <= 1 for j in range (len(taskset))) , "eq13")
        c+=1

    m.update()
    m.optimize()

    if m.status == GRB.Status.INF_OR_UNBD:
    # Turn presolve off to determine whether model is infeasible
    # or unbounded
        m.setParam(GRB.Param.Presolve, 0)
        m.optimize()

    if m.status == GRB.Status.OPTIMAL:
        for v in m.getVars():
            print('%s %g' % (v.varName, v.x))
        print('Obj: %g' % m.objVal)
        #validate results for all tasks respectively
        c = 0
        #here we need RM sorting
        tmpTasks=RMsort(taskset, 'period')
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
    elif m.status != GRB.Status.INFEASIBLE:
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
    #validate results to be sure nothing went wrong
    '''
    for i, proc in enumerate(procs):
        if analysis.schedulable(proc) is False:
            print 'Partition on processor '+str(i)+' is infeasible.'
    '''




    return 1
