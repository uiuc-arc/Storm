# Storm

This repository contains the source code for our paper: 
[Storm: Program Reduction for Testing and Debugging Probabilistic Programming Systems](http://misailo.web.engr.illinois.edu/papers/storm-fse19.pdf)


## How to run

Prerequisites:

```
java
maven
```

To install all dependencies and build all the benchmarks, use:

`bash setup.sh`


To change which set of benchmarks to use, edit `/src/main/resources/config.properties` and change the `TESTSET` to `stan` for "stan issues", `stan_em`
for "stan example models", and `pyro` for "pyro benchmarks"

To run Storm on all the benchmarks in the chosen testset, use:

`bash run.sh`

After running, the output will be in `out/diag*` folder

If you use our framework for your research, please cite as:

```
@article{dutta2019storm,
  title={Storm: Program Reduction for Testing and Debugging Probabilistic Programming Systems},
  author={Dutta, Saikat and Zhang, Wenxian and Huang, Zixin and Misailovic, Sasa},
  year={2019}
}
```
