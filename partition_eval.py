import partition_ILP as multi
import STPartition as STP
import generator

def main():
    # some taskset, third argument is for sstype setting as PASS {S, M, L}
    # Forth argument is the propotion of SSS in the task set.
    taskset = generator.taskGeneration(10, 100, 'S')
    # taskset, num of procs

    obj = multi.partition(taskset, 'carryin')
    obj = multi.partition(taskset, 'blocking')
    obj = multi.partition(taskset, 'k2q')
    obj = multi.partition(taskset, 'inflation')
    obj = STP.STPartition(taskset, 'carry')
    obj = STP.STPartition(taskset, 'block')
    obj = STP.STPartition(taskset, 'jit')

if __name__ == "__main__":
    main()
