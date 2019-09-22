#!/bin/sh
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan2237
cd $1
echo $pwd
if [ ! -d "cmdstan-2.14.0" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.14.0/cmdstan-2.14.0.tar.gz
    tar -xf cmdstan-2.14.0.tar.gz
fi

cd cmdstan-2.14.0
make build
if [ ! -d "stan2237" ]; then
    mkdir stan2237
fi
echo $pwd

# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan2237.template && cp stan2237.stan $here/stan2237.stan && cp stan2237.data.R $here/stan2237.data.R)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi

diff ../stan2237.stan stan2237/stan2237.stan

#if [ $? -ne 0 ]; then
cp ../*.R ../*.stan stan2237/
#fi
pwd
echo "making..."
rm -f stan2237/stan2237
make stan2237/stan2237
cd ./stan2237/
pwd
START=$(date +%N)
if [ -z $2 ]
then
./stan2237 sample num_samples=1000 num_warmup=200 save_warmup=0 thin=1 adapt engaged=1 gamma=0.05 delta=0.88 kappa=0.75 t0=10.0 init_buffer=75 term_buffer=50 window=25 algorithm=hmc engine=nuts max_depth=10 metric=diag_e stepsize=1.0 stepsize_jitter=1.0 random seed=-1 init=stan2237.init.R id=1 data file=stan2237.data.R output file=stan2237.csv refresh=100 > stanout 2>&1
else
./stan2237 sample num_samples=$2 num_warmup=200 save_warmup=0 thin=1 adapt engaged=1 gamma=0.05 delta=0.88 kappa=0.75 t0=10.0 init_buffer=75 term_buffer=50 window=25 algorithm=hmc engine=nuts max_depth=10 metric=diag_e stepsize=1.0 stepsize_jitter=1.0 random seed=-1 init=stan2237.init.R id=1 data file=stan2237.data.R output file=stan2237.csv refresh=100 > stanout 2>&1
fi

nans=`grep -wi "variable omega missing" stanout | wc -l`
if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi



