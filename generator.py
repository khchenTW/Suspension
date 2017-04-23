from __future__ import division
from scipy import stats
import numpy as np
import random
from scipy.stats import exponweib
import math
import analysis
import sys, getopt
import json

ofile = "taskset-p.txt"
USet=[]
class task (dict):
    def __init__(self, execution, period, deadline, suspension):
        dict.__setitem__(self, "execution", float (execution))
        dict.__setitem__(self, "period", float (period))
        dict.__setitem__(self, "deadline", float (deadline))
        dict.__setitem__(self, "suspension", float (suspension))

def UUniFast(n,U_avg):
    global USet
    sumU=U_avg
    for i in range(n-1):
        nextSumU=sumU*math.pow(random.random(), 1/(n-i))
        USet.append(sumU-nextSumU)
        sumU=nextSumU
    USet.append(sumU)

def UniDist(n,U_min,U_max):
	for i in range(n-1):
	    uBkt=random.uniform(U_min, U_max)
	    USet.append(uBkt)

def CSet_generate(Pmin,numLog, p, sstype=0):
	global USet,PSet
	j=0
        # the number of SSS
        x = len(USet) * p
	for i in USet:
	    thN=j%numLog
	    p=random.uniform(Pmin*math.pow(10, thN), Pmin*math.pow(10, thN+1))
            if x != 0:
                if sstype == 0:
                    suspension = random.uniform(0.01*(p-i*p), 0.1*(p-i*p))
                elif sstype == 1:
                    suspension = random.uniform(0.1*(p-i*p), 0.6*(p-i*p))
                else:
                    suspension = random.uniform(0.6*(p-i*p), (p-i*p))
                x-=1
            else:
                suspension = 0
            PSet.append(task(i*p, p, p, suspension))
	    j=j+1;

def init():
	global USet,PSet
	USet=[]
	PSet=[]

def taskGeneration(numTasks, uTotal, sstype, propotion):
    random.seed()
    init()
    UUniFast(numTasks,uTotal/100)
    CSet_generate(1,2, propotion, sstype)
    fo = open(ofile, "wb")
    print >>fo, json.dumps(PSet)
    return PSet



def draw_runnables_per_tasks():
    dist = stats.rv_discrete(name='runnables per task', values = ([2, 3, 4, 5], [0.3, 0.4, 0.2, 0.1]))
    return int(dist.rvs(size=1))

# For a given amount of runnables, the mapping of runnables to
# tasks is randomized.
# Returns the amount of runnables per task i.e [2,3,4,5]
# implies task 1 contains 2 runnables, task 2 contains 3 runnables etc.

def runnables_per_tasks(runnables):
    partitions = []
    n = runnables

    # O(|runnables|)
    while True:
        if n == 0 or n == 1:
            #raise ValueError("At leat two runnables required for useful mapping")
            return partitions

        if n == 2:
            partitions = partitions + [2]
            return partitions

        if n == 3:
            partitions = partitions + [3]
            return partitions

        if n == 4:
            dist = stats.rv_discrete(name='n=4', values = ([22, 4], [float(9)/29, float(20)/29]))
            sample = int(dist.rvs(size=1))
            if sample == 22:
                partitions = partitions + [2, 2]
            else:
                partitions = partitions + [4]
            return partitions

        if n == 5:
            dist = stats.rv_discrete(name='n=5', values = ([23, 5], [float(12)/22, float(10)/22]))
            sample = int(dist.rvs(size=1))
            if sample == 23:
                partitions = partitions + [2, 3]
            else:
                partitions = partitions + [5]
            return partitions

        if n == 6:
            dist = stats.rv_discrete(name='n=6', values = ([33, 24], [float(16)/100, float(6)/100]))
            sample = int(dist.rvs(size=1))
            if sample == 33:
                partitions = partitions + [3, 3]
            else:
                partitions = partitions + [2, 4]
            return partitions

        dist = stats.rv_discrete(name='runnables per task', values = ([2, 3, 4, 5], [0.3, 0.4, 0.2, 0.1]))
        sample = int(dist.rvs(size=1))
        partitions = partitions + [sample]
        n = n - sample

def sample_runnable_acet(period, amount = 1, scalingFlag=True):
    # acet for angle synchronous modeled as sporadic task with T_min = 5ms
    if period == 'angle':
        scaling = np.random.uniform(1.2, 28.17, amount)
        dist = exponweib(1, 1.02354320004197374, loc=0, scale=1.0/0.1519099030)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.34 or samples[i] > 30.11:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
               continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    # Parameters fitted with data from WATERS 'Real World Automotive Benchmarks For Free'
    if period == 1:
        scaling = np.random.uniform(1.3, 29.11, amount)
        dist = exponweib(1, 1.044, loc=0, scale=1.0/0.214)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.34 or samples[i] > 30.11:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
               continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 2:
        scaling = np.random.uniform(1.54, 19.04, amount)
        dist = exponweib(1, 1.0607440083, loc=0, scale=1.0/0.2479463059)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.32 or samples[i] > 40.69:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
               continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 5:
        scaling = np.random.uniform(1.13, 18.44, amount)
        dist = exponweib(1, 1.00818633, loc=0, scale=1.0/0.09)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.36 or samples[i] > 83.38:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
               continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 10:
        scaling = np.random.uniform(1.06, 30.03, amount)
        dist = exponweib(1, 1.0098, loc=0, scale=1.0/0.0985)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.21 or samples[i] > 309.87:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
               continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 20:
        scaling = np.random.uniform(1.06, 15.61, amount)
        dist = exponweib(1, 1.01309699673984310, loc=0, scale=1.0/0.1138186679)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.25 or samples[i] > 291.42:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
               continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 50:
        scaling = np.random.uniform(1.13, 7.76, amount)
        dist = exponweib(1, 1.00324219159296302, loc=0, scale=1.0/0.05685450460)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.29 or samples[i] > 92.98:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
               continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 100:
        scaling = np.random.uniform(1.02, 8.88, amount)
        dist = exponweib(1, 1.00900736028318527, loc=0, scale=1.0/0.09448019812)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.21 or samples[i] > 420.43:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
               continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 200:
        scaling = np.random.uniform(1.03, 4.9, amount)
        dist = exponweib(1, 1.15710612360723798, loc=0, scale=1.0/0.3706045664)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.22 or samples[i] > 21.95:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
               continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 1000:
        scaling = np.random.uniform(1.84, 4.75, amount)
        if scalingFlag:
            return list(0.001 * np.random.uniform(0.37, 0.46, amount) *scaling)
        else:
            return list(0.001 * np.random.uniform(0.37, 0.46, amount))


def is_valid(taskset, util_max):
    util = 0.0
    for task in taskset:
        util += task['execution']/task['period']
    if util > util_max:
        return False
    return True



def generate_angle_workload(util, cylinder = 4, mode = 'sporadic'):
    util = round(util, 3)
    if mode == 'sporadic':
        # priod in ms
        period = float(120)/(6000*cylinder) * 1000
        while True:
            load = []
            util_current = 0
            last_util = 0
            while util_current <= util:
                execution = sum(sample_runnable_acet('angle', 1))
                load.append(task(execution, period, period))
                util_current += float(execution)/period
                last_util = float(execution)/period
            if round(util_current,3) == util:
                return load
            else:
                continue

    if mode == 'arrival':
        while True:
            load = []
            util_current = 0
            last_util = 0
            while util_current <= util:
                execution = sum(sample_runnable_acet('angle', 1))
                period = float(120)/(500*cylinder)*1000
                load.append(task(execution, period, period))
                util_current += float(execution)/period
                last_util = float(execution)/period
            if round(util_current,3) == util:
                return load
            else:
                continue


def generate_util_fixed(util, period_pdf = [0.18, 0.02, 0.02, 0.25, 0.25, 0.03, 0.2, 0.01, 0.04], scalingFlag=True):
    util = round(util, 3)
    while True:
        util_current = 0
        num_runnables = 0
        periods_dist = stats.rv_discrete(name='periods', values = ([1,2,5,10,20,50,100,200,1000], period_pdf))
        run_dist = stats.rv_discrete(name='runnables per task', values = ([2, 3, 4, 5], [0.3, 0.4, 0.2, 0.1]))
        taskset = []
        last_util = 0
        while util_current <= util:
            period = int(periods_dist.rvs(size=1))
            #runnables = int(run_dist.rvs(size=1))
            #1 task = 1 runnable for now
            runnables = 1
            num_runnables += runnables
            execution = sum(sample_runnable_acet(period, runnables, scalingFlag))
            #temporary use execution generator as suspension
            suspension = sum(sample_runnable_acet(period, runnables, scalingFlag))
            taskset.append(task(execution, period, period, suspension))
            util_current += float(execution/period)
            last_util = float(execution/period)
        #print round(util_current,3)
        if round(util_current,3) == util:
            print num_runnables
            return taskset
        else:
            continue


