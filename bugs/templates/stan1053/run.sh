#!/bin/sh
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan1053
cd $1
echo $pwd
if [ ! -d "cmdstan-2.6.0" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.6.0/cmdstan-2.6.0.tar.gz
    tar -xf cmdstan-2.6.0.tar.gz
fi

cd cmdstan-2.6.0
make build
if [ ! -d "stan1053" ]; then
    mkdir stan1053
fi

# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan1053.template && cp stan1053.stan $here/stan1053.stan)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi

diff ../stan1053.stan stan1053/stan1053.stan
#if [ $? -ne 0 ]; then
cp ../*.stan stan1053/
#fi
pwd
echo "making..."
rm -f stan1053/stan1053
make stan1053/stan1053
cd ./stan1053/
pwd
START=$(date +%N)
if [ -z $2 ]
then
./stan1053 sample algorithm=fixed_param num_warmup=5000 num_samples=10000 random seed=12345 > stanout 2>&1
else
echo "Samples : $2"
./stan1053 sample algorithm=fixed_param num_warmup=5000 num_samples=$2 random seed=12345 > stanout 2>&1
fi

nans=`grep -i "parameter is inf" stanout | wc -l`
if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi



