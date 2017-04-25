import partition_ILP as multi
import STPartition as STP
import generator

def main():
    # some taskset, third argument is for sstype setting as PASS {S, M, L}
    # Forth argument is the propotion of SSS in the task set.
    taskset = generator.taskGeneration(3, 50, 'S')
    # taskset, num of procs
    obj = []
    # ILP Tests
    obj.append(multi.partition(taskset, 'carryin'))
    obj.append(multi.partition(taskset, 'blocking'))
    obj.append(multi.partition(taskset, 'k2q'))
    obj.append(multi.partition(taskset, 'inflation'))

    binpack = 'last'
    # Heuristic + TDA Tests
    obj.append(STP.STPartition(taskset, 'carry', binpack))
    obj.append(STP.STPartition(taskset, 'block', binpack))
    obj.append(STP.STPartition(taskset, 'jit', binpack))

    # Heuristic + Constant Time Tests
    obj.append(STP.STPartition(taskset, 'CTcarry', binpack))
    obj.append(STP.STPartition(taskset, 'CTblock', binpack))
    obj.append(STP.STPartition(taskset, 'CTjit', binpack))

    # Show the results
    print ''
    print '[ILPcarry, ILPblock, ILPjit, inflation, Hcarry, Hblock, Hjit, CTcarry, CTblock, CTjit]'
    print obj
if __name__ == "__main__":
    main()