def generate_taskset(util_max = 1.0, runnable_min = 600, runnable_max = 800, max_trials = 1, period_pdf = [0.18, 0.02, 0.02, 0.25, 0.25, 0.03, 0.2, 0.01, 0.04]):
    trials = 0
    while True:
        trials += 1
        taskset = []
        dist = stats.rv_discrete(name='periods', values = ([1,2,5,10,20,50,100,200,1000], period_pdf))
        runnables = int(np.random.uniform(runnable_min, runnable_max))

        sys_runnable_periods = dist.rvs(size=runnables)

        sys_runnables_period_0001_amount = 0
        sys_runnables_period_0002_amount = 0
        sys_runnables_period_0005_amount = 0
        sys_runnables_period_0010_amount = 0
        sys_runnables_period_0020_amount = 0
        sys_runnables_period_0050_amount = 0
        sys_runnables_period_0100_amount = 0
        sys_runnables_period_0200_amount = 0
        sys_runnables_period_1000_amount = 0

        for period in sys_runnable_periods:
            if period == 1:
                sys_runnables_period_0001_amount += 1
            if period == 2:
                sys_runnables_period_0002_amount += 1
            if period == 5:
                sys_runnables_period_0005_amount += 1
            if period == 10:
                sys_runnables_period_0010_amount += 1
            if period == 20:
                sys_runnables_period_0020_amount += 1
            if period == 50:
                sys_runnables_period_0050_amount += 1
            if period == 100:
                sys_runnables_period_0100_amount += 1
            if period == 200:
                sys_runnables_period_0200_amount += 1
            if period == 1000:
                sys_runnables_period_1000_amount += 1

        # build tasks from runnables (PERIOD = 1)
        amounts = runnables_per_tasks(sys_runnables_period_0001_amount)
        for amount in amounts:
            # C_i = sum of acet(runnable), runnable assigned to task i

            taskset.append(task(sum(sample_runnable_acet(1, amount)), 1, 1))

        # build tasks from runnables (PERIOD = 2)
        amounts = runnables_per_tasks(sys_runnables_period_0002_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(2, amount)), 2, 2))

            # build tasks from runnables (PERIOD = 5)
        amounts = runnables_per_tasks(sys_runnables_period_0005_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(5, amount)), 5, 5))

            # build tasks from runnables (PERIOD = 10)
        amounts = runnables_per_tasks(sys_runnables_period_0010_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(10, amount)), 10, 10))

            # build tasks from runnables (PERIOD = 20)
        amounts = runnables_per_tasks(sys_runnables_period_0020_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(20, amount)), 20, 20))

            # build tasks from runnables (PERIOD = 50)
        amounts = runnables_per_tasks(sys_runnables_period_0050_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(50, amount)), 50, 50))

            # build tasks from runnables (PERIOD = 100)
        amounts = runnables_per_tasks(sys_runnables_period_0100_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(100, amount)), 100, 100))

            # build tasks from runnables (PERIOD = 200)
        amounts = runnables_per_tasks(sys_runnables_period_0200_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(200, amount)), 200, 200))

            # build tasks from runnables (PERIOD = 1000)
        amounts = runnables_per_tasks(sys_runnables_period_1000_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(1000, amount)), 1000, 1000))

        if is_valid(taskset, util_max):
            return taskset
        else:
            #if trials >= max_trials:
                #raise ValueError("amount of runnables is inappropriate for given max utilization")
            #continue
            return taskset

