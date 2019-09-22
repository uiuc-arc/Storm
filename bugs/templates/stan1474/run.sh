#!/bin/sh
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan1474
cd $1
echo $pwd
if [ ! -d "cmdstan-2.6.0" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.6.0/cmdstan-2.6.0.tar.gz
    tar -xf cmdstan-2.6.0.tar.gz
fi

cd cmdstan-2.6.0
make build
if [ ! -d "stan1474" ]; then
    mkdir stan1474
fi
echo $pwd
# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan1474.template && cp stan1474.stan $here/stan1474.stan)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi

diff ../stan1474.stan stan1474/stan1474.stan
#if [ $? -ne 0 ]; then
cp  ../*.stan stan1474/
#fi
pwd
echo "making..."
rm -f stan1474/stan1474	
make stan1474/stan1474
cd ./stan1474/
pwd
START=$(date +%N)
if [ -z $2 ]
then
./stan1474 sample random seed=4294967295 > stanout 2>&1
else
./stan1474 sample num_samples=$2 random seed=4294967295 > stanout 2>&1
fi

nans=`grep -wi "\-nan" stanout | wc -l`
if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi


