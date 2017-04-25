import partition_ILP as multi
import STPartition as STP
import generator

def main():
    # some taskset, third argument is for sstype setting as PASS {S, M, L}
    # Forth argument is the propotion of SSS in the task set.
    taskset = generator.taskGeneration(10, 300, 'S')
    # taskset, num of procs

    # ILP Tests
    obj = multi.partition(taskset, 'carryin')
    obj = multi.partition(taskset, 'blocking')
    obj = multi.partition(taskset, 'k2q')
    obj = multi.partition(taskset, 'inflation')
    # Heuristic + TDA Tests
    obj = STP.STPartition(taskset, 'carry')
    obj = STP.STPartition(taskset, 'block')
    obj = STP.STPartition(taskset, 'jit')

    # Heuristic + Constant Time Tests
    obj = STP.STPartition(taskset, 'CTcarry')
    obj = STP.STPartition(taskset, 'CTblock')
    obj = STP.STPartition(taskset, 'CTjit')

if __name__ == "__main__":
    main()
