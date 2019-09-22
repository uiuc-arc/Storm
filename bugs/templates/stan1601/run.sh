#!/bin/sh
# first argument is the directory where everthing should be setup

cd $1
pwd
if [ ! -d "cmdstan-2.7.0" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.7.0/cmdstan-2.7.0.tar.gz
    tar -xf cmdstan-2.7.0.tar.gz
fi

cd cmdstan-2.7.0
make build
if [ ! -d "stan1601" ]; then
    mkdir stan1601
fi

# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan1601.template && cp stan1601.stan $here/stan1601.stan && cp stan1601.data.R $here/stan1601.data)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi

diff ../stan1601.stan stan1601/stan1601.stan

cp ../*.data ../*.stan stan1601/

echo "making..."
rm -f stan1601/stan1601
make stan1601/stan1601
cd ./stan1601/

START=$(date +%N)
if [ -z $2 ]
then
./stan1601 variational elbo_samples=10 eval_elbo=10 iter=100 tol_rel_obj=0.001 random seed=3125502058 data file=stan1601.data > stanout 2>&1
else
echo "Running with iters: $2"
./stan1601 variational elbo_samples=10 eval_elbo=10 iter=$2 tol_rel_obj=0.001 random seed=3125502058 data file=stan1601.data > stanout 2>&1
fi

nans=`grep -i "input vector.*nan" stanout | wc -l`
if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi



