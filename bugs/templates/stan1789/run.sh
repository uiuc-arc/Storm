#!/bin/sh
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan1789
cd $1
echo $pwd
if [ ! -d "cmdstan-2.9.0" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.9.0/cmdstan-2.9.0.tar.gz
    tar -xf cmdstan-2.9.0.tar.gz
fi

cd cmdstan-2.9.0
make build
if [ ! -d "stan1789" ]; then
    mkdir stan1789
fi
echo $pwd
# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan1789.template && cp stan1789.stan $here/stan1789.stan)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi

diff ../stan1789.stan stan1789/stan1789.stan
#if [ $? -ne 0 ]; then
cp ../*.stan stan1789/
#fi
pwd
echo "making..."
rm -f stan1789/stan1789
make stan1789/stan1789
cd ./stan1789/
pwd
START=$(date +%N)
if [ -z $2 ] 
then
./stan1789 sample > stanout 2>&1
else
./stan1789 sample num_samples=$2 > stanout 2>&1
fi

nans=`grep -wi "Rejecting initial value" stanout | wc -l`
if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi


