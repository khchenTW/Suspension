# Suspension-base Partitioning Approaches

This is the related source code for the RTAS'18 paper:
http://zheng.eng.wayne.edu/_resources/pdfs/RTAS2018.pdf.

"Shared-Resource-Centric Limited Preemptive Scheduling: A Comprehensive Study of Suspension-base Partitioning Approaches", Zheng Dong, Cong Liu, Soroush Bateni, Kuan-Hsun Chen, Jian-Jia Chen, Georg von der Brüggen and Junjie Shi.

# Environment

We used the Gurobi library, https://www.gurobi.com/index, to implement the proposed ILPs. 

You may need a license to use the library.

Python version is 2.7

# The way to use (Follow the paper)

partition_eval.py is for the assumption that one task requires only one resource:  
"Usage: python partition_eval.py [debug] [# of sets] [generate/load] [stype] [btype]"
The details of each parameter are as follows:
> debug, it is used to put some ad-hoc code for debugging.

> \# of sets, it is the amount of tasksets you want to test in the simulation.

> generate/load, 0 generates the npy file which contains the generated task sets; 1 directly read the generated task sets.

> stype, the length of suspension: S, M, and L. Please refer to generator.py for more details.

> btype, N for preemptive scehduling: [S, M, L] for limited preemptive scheduling. 

For example, if you want to test 100 task sets with "short resource access" for limited-preemptive [S,M,L] or preemptive scheudling [N]:

Step 1 - generate task sets:
> python partition_eval.py 0 100 0 S [N,S,M,L] 

Step 2 - read task sets:
> python partition_eval.py 0 100 1 S [N,S,M,L]

For different kind of tests, the implementations are modularized in different files separately:  
>Trinty ILP test: trinity_ILP.py  
>TDA test: TDA.py  
>Combo ILP test: combo_ILP.py  
>Constant Time Test: ctTest.py  
>Optimization algorithm is in STPartition.py

Mpartition_eval.py is without the assumption of resource constraints.  
All the used modules for this simulation are with prefix "M"

# Printer (Readable output generator)
In printer folder, mean_printer.py has the completed toolbox to generate the readable figures.  
The core in the toolbox is "wayofMean()": 
> It uses the given way of mean, e.g., np.mean or gmean to generate the results with all the other parameters.
Now the default is the geometric mean.

"Usage: python mean_printer.py [representative/ILP/TDA/CT]"
> The input should be given as the string: "REP", "ILP", "TDA", "CT"

The file inputs should be placed in the corresponding folder, which can be found in the source code.


