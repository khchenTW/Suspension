import partition_ILP as multi
import STPartition as STP
import generator

def main():
    # some taskset, third argument is for sstype setting as PASS {S, M, L}
    # Forth argument is the propotion of SSS in the task set.
    taskset = generator.taskGeneration(10, 150, 'S')
    # taskset, num of procs

    obj = multi.partition(taskset, 'carryin')
    obj = multi.partition(taskset, 'blocking')
    obj = multi.partition(taskset, 'k2q')
    obj = multi.partition(taskset, 'inflation')
    obj = STP.STPartition(taskset)

if __name__ == "__main__":
    main()
