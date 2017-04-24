#mapping function for a quick use
def utili(task):
    return float(task['shared-R']/task['period'])

def utiliAddE(task):
    return float((task['shared-R']+task['exclusive-R'])/task['period'])

def vfunc(task):
    return float(2*task['shared-R']-task['shared-R']*task['shared-R']/task['period'])

def qfunc(task):
    return float(min(task['shared-R'],task['exclusive-R'])/task['period'])

