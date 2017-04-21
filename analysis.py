import generator as autogen
import sys
import numpy as np
import matplotlib.pyplot as plt
import itertools
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages
from os import listdir
from os.path import isfile, join

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
rcParams['ps.useafm'] = True
rcParams['pdf.use14corefonts'] = True
rcParams['text.usetex'] = True


def cumulative_utilisation (taskset, periods = {0.5,1,2,5,10,20,50,100,200,1000}):
#     if not periods:
#         return sum(map(lambda x : x['execution']/x['period'], taskset))

#     if periods.issubset({1,2,5,10,20,50,100,200,1000,'angle'}) is False:
#         raise ValueError("Set of periods must be a subset of {1, 2, 5, 10, 20, 100, 200, 1000}")
#         return -1
#     else:
    util = 0.0
    for period in periods:
        if (period == 0.5):
            util += sum(map(lambda task : task['execution'] / task['deadline'], filter(lambda task : task['period'] == period, taskset)))
        else:  
            util += sum(map(lambda task : task['execution'] / task['period'], filter(lambda task : task['period'] == period, taskset)))
    return util

def cumulative_execution (taskset, periods = {0.5,1,2,5,10,20,50,100,200,1000}):
    #print periods
    exe = 0.0
    for task in taskset:
        for period in periods:
            if (task['period'] == period):
                #print task['execution']
                exe  += task['execution']
    return exe

def max_wcet (taskset, periods = {0.5,1,2,5,10,20,50,100,200,1000}):
#     if not periods:
#         return 0.0
#     if periods.issubset({1,2,5,10,20,50,100,200,1000}) is False:
#         raise ValueError("Set of periods must be a subset of {1, 2, 5, 10, 20, 100, 200, 1000}")
#         return -1
#     else:
    wcet = 0.0
    for task in taskset:
        for period in periods:
            if (task['period'] == period):
                if (task['execution'] > wcet):
                    wcet = task['execution']
    return wcet

def z_util (taskset):
    return cumulative_utilisation(taskset, {100,200,1000})

def y_util(taskset):
    return cumulative_utilisation(taskset, {1})


def schedulable(taskset):
#      if not taskset:
#          return False
     
     cond_1 = (cumulative_utilisation(taskset) <= 1)
     cond_2 = cumulative_utilisation(taskset, {1,2,5}) <= max((1-0.2*(cumulative_utilisation(taskset, {2}))), (0.8 + 0.2*(cumulative_utilisation(taskset, {1,2}))))
     cond_3 = cumulative_utilisation(taskset, {1,2,5,10,20,50}) <= max((1-0.2*cumulative_utilisation(taskset, {20})), (0.8 + 0.2*(cumulative_utilisation(taskset, {1,2,5,10,20}))))
 
     if (cond_1 and cond_2 and cond_3):
        return True
     else:
        return False
        
def schedulable_np(taskset):
#     if not taskset:
#         return False
    
    cond_1 = (max_wcet(taskset, {2,5,10,20,50,100,200,1000})/1.0 + cumulative_utilisation(taskset, {1})) <= 1
#     if (cond_1 == False):
#         print 1
#         print max_wcet(taskset, {2,5,10,20,50,100,200,1000})/1.0
    cond_2 = (max_wcet(taskset, {5,10,20,50,100,200,1000})/2.0 + cumulative_utilisation(taskset, {1,2})) <= 1
