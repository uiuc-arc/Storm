#!/bin/sh
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan1200
cd $1
echo $pwd
if [ ! -d "cmdstan" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.5.0/cmdstan-2.5.0.tar.gz
    tar -xf cmdstan-2.5.0.tar.gz
fi

cd cmdstan
make build
if [ ! -d "stan1200" ]; then
    mkdir stan1200
fi
echo $pwd


# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan1200.template && cp stan1200.stan $here/stan1200.stan && cp stan1200.data.R $here/stan1200.data.R)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi

#diff ../stan1200.stan stan1200/stan1200.stan

#if [ $? -ne 0 ]; then
cp ../*.R ../*.stan stan1200/
#fi
pwd
echo "making..."
rm -f stan1200/stan1200
timeout 120 make stan1200/stan1200 > /dev/null 2>&1
cd ./stan1200/
pwd
START=$(date +%N)
export LIBC_FATAL_STDERR_=1
{ timeout 180 ./stan1200 optimize data file=stan1200.data.R; } > stanout 2>&1

nans=`grep -i "Segmentation fault\|Aborted" stanout | wc -l`
if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi



