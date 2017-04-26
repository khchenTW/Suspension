from __future__ import division
from collections import OrderedDict
import partition_ILP as multi
import trinity_ILP as tri
import STPartition as STP
import generator
import sys
import math
import numpy as np
from scipy.stats.mstats import gmean
from miscs import *

def main():
    args = sys.argv
    if len(args) < 5:
            print "Usage: python partition_eval.py [debug] [# of sets] [generate/load] [stype] [group]"
            return -1 # no input

    debug = int (args[1])
    if debug == 0:
        tasksets_amount = int (args[2])
        mode = int(args[3]) # 0 = generate, 1 = directly use the inputs
        stype = args[4] # S, M, L
        group = args[5] # this should be less than inputfiles_amount
        inputfiles_amount = 1 # n for distribution
        tasksets_amount = int(math.ceil(tasksets_amount / inputfiles_amount))

        dist_utilizations = OrderedDict()
        #dist_utilizations['10Tasks'] = 10
        #dist_utilizations['20Tasks'] = 20
        dist_utilizations['30Tasks'] = 30

        idx = 0
        perAmount = [[] for i in range(len(dist_utilizations.items()))]
        for set_name, amount in dist_utilizations.items():
            #for uti in range(int(100/10*amount), int(550/10*amount)+1, 5*amount):
            for uti in range(int(400/10*amount), int(550/10*amount)+1, 5*amount):
                for j in range(inputfiles_amount):
                    if mode == 0:
                        if stype == 'S':
                            tasksets = [generator.taskGeneration(amount, uti, 'S') for n in range(tasksets_amount)]
                            np.save ('input/'+str(set_name)+'_'+str(uti)+'_'+str(j)+'_S', tasksets)

                        elif stype == 'M':
                            tasksets = [generator.taskGeneration(amount, uti, 'M') for n in range(tasksets_amount)]
                            np.save ('input/'+str(set_name)+'_'+str(uti)+'_'+str(j)+'_M', tasksets)

                        elif stype == 'L':
                            tasksets = [generator.taskGeneration(amount, uti, 'L') for n in range(tasksets_amount)]
                            np.save ('input/'+str(set_name)+'_'+str(uti)+'_'+str(j)+'_L', tasksets)
                    else:
                        pass
                        #TODO check if the inputs are there.
                perAmount[idx].append('input/'+str(set_name)+'_'+str(uti)+'_'+str(group)+'_'+str(stype)+'.npy')
            idx+=1
        print perAmount

        if mode == 1:
            gRes=[[] for i in range(13)] # 13 methods
            for idx, filenames  in enumerate(perAmount):
                #fileB = 'Results-tasks'+repr((1+idx)*10)+'_stype'+repr(stype)+'_group'+repr(group)
                fileB = 'Results-tasks'+repr((1+idx)*30)+'_stype'+repr(stype)+'_group'+repr(group)
                file_B = open('output/'+fileB + '.txt', "w")
                for filename in filenames:
                    file_B.write(filename+'\n')
                    tasksets = np.load(filename)
                    for taskset in tasksets:
                        res = test(taskset, debug)
                        file_B.write('[ILPcarry, ILPblock, ILPjit, inflation, Trinity, TDAcarry, TDAblock, TDAjit, TDAjitblock, TDAmix, CTcarry, CTblock, CTjit, CTmix]\n')
                        file_B.write(str(res)+'\n')
                        for ind, j in enumerate(res):
                            if j == -1:
                                file_B.write('Infeasible in ILP \n')
                            elif j == -2:
                                file_B.write('ILP pops out an uncatched status \n')
                            elif j == -3:
                                file_B.write('Infeasible in the double checking \n')
                            gRes[ind].append(j)
                    result = []
                    for i in gRes:
                        result.append(gmean(i))
                    file_B.write('Gmean: \n')
                    file_B.write(str(result)+'\n')
                file_B.close()
        if mode == 2:
            gRes=[[] for i in range(13)] # 13 methods
            for idx, filenames  in enumerate(perAmount):
                if idx == 2: #print for 30 tasks
                    fileA = 'DEtasks'+repr((1+idx)*10)+'_stype'+repr(stype)+'_group'+repr(group)
                    file = open('output/'+fileA + '.txt', "w")
                    for filename in filenames:
                        file.write(filename+'\n')
                        tasksets = np.load(filename)
                        for taskset in tasksets:
                            file.write(str(taskset)+'\n')
                            sumUt = 0.0
                            sumUs = 0.0
                            for i in taskset:
                                sumUt += utili(i)
                                sumUs += utiliAddE(i)
                            file.write('total utili:'+str(sumUt)+'\n')
                            file.write('total utili+exclusive:'+str(sumUs)+'\n')
                        file.write('\n')
                    file.close()

    else:
        # DEBUG
        # generate some taskset, third argument is for sstype setting as PASS {S, M, L}
        taskset = generator.taskGeneration(4, 300, 'S')
        test(taskset, debug)

def test(taskset, debug):
    # taskset, num of procs
    obj = []
    if debug == 1:
        print "DEBUG MODE:"
    else:
        # ILP Tests
        obj.append(multi.partition(taskset, 'carryin'))
        obj.append(multi.partition(taskset, 'blocking'))
        obj.append(multi.partition(taskset, 'k2q'))
        obj.append(multi.partition(taskset, 'inflation'))
        obj.append(tri.partition(taskset))
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

    #print ''
    #print '[ILPcarry, ILPblock, ILPjit, inflation, Trinity, TDAcarry, TDAblock, TDAjit, TDAjitblock, TDAmix, CTcarry, CTblock, CTjit, CTmix]'
    #print obj
    return obj
if __name__ == "__main__":
    main()
