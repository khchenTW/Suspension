#mapping function for a quick use
def utili(task):
    return float(task['shared-R']/task['period'])

def utiliAddE(task):
    '''
    print task['block']
    print task['exclusive-R']
    print task['shared-R']
    print task['period']
    '''
    return float((task['shared-R']+task['exclusive-R']+task['block'])/task['period'])

def zfunc(task):
    return task['resource']

def vfunc(task):
    return float(2*task['shared-R']-task['shared-R']*task['shared-R']/task['period'])

def qfunc(task):
    return float(min(task['shared-R'],task['exclusive-R']))

def RMsort(tasks, criteria):
    return sorted(tasks, key=lambda item:item[criteria])
