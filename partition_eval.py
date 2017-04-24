import partition_ILP as multi
import generator

def main():
    # some taskset, third argument is for sstype setting as PASS {S, M, L}={0, 1, else}
    # Forth argument is the propotion of SSS in the task set.
    taskset = generator.taskGeneration(10, 100, 0, 0.2)
    # taskset, num of procs

    obj = multi.partition(taskset, 'carryin')
    obj = multi.partition(taskset, 'blocking')
    obj = multi.partition(taskset, 'k2q')
    obj = multi.partition(taskset, 'inflation')

if __name__ == "__main__":
    main()