#     if (cond_2 == False):
#         print 2
#         print max_wcet(taskset, {5,10,20,50,100,200,1000})/2.0
    cond_10 = (max_wcet(taskset, {20,50,100,200,1000})/10.0 + cumulative_utilisation(taskset, {1,2,5,10})) <= 1
    cond_20 = (max_wcet(taskset, {50,100,200,1000})/20.0 + cumulative_utilisation(taskset, {1,2,5,10,20})) <= 1
    cond_100 = (max_wcet(taskset, {200,1000})/100.0 + cumulative_utilisation(taskset, {1,2,5,10,20,50,100})) <= 1
    cond_200 = (max_wcet(taskset, {1000})/200.0 + cumulative_utilisation(taskset, {1,2,5,10,20,50,100,200})) <= 1
    cond_1000 = (cumulative_utilisation(taskset, {1,2,5,10,20,50,100,200,1000})) <= 1
    #cond_5 = (max_wcet(taskset, {10,20,50,100,200,1000})/5.0 + cumulative_utilisation(taskset, {1,2,5})) <= ((0.9 - (max_wcet(taskset, {5})/(5.0*2.0))) + ((cumulative_utilisation(taskset, {1})/10.0)))
    cond_5 = (max_wcet(taskset, {10,20,50,100,200,1000})/5.0 + cumulative_utilisation(taskset, {1,2,5})) <= max((1-0.2*(cumulative_utilisation(taskset, {2}))), (0.8 + 0.2*(cumulative_utilisation(taskset, {1,2}))))
    #if (cond_5 == False):
        #print 5
        #print max_wcet(taskset, {5,10,20,50,100,200,1000})/2.0 
    #cond_50 = (max_wcet(taskset, {100,200,1000})/50.0 + cumulative_utilisation(taskset, {1,2,5,10,20,50})) <= (0.9 - ((max_wcet(taskset, {50})/(50.0*2.0))) + ((cumulative_utilisation(taskset, {1,2,5,10})/10.0)))
    cond_50 = (max_wcet(taskset, {100,200,1000})/50.0 + cumulative_utilisation(taskset, {1,2,5,10,20,50})) <= max((1-0.2*cumulative_utilisation(taskset, {20})), (0.8 + 0.2*(cumulative_utilisation(taskset, {1,2,5,10,20}))))
    #cond_50 = (max_wcet({100,200,1000})/50.0 + cumulative_utilisation(taskset, {1,2,5,10,20,50})) <= (0.9 - cumulative_utilisation(taskset, {50})/2.0 + cumulative_utilisation(taskset, {1,2,5,10})/10.0)
    
    if (cond_1 and cond_2 and cond_5 and cond_10 and cond_20 and cond_50 and cond_100 and cond_200 and cond_1000):
        return True
    else:
        return False

def schedulable_np_fixed(taskset, blocking_time):
#     if not taskset:
#         return False
    
    #cond_1 = ((blocking_time)/1.0 + cumulative_utilisation(taskset, {1})) <= 1
    cond_1 = (min(max_wcet(taskset, {2,5,10,20,50,100,200,1000}),blocking_time)/1.0 + cumulative_utilisation(taskset, {1})) <= 1
#    if (cond_1 == False):
#        print 1
#         print max_wcet(taskset, {2,5,10,20,50,100,200,1000})/1.0
    #cond_2 = ((blocking_time)/2.0 + cumulative_utilisation(taskset, {1,2})) <= 1
    cond_2 = (min(max_wcet(taskset, {5,10,20,50,100,200,1000}),blocking_time)/2.0 + cumulative_utilisation(taskset, {1,2})) <= 1
