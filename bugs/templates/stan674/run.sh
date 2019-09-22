#!/bin/sh
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan674
cd $1
echo $pwd
if [ ! -d "cmdstan" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.3.0/cmdstan-2.3.0.tar.gz
    tar -xf cmdstan-2.3.0.tar.gz
fi

cd cmdstan
make build
if [ ! -d "stan674" ]; then
    mkdir stan674
fi


# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan674.template && cp stan674.stan $here/stan674.stan)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi

diff ../stan674.stan stan674/stan674.stan
#if [ $? -ne 0 ]; then
cp ../*.data ../*.stan stan674/
#fi
pwd
echo "making..."
rm -f stan674/stan674
make stan674/stan674
cd ./stan674/
pwd
START=$(date +%N)

if [ -z $2 ]
then
timeout 120 ./stan674  sample random seed=4294967295 > /dev/null
else
echo "Samples : $2"
timeout 120 ./stan674  sample num_samples=$2 random seed=4294967295 > /dev/null
fi

status=$?
if [ $status -eq 124 ] #timed out
then
    echo "Passed"
else
	echo "Failed"
fi




