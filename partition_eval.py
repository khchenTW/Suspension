from __future__ import division
import partition_ILP as multi
import STPartition as STP
import generator
import sys
import math
import numpy as np

def main():
    '''
    args = sys.argv
    if len(args) < 3:
        return -1 # no input
    tasksets_amount = int (args[1])
    inputfiles_amount = int (args[2])
    tasksets_amount = int(math.ceil(tasksets_amount / inputfiles_amount))
    dist_utilizations = {
        "10Tasks" : 10,
        "20Tasks" : 20,
        "30Tasks" : 30,
    }
    trail = 0
    uti = 1
    for set_name, amount in dist_utilizations.items():
        uti = amount*10
        for u in range(1, 15):

        for j in range(inputfiles_amount):
            tasksets = [generator.taskGeneration(amount, uti, 'S') for n in range(tasksets_amount)]
            np.save (str(set_name)+'_'+str(uti)+'_'+str(j)+'_'+'S', tasksets)

            tasksets = [generator.taskGeneration(amount, uti, 'M') for n in range(tasksets_amount)]
            np.save (str(set_name)+'_'+str(uti)+'_'+str(j)+'_'+'M', tasksets)

            tasksets = [generator.taskGeneration(amount, uti, 'L') for n in range(tasksets_amount)]
            np.save (str(set_name)+'_'+str(uti)+'_'+str(j)+'_'+'L', tasksets)
        trail+=1
    '''
    # generate some taskset, third argument is for sstype setting as PASS {S, M, L}
    taskset = generator.taskGeneration(10, 100, 'S')

    #for taskset in :
    # taskset, num of procs
    obj = []
    # ILP Tests
    obj.append(multi.partition(taskset, 'carryin'))
    obj.append(multi.partition(taskset, 'blocking'))
    obj.append(multi.partition(taskset, 'k2q'))
    obj.append(multi.partition(taskset, 'inflation'))

    binpack = 'first'
    # Heuristic + TDA Tests
    obj.append(STP.STPartition(taskset, 'carry', binpack))
    obj.append(STP.STPartition(taskset, 'block', binpack))
    obj.append(STP.STPartition(taskset, 'jit', binpack))
    obj.append(STP.STPartition(taskset, 'jitblock', binpack))
    obj.append(STP.STPartition(taskset, 'tdamix', binpack))

    # Heuristic + Constant Time Tests
    obj.append(STP.STPartition(taskset, 'CTcarry', binpack))
    obj.append(STP.STPartition(taskset, 'CTblock', binpack))
    obj.append(STP.STPartition(taskset, 'CTjit', binpack))
    obj.append(STP.STPartition(taskset, 'CTmix', binpack))

    # Show the results

    print ''
    print '[ILPcarry, ILPblock, ILPjit, inflation, TDAcarry, TDAblock, TDAjit, TDAjitblock, TDAmix, CTcarry, CTblock, CTjit, CTmix]'
    print obj
if __name__ == "__main__":
    main()