#    if (cond_2 == False):
#        print 2
#        print max_wcet(taskset, {5,10,20,50,100,200,1000})/2.0
    #cond_10 = ((blocking_time)/10.0 + cumulative_utilisation(taskset, {1,2,5,10})) <= 1
    cond_10 = (min(max_wcet(taskset, {20,50,100,200,1000}),blocking_time)/10.0 + cumulative_utilisation(taskset, {1,2,5,10})) <= 1
    #cond_20 = ((blocking_time)/20.0 + cumulative_utilisation(taskset, {1,2,5,10,20})) <= 1
    cond_20 = (min(max_wcet(taskset, {50,100,200,1000}),blocking_time)/20.0 + cumulative_utilisation(taskset, {1,2,5,10,20})) <= 1
    #cond_100 = ((blocking_time)/100.0 + cumulative_utilisation(taskset, {1,2,5,10,20,50,100})) <= 1
    cond_100 = (min(max_wcet(taskset, {200,1000}),blocking_time)/100.0 + cumulative_utilisation(taskset, {1,2,5,10,20,50,100})) <= 1
    #cond_200 = ((blocking_time)/200.0 + cumulative_utilisation(taskset, {1,2,5,10,20,50,100,200})) <= 1
    cond_200 = (min(max_wcet(taskset, {1000}),blocking_time)/200.0 + cumulative_utilisation(taskset, {1,2,5,10,20,50,100,200})) <= 1
    cond_1000 = (cumulative_utilisation(taskset, {1,2,5,10,20,50,100,200,1000})) <= 1
    #cond_5 = ((blocking_time)/5.0 + cumulative_utilisation(taskset, {1,2,5})) <= ((0.9 - (max_wcet(taskset, {5})/(5.0*2.0))) + ((cumulative_utilisation(taskset, {1})/10.0)))
    #cond_5 = ((blocking_time)/5.0 + cumulative_utilisation(taskset, {1,2,5})) <= max((1-0.2*(cumulative_utilisation(taskset, {2}))), (0.8 + 0.2*(cumulative_utilisation(taskset, {1,2}))))
    cond_5 = (min(max_wcet(taskset, {10,20,50,100,200,1000}),blocking_time)/5.0 + cumulative_utilisation(taskset, {1,2,5})) <= max((1-0.2*(cumulative_utilisation(taskset, {2}))), (0.8 + 0.2*(cumulative_utilisation(taskset, {1,2}))))
    #if (cond_5 == False):
        #print 5
        #print max_wcet(taskset, {5,10,20,50,100,200,1000})/2.0 
    #cond_50 = ((blocking_time)/50.0 + cumulative_utilisation(taskset, {1,2,5,10,20,50})) <= (0.9 - ((max_wcet(taskset, {50})/(50.0*2.0))) + ((cumulative_utilisation(taskset, {1,2,5,10})/10.0)))
    #cond_50 = ((blocking_time)/50.0 + cumulative_utilisation(taskset, {1,2,5,10,20,50})) <= max((1-0.2*cumulative_utilisation(taskset, {20})), (0.8 + 0.2*(cumulative_utilisation(taskset, {1,2,5,10,20}))))
    cond_50 = (min(max_wcet(taskset, {100,200,1000}),blocking_time)/50.0 + cumulative_utilisation(taskset, {1,2,5,10,20,50})) <= max((1-0.2*cumulative_utilisation(taskset, {20})), (0.8 + 0.2*(cumulative_utilisation(taskset, {1,2,5,10,20}))))
    #cond_50 = (max_wcet({100,200,1000})/50.0 + cumulative_utilisation(taskset, {1,2,5,10,20,50})) <= (0.9 - cumulative_utilisation(taskset, {50})/2.0 + cumulative_utilisation(taskset, {1,2,5,10})/10.0)
    
    if (cond_1 and cond_2 and cond_5 and cond_10 and cond_20 and cond_50 and cond_100 and cond_200 and cond_1000):
        return True
    else:
        return False


def schedulable_angle_taskset(taskset):
#     if not taskset:
#         return False
     
    cond_1 = ((cumulative_execution(taskset, {0.5}) + cumulative_utilisation(taskset, {0.5,1})) <= 1)
    #print cumulative_execution(taskset, {0.5})
    #print cond_1
    cond_2 = ((cumulative_execution(taskset, {0.5})/2.0 + cumulative_utilisation(taskset, {0.5,1,2})) <= 1)
    #print cond_2
    cond_10 = ((cumulative_execution(taskset, {0.5})/10.0 + cumulative_utilisation(taskset, {0.5,1,2,5,10})) <= 1)
    #print cond_10
    cond_20 = ((cumulative_execution(taskset, {0.5})/20.0 + cumulative_utilisation(taskset, {0.5,1,2,5,10,20})) <= 1)
    #print cond_20
    cond_100 = ((cumulative_execution(taskset, {0.5})/100.0 + cumulative_utilisation(taskset, {0.5,1,2,5,10,20,50,100})) <= 1)
    #print cond_100
    cond_200 = ((cumulative_execution(taskset, {0.5})/200.0 + cumulative_utilisation(taskset, {0.5,1,2,5,10,20,50,100,200})) <= 1)
    #print cond_200
    cond_1000 = ((cumulative_execution(taskset, {0.5})/1000.0 + cumulative_utilisation(taskset, {0.5,1,2,5,10,20,50,100,200,1000})) <= 1)
    #print cond_1000
    cond_0 = ((cumulative_utilisation(taskset, {0.5}) + cumulative_execution(taskset, {0.5})  <= 1))
    #print cond_0
    cond_5 = ((cumulative_utilisation(taskset, {1,2,5}) + cumulative_execution(taskset, {0.5})/5.0) <= max(1-0.2*(cumulative_utilisation(taskset, {2})), 0.8 + 0.2*(cumulative_utilisation(taskset, {1,2}))))
    #print cond_5
    cond_50 = (cumulative_utilisation(taskset, {0.5,1,2,5,10,20,50}) + cumulative_execution(taskset, {0.5})/50.0 <= max(1-0.2*cumulative_utilisation(taskset, {20}), 0.8 + 0.2*(cumulative_utilisation(taskset, {1,2,5,10,20}))))
    #print cond_50 
    if (cond_0 and cond_1 and cond_2 and cond_5 and cond_10 and cond_20 and cond_50 and cond_100 and cond_200 and cond_1000):
    #if (cond_1):
        return True
    else:
        return False
    