def generate_taskset_util(util_max = 1.0, period_pdf = [0.03, 0.02, 0.02, 0.25, 0.40, 0.03, 0.2, 0.01, 0.04], scalingFlag = False, threshold = 0.1):
    max_trials = 1
    #trials = 0
    while True:
        #trials += 1
        taskset = []
        dist = stats.rv_discrete(name='periods', values = ([1,2,5,10,20,50,100,200,1000], period_pdf))
        runnables = 1800.0

        sys_runnable_periods = dist.rvs(size=runnables)

        sys_runnables_period_0001_amount = 0
        sys_runnables_period_0002_amount = 0
        sys_runnables_period_0005_amount = 0
        sys_runnables_period_0010_amount = 0
        sys_runnables_period_0020_amount = 0
        sys_runnables_period_0050_amount = 0
        sys_runnables_period_0100_amount = 0
        sys_runnables_period_0200_amount = 0
        sys_runnables_period_1000_amount = 0

        for period in sys_runnable_periods:
            if period == 1:
                sys_runnables_period_0001_amount += 1
            if period == 2:
                sys_runnables_period_0002_amount += 1
            if period == 5:
                sys_runnables_period_0005_amount += 1
            if period == 10:
                sys_runnables_period_0010_amount += 1
            if period == 20:
                sys_runnables_period_0020_amount += 1
            if period == 50:
                sys_runnables_period_0050_amount += 1
            if period == 100:
                sys_runnables_period_0100_amount += 1
            if period == 200:
                sys_runnables_period_0200_amount += 1
            if period == 1000:
                sys_runnables_period_1000_amount += 1

        # build tasks from runnables (PERIOD = 1)
        amounts = runnables_per_tasks(sys_runnables_period_0001_amount)
        for amount in amounts:
            # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(1, amount, scalingFlag)), 1, 1))


        # build tasks from runnables (PERIOD = 2)
        amounts = runnables_per_tasks(sys_runnables_period_0002_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(2, amount, scalingFlag)), 2, 2))

            # build tasks from runnables (PERIOD = 5)
        amounts = runnables_per_tasks(sys_runnables_period_0005_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(5, amount, scalingFlag)), 5, 5))

            # build tasks from runnables (PERIOD = 10)
        amounts = runnables_per_tasks(sys_runnables_period_0010_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(10, amount, scalingFlag)), 10, 10))

            # build tasks from runnables (PERIOD = 20)
        amounts = runnables_per_tasks(sys_runnables_period_0020_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(20, amount, scalingFlag)), 20, 20))

            # build tasks from runnables (PERIOD = 50)
        amounts = runnables_per_tasks(sys_runnables_period_0050_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(50, amount, scalingFlag)), 50, 50))

            # build tasks from runnables (PERIOD = 100)
        amounts = runnables_per_tasks(sys_runnables_period_0100_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(100, amount, scalingFlag)), 100, 100))

            # build tasks from runnables (PERIOD = 200)
        amounts = runnables_per_tasks(sys_runnables_period_0200_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(200, amount, scalingFlag)), 200, 200))

            # build tasks from runnables (PERIOD = 1000)
        amounts = runnables_per_tasks(sys_runnables_period_1000_amount)
        for amount in amounts:
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(sum(sample_runnable_acet(1000, amount, scalingFlag)), 1000, 1000))


        random.shuffle(taskset)


        util = 0.0
        i = 0
        for tasks in taskset:
            util += tasks['execution']/tasks['period']
            i = i + 1
            if util > util_max:
                break

        if(util <= util_max + threshold):
            taskset = taskset[:i]
        else:
            i = i - 1
            initialSet = taskset[:i]
            remainingTasks = taskset[i:]
            tasks = remainingTasks[0]
            util -= tasks['execution']/tasks['period']
            while (util < util_max):
                tasks = remainingTasks[0]
                if (util + tasks['execution']/tasks['period'] <= util_max + threshold):
                    util += tasks['execution']/tasks['period']
                    initialSet.append(tasks)
                remainingTasks = remainingTasks[1:]
            taskset = initialSet
        print util
        return taskset

def generate_taskset_util_number(number_of_sets = 100, util_max = 1.0, period_pdf = [0.03, 0.02, 0.02, 0.25, 0.40, 0.03, 0.2, 0.01, 0.04], scalingFlag = False, threshold = 0.1, angle = False, cylinder = 4, mode = 'sporadic'):
    max_trials = 1
    #trials = 0
    while True:
        #trials += 1
        taskset = []
        angle_period = float(120.0)/(6000.0*cylinder) * 1000.0
        #print angle_period
        if (angle == False):
            dist = stats.rv_discrete(name='periods', values = ([1,2,5,10,20,50,100,200,1000], period_pdf))
        else:
            dist = stats.rv_discrete(name='periods', values = ([1,2,5,10,20,50,100,200,1000,2000], period_pdf))
        runnables = (3000*number_of_sets)



        sys_runnable_periods = dist.rvs(size=runnables)

        sys_runnables_period_0001_amount = 0
        sys_runnables_period_0002_amount = 0
        sys_runnables_period_0005_amount = 0
        sys_runnables_period_0010_amount = 0
        sys_runnables_period_0020_amount = 0
        sys_runnables_period_0050_amount = 0
        sys_runnables_period_0100_amount = 0
        sys_runnables_period_0200_amount = 0
        sys_runnables_period_1000_amount = 0
        sys_runnables_period_angle_amount = 0

        for period in sys_runnable_periods:
            if period == 1:
                sys_runnables_period_0001_amount += 1
            elif period == 2:
                sys_runnables_period_0002_amount += 1
            elif period == 5:
                sys_runnables_period_0005_amount += 1
            elif period == 10:
                sys_runnables_period_0010_amount += 1
            elif period == 20:
                sys_runnables_period_0020_amount += 1
            elif period == 50:
                sys_runnables_period_0050_amount += 1
            elif period == 100:
                sys_runnables_period_0100_amount += 1
            elif period == 200:
                sys_runnables_period_0200_amount += 1
            elif period == 1000:
                sys_runnables_period_1000_amount += 1
            else:
                sys_runnables_period_angle_amount += 1

