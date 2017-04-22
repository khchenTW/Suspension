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

def partition(taskset):
    '''
    if analysis.cumulative_utilisation(taskset) > processors:
        raise ValueError("utilisation is too large")
    '''
    def utili(task):
        return float(task['execution']/task['period'])

    def utiliAddE(task):
        return float(task['execution']+task['suspension']/task['period'])

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

    #condition Eq 10
    c = 0
    #here need RM sorting
    tmpTasks=RMsort(taskset, 'period')
    for kid, taskk in enumerate(tmpTasks): #i is the k task
        hpTasks = tmpTasks[:c]
        m.addConstrs((
        quicksum( x[tid, j] * utili( i ) for tid, i in enumerate(hpTasks)) <= ( 1 - x[kid,j] ) + x[kid,j] * np.log(3/(utiliAddE(taskk)+2)) for j in range (len(taskset))) , "eq10")
        c+=1


    m.update()
    m.optimize()

    # prepare readable solution
    '''
    mapped = [var for var in m.getVars() if var.varName.find('allocation') != -1 and var.x != 0]
    procs = [[] for amount in range(processors)]
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