def schedulable_angle_taskset_less_pessimistic(taskset):
#     if not taskset:
#         return False
     
    cond_1 = ((cumulative_execution(taskset, {0.5})/1.0 + cumulative_utilisation(taskset, {1})) <= 1)
    #print cumulative_execution(taskset, {0.5})
    #print cond_1
    cond_2 = ((cumulative_execution(taskset, {0.5})/2.0 + cumulative_utilisation(taskset, {1,2})) <= 1)
    #print cond_2
    cond_10 = ((cumulative_execution(taskset, {0.5})/10.0 + cumulative_utilisation(taskset, {0.5,1,2,5,10})) <= 1)
    #print cond_10
    cond_20 = ((cumulative_execution(taskset, {0.5})/20.0 + cumulative_utilisation(taskset, {0.5,1,2,5,10,20})) <= 1)
    #print cond_20
    cond_100 = ((cumulative_execution(taskset, {0.5})/100.0 + cumulative_utilisation(taskset, {0.5,1,2,5,10,20,50,100})) <= 1)
    #print cond_100
    cond_200 = ((cumulative_execution(taskset, {0.5})/200.0 + cumulative_utilisation(taskset, {0.5,1,2,5,10,20,50,100,200})) <= 1)
    #print cond_200
    cond_1000 = ((cumulative_execution(taskset, {0.5})/1000.0 + cumulative_utilisation(taskset, {0.5,1,2,5,10,20,50,100,200,1000})) <= 1)
    #print cond_1000
    cond_0 = ((cumulative_utilisation(taskset, {0.5}) + cumulative_execution(taskset, {0.5})  <= 1))
    #print cond_0
    cond_5 = ((cumulative_utilisation(taskset, {1,2,5}) + cumulative_execution(taskset, {0.5})/5.0) <= max(1-0.2*(cumulative_utilisation(taskset, {2})), 0.8 + 0.2*(cumulative_utilisation(taskset, {1,2}))))
    #print cond_5
    cond_50 = (cumulative_utilisation(taskset, {0.5,1,2,5,10,20,50}) + cumulative_execution(taskset, {0.5})/50.0 <= max(1-0.2*cumulative_utilisation(taskset, {20}), 0.8 + 0.2*(cumulative_utilisation(taskset, {1,2,5,10,20}))))
    #print cond_50 
    if (cond_0 and cond_1 and cond_2 and cond_5 and cond_10 and cond_20 and cond_50 and cond_100 and cond_200 and cond_1000):
    #if (cond_1):
        return True
    else:
        return False
    
    
def schedulable_angle_taskset_period(taskset):
#     if not taskset:
#         return False
     
    cond_1 = (cumulative_utilisation(taskset, {1}) <= 1)
    #print cumulative_execution(taskset, {0.5})
    #print cond_1
    cond_2 = (cumulative_utilisation(taskset, {1,2}) <= 1)
    #print cond_2
    cond_10 = ((cumulative_execution(taskset, {0.5})/10.0 + cumulative_utilisation(taskset, {0.5,1,2,5,10})) <= 1)
    #print cond_10
    cond_20 = ((cumulative_execution(taskset, {0.5})/20.0 + cumulative_utilisation(taskset, {0.5,1,2,5,10,20})) <= 1)
    #print cond_20
    cond_100 = ((cumulative_execution(taskset, {0.5})/100.0 + cumulative_utilisation(taskset, {0.5,1,2,5,10,20,50,100})) <= 1)
    #print cond_100
    cond_200 = ((cumulative_execution(taskset, {0.5})/200.0 + cumulative_utilisation(taskset, {0.5,1,2,5,10,20,50,100,200})) <= 1)
    #print cond_200
    cond_1000 = ((cumulative_execution(taskset, {0.5})/1000.0 + cumulative_utilisation(taskset, {0.5,1,2,5,10,20,50,100,200,1000})) <= 1)
    #print cond_1000
    cond_0 = ((cumulative_utilisation(taskset, {0.5}) + cumulative_execution(taskset, {0.5})  <= 1))
    #print cond_0
    cond_5 = ((cumulative_utilisation(taskset, {1,2,5}) + cumulative_execution(taskset, {0.5})/5.0) <= max(1-0.2*(cumulative_utilisation(taskset, {2})), 0.8 + 0.2*(cumulative_utilisation(taskset, {1,2}))))
    #print cond_5
    cond_50 = (cumulative_utilisation(taskset, {0.5,1,2,5,10,20,50}) + cumulative_execution(taskset, {0.5})/50.0 <= max(1-0.2*cumulative_utilisation(taskset, {20}), 0.8 + 0.2*(cumulative_utilisation(taskset, {1,2,5,10,20}))))
    #print cond_50 
    if (cond_0 and cond_1 and cond_2 and cond_5 and cond_10 and cond_20 and cond_50 and cond_100 and cond_200 and cond_1000):
    #if (cond_1):
        return True
    else:
        return False
    
        