#         print period_pdf
#
#         print '    1: ' + str(sys_runnables_period_0001_amount) + ' ' +  str(sys_runnables_period_0001_amount*100.0/runnables)
#         print '    2: ' +str(sys_runnables_period_0002_amount) + ' ' +  str(sys_runnables_period_0002_amount*100.0/runnables)
#         print '    5: ' +str(sys_runnables_period_0005_amount) + ' ' +  str(sys_runnables_period_0005_amount*100.0/runnables)
#         print '   10: ' +str(sys_runnables_period_0010_amount) + ' ' +  str(sys_runnables_period_0010_amount*100.0/runnables)
#         print '   20: ' +str(sys_runnables_period_0020_amount) + ' ' +  str(sys_runnables_period_0020_amount*100.0/runnables)
#         print '   50: ' +str(sys_runnables_period_0050_amount) + ' ' +  str(sys_runnables_period_0050_amount*100.0/runnables)
#         print '  100: ' +str(sys_runnables_period_0100_amount) + ' ' +  str(sys_runnables_period_0100_amount*100.0/runnables)
#         print '  200: ' +str(sys_runnables_period_0200_amount) + ' ' +  str(sys_runnables_period_0200_amount*100.0/runnables)
#         print ' 1000: ' +str(sys_runnables_period_1000_amount) + ' ' +  str(sys_runnables_period_1000_amount*100.0/runnables)
#         print 'angle: ' +str(sys_runnables_period_angle_amount) + ' ' +  str(sys_runnables_period_angle_amount*100.0/runnables)
#
#         print (sys_runnables_period_0001_amount + sys_runnables_period_0002_amount + sys_runnables_period_0005_amount + sys_runnables_period_0010_amount +  sys_runnables_period_0020_amount + sys_runnables_period_0050_amount + sys_runnables_period_0100_amount + sys_runnables_period_0200_amount + sys_runnables_period_1000_amount, sys_runnables_period_angle_amount)


#         average_exe=0.0
#         print "period: 0001"

            # build tasks from runnables (PERIOD = 1)
        wcets = sample_runnable_acet(1, sys_runnables_period_0001_amount, scalingFlag)
        for i in range(sys_runnables_period_0001_amount):
            # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i] , 1, 1))
#             average_exe +=wcets[i]
#         print "average WCET: " + str(average_exe/sys_runnables_period_0001_amount)
#         average_exe=0.0
#         print "\n period: 0002"

            # build tasks from runnables (PERIOD = 2)
        wcets = sample_runnable_acet(2, sys_runnables_period_0002_amount, scalingFlag)
        for i in range(sys_runnables_period_0002_amount):
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i] , 2, 2))
            #average_exe +=wcets[i]
#         print "average WCET: " + str(average_exe/sys_runnables_period_0002_amount)
#         average_exe=0.0
#         print "\n period: 0005"

            # build tasks from runnables (PERIOD = 5)
        wcets = sample_runnable_acet(5, sys_runnables_period_0005_amount, scalingFlag)
        for i in range(sys_runnables_period_0005_amount):
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i] , 5, 5))#
#             average_exe +=wcets[i]
#         print "average WCET: " + str(average_exe/sys_runnables_period_0005_amount)
#         average_exe=0.0
#         print "\n period: 0010"


            # build tasks from runnables (PERIOD = 10)
        wcets = sample_runnable_acet(10, sys_runnables_period_0010_amount, scalingFlag)
        for i in range(sys_runnables_period_0010_amount):
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i], 10, 10))
#             average_exe +=wcets[i]
#         print "average WCET: " + str(average_exe/sys_runnables_period_0010_amount)
#         average_exe=0.0
#         print "\n period: 0020"

            # build tasks from runnables (PERIOD = 20)
        wcets = sample_runnable_acet(20, sys_runnables_period_0020_amount, scalingFlag)
        for i in range(sys_runnables_period_0020_amount):
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i], 20, 20))
            #average_exe +=wcets[i]
