import partitionalgo as multi
import analysis
import generator

def main():
    # some taskset, third argument is for sstype setting as PASS {S, M, L}={0, 1, else}
    # Forth argument is the propotion of SSS in the task set.
    taskset = generator.taskGeneration(10, 20, 0, 0.2)
    # taskset, num of procs

    obj = multi.partition(taskset, 10)
    obj = multi.partition(taskset, 11)
    obj = multi.partition(taskset, 13)

if __name__ == "__main__":
    main()