def schedulable_np_angle_taskset(taskset):
#     if not taskset:
#         return False
    
    cond_1 = ((max_wcet(taskset, {2,5,10,20,50,100,200,1000})/1.0 + cumulative_execution(taskset, {0.5})/1.0 + cumulative_utilisation(taskset, {0.5, 1})) <= 1)
    cond_2 = ((max_wcet(taskset, {5,10,20,50,100,200,1000})/2.0 + cumulative_execution(taskset, {0.5})/2.0 + cumulative_utilisation(taskset, {0.5, 1,2})) <= 1)
    cond_10 = ((max_wcet(taskset, {20,50,100,200,1000})/10.0 + cumulative_execution(taskset, {0.5})/10.0 + cumulative_utilisation(taskset, {0.5, 1,2,5,10})) <= 1)
    cond_20 = ((max_wcet(taskset, {50,100,200,1000})/20.0 + cumulative_execution(taskset, {0.5})/20.0 + cumulative_utilisation(taskset, {0.5, 1,2,5,10,20})) <= 1)
    cond_100 = ((max_wcet(taskset, {200,1000})/100.0 + cumulative_execution(taskset, {0.5})/100.0 + cumulative_utilisation(taskset, {0.5, 1,2,5,10,20,50,100})) <= 1)
    cond_200 = ((max_wcet(taskset, {1000})/200.0 + cumulative_execution(taskset, {0.5})/200.0 + cumulative_utilisation(taskset, {0.5, 1,2,5,10,20,50,100,200})) <= 1)
    cond_1000 = ((cumulative_execution(taskset, {0.5})/1000.0 + cumulative_utilisation(taskset, {0.5, 1,2,5,10,20,50,100,200,1000})) <= 1)
    cond_0 = ((cumulative_utilisation(taskset, {0.5}) + cumulative_execution(taskset, {0.5})  <= 1))
    cond_5 = ((max_wcet(taskset, {10,20,50,100,200,1000})/5.0 + cumulative_utilisation(taskset, {1,2,5}) + cumulative_execution(taskset, {0.5}))/5.0 <= max(1-0.2*(cumulative_utilisation(taskset, {2})), 0.8 + 0.2*(cumulative_utilisation(taskset, {1,2}))))
    cond_50 = ((max_wcet(taskset, {100,200,1000})/50.0 + cumulative_utilisation(taskset, {1,2,5,10,20,50}) + cumulative_execution(taskset, {0.5})/50.0 <= max(1-0.2*cumulative_utilisation(taskset, {20}), 0.8 + 0.2*(cumulative_utilisation(taskset, {1,2,5,10,20}))))) 
    if (cond_0 and cond_1 and cond_2 and cond_5 and cond_10 and cond_20 and cond_50 and cond_100 and cond_200 and cond_1000):
        return True
    else:
        return False

def schedulable_angle_task(task, taskset, angle):
    c_angle_max_sum = sum(map(lambda x:x['execution'],angle))
    u_angle_sum = sum(map(lambda x:float(x['execution'])/x['period'], angle))
    
    if task['period'] in [1,2,10,20,100,200,1000]:
        angle_workload =  u_angle_sum + (1.0/task['period'])*c_angle_max_sum
        task_demand = cumulative_utilisation(taskset,set(filter(lambda x : x <= task['period'], [1,2,5,10,20,50,100,200,1000])))
        return  (task_demand + angle_workload <= 1)
            
    if task['period'] == 5:
        angle_workload =  u_angle_sum + 0.2 * c_angle_max_sum
        task_demand = cumulative_utilisation(taskset,{1,2,5})
        return (task_demand + angle_workload <= 0.9 + 0.1*cumulative_utilisation(taskset,{1}))
            
    if task['period'] == 50:
        angle_workload =  u_angle_sum + 0.02 * c_angle_max_sum
        task_demand = cumulative_utilisation(taskset,{1,2,5,10,20,50})
        return (task_demand + angle_workload <= 0.9 + 0.1*cumulative_utilisation(taskset,{1,2,5,10}))