#         print "average WCET: " + str(average_exe/sys_runnables_period_0020_amount)
#         average_exe=0.0
#         print "\n period: 0050"

            # build tasks from runnables (PERIOD = 50)
        wcets = sample_runnable_acet(50, sys_runnables_period_0050_amount, scalingFlag)
        for i in range(sys_runnables_period_0050_amount):
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i], 50, 50))
#             average_exe +=wcets[i]
#         print "average WCET: " + str(average_exe/sys_runnables_period_0050_amount)
#         average_exe=0.0
#         print "\n period: 0100"

            # build tasks from runnables (PERIOD = 100)
        wcets = sample_runnable_acet(100, sys_runnables_period_0100_amount, scalingFlag)
        for i in range(sys_runnables_period_0100_amount):
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i], 100, 100))
#             average_exe +=wcets[i]
#         print "average WCET: " + str(average_exe/sys_runnables_period_0100_amount)
#         average_exe=0.0
#         print "\n period: 0200"

            # build tasks from runnables (PERIOD = 200)
        wcets = sample_runnable_acet(200, sys_runnables_period_0200_amount, scalingFlag)
        for i in range(sys_runnables_period_0200_amount):
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i], 200, 200))
#             average_exe +=wcets[i]
#         print "average WCET: " + str(average_exe/sys_runnables_period_0200_amount)
#         average_exe=0.0
#         print "\n period: 1000"

            # build tasks from runnables (PERIOD = 1000)
        wcets = sample_runnable_acet(1000, sys_runnables_period_1000_amount, scalingFlag)
        for i in range(sys_runnables_period_1000_amount):
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i], 1000, 1000))
#             average_exe +=wcets[i]
#         print len(taskset)
#         print "average WCET: " + str(average_exe/sys_runnables_period_1000_amount)
#         average_exe=0.0

        # As angle tasks may have the same period as normal tasks, the period is set to 0.5 to distinguish them
        wcets = sample_runnable_acet('angle', sys_runnables_period_angle_amount, scalingFlag)
        for i in range(sys_runnables_period_angle_amount):
                # C_i = sum of acet(runnable), runnable assigned to task i
            taskset.append(task(wcets[i], 0.5, angle_period))

        random.shuffle(taskset)
        sets=[]

        for j in range(number_of_sets):
            thisset = taskset[:3000]
            taskset = taskset[3000:]
            #print len(taskset)
            util = 0.0
            i = 0
            for tasks in thisset:
                if (tasks['period'] == 0.5):
                    util += tasks['execution']/tasks['deadline']
                else:
                    util += tasks['execution']/tasks['period']
                i = i + 1
                if util > util_max:
                    break

            if(util <= util_max + threshold):
                thisset = thisset[:i]
            else:
                i = i - 1
                initialSet = thisset[:i]
                remainingTasks = thisset[i:]
                tasks = remainingTasks[0]
                if (tasks['period'] == 0.5):
                    util -= tasks['execution']/tasks['deadline']
                else:
                    util -= tasks['execution']/tasks['period']
                #util -= tasks['execution']/tasks['period']
                while (util < util_max):
                    tasks = remainingTasks[0]
                    if (tasks['period'] == 0.5):
                        if (util + tasks['execution']/tasks['deadline'] <= util_max + threshold):
                            util += tasks['execution']/tasks['deadline']
                            initialSet.append(tasks)
                        remainingTasks = remainingTasks[1:]

                    else:
                        if (util + tasks['execution']/tasks['period'] <= util_max + threshold):
                            util += tasks['execution']/tasks['period']
                            initialSet.append(tasks)
                        remainingTasks = remainingTasks[1:]

                thisset = initialSet
            sets.append(thisset)
#             print analysis.cumulative_utilisation (thisset, periods = {0.5})
#             print analysis.cumulative_utilisation (thisset, periods = {5})
#             print util
        return sets