def schedulable_angle(taskset, angle):
    for task in taskset:
        if schedulable_angle_task(task, taskset, angle) is False:
            return False
    return True

def main():
    args = sys.argv
    test_name = str(args[1])
    tasksets_amount = int(args[2])

    dist_periods_profiles = {
        "P1" : [0.18, 0.02, 0.02, 0.25, 0.25, 0.03, 0.2, 0.01, 0.04],
        "P2" : [0.03, 0.17, 0.02, 0.25, 0.25, 0.03, 0.2, 0.01, 0.04],
        "P3" : [0.03, 0.02, 0.17, 0.25, 0.25, 0.03, 0.2, 0.01, 0.04],
        "P4" : [0.03, 0.02, 0.02, 0.40, 0.25, 0.03, 0.2, 0.01, 0.04],
        "P5" : [0.03, 0.02, 0.02, 0.25, 0.40, 0.03, 0.2, 0.01, 0.04],
        "P6" : [0.03, 0.02, 0.02, 0.25, 0.25, 0.18, 0.2, 0.01, 0.04],
        "P7" : [0.03, 0.02, 0.02, 0.25, 0.25, 0.03, 0.35, 0.01, 0.04],
        "P8" : [0.03, 0.02, 0.02, 0.25, 0.25, 0.03, 0.2, 0.16, 0.04],
        "P9" : [0.03, 0.02, 0.02, 0.25, 0.25, 0.03, 0.2, 0.01, 0.19],
        "P10" : [0.0466, 0.0366, 0.0366, 0.2666, 0.2666, 0.0466, 0.21660000000000001, 0.0266, 0.0566]
    }
    
    for profile_name, profile in dist_periods_profiles.items():
        print 'Running ' + str(profile_name)
        tasksets = [autogen.generate_taskset(runnable_min = 600, runnable_max = 800, max_trials = 10, period_pdf = profile) for n in range(tasksets_amount)]
        np.save (str(test_name)+'_'+str(profile_name), tasksets)

def plot(filenames = [], savename = 'automotive'):

    figlabel = itertools.cycle(('a','b','c','d','e','f','g','h','i'))
    marker = itertools.cycle(('+', 'v','*','D','x','+'))
    colors = itertools.cycle(('g','r','b','g','r','y','y','b'))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax = fig.add_subplot(111)
    fig.subplots_adjust (top = 0.9, left = 0.1, right = 0.95, hspace = 0.3)
    ax.set_xlabel('T100 + T200 + T1000 Utilization (\%)',size=10)
    ax.set_ylabel('T1 Utilization (\%)',size=10)
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.tick_params(labelcolor = 'w', top = 'off', bottom = 'off', left = 'off', right = 'off')
    ax.axis([0,10,0,100])

    for bound in np.arange(93, 100, 2.5):
        x = np.arange(11)
        y = 10*(bound-90) - 10*x
        ax.plot(x, y, '--', color = colors.next(), marker = '+', markersize = 1, markevery = 1, fillstyle = 'full', label = '', linewidth = 1)
        plt.text(bound-90, 6, str(bound) + '%', rotation=-45)
    
    for filename in filenames:
        tasksets = np.load(str(filename))
        x = []
        y = []
        for taskset in tasksets:
            x.append(z_util(taskset)*100)
            y.append(y_util(taskset)*100)
        ax.plot(x, y, '-', color = colors.next(), marker = marker.next(), markersize = 8, markevery = 1, fillstyle = 'none', label = '', linewidth = 0)
    
    ax.tick_params(labelcolor='k', top='off', bottom='off', left='off', right='off')
        
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(10)
        
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(10)    
    
    ax.grid()
    plt.legend()
    plt.show()

    pp = PdfPages (str(savename)+'.pdf')
    pp.savefig(fig)
    pp.close()

if __name__ == "__main__":
    main()
