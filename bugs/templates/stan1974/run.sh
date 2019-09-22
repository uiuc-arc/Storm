#!/bin/sh
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan1974
cd $1
echo $pwd
if [ ! -d "cmdstan-2.10.0" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.10.0/cmdstan-2.10.0.tar.gz
    tar -xf cmdstan-2.10.0.tar.gz
fi

cd cmdstan-2.10.0
make build
if [ ! -d "stan1974" ]; then
    mkdir stan1974
fi
echo $pwd
# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan1974.template && cp stan1974.stan $here/stan1974.stan)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi
diff ../stan1974.stan stan1974/stan1974.stan
#if [ $? -ne 0 ]; then
cp ../*.data ../*.stan stan1974/
#fi
pwd
echo "making..."
rm -f stan1974/stan1974
make stan1974/stan1974
cd ./stan1974/
pwd
START=$(date +%N)
if [ -z $2 ]
then
timeout 60 ./stan1974 sample > stanout 2>&1
else
timeout 60 ./stan1974 sample num_samples=$2 > stanout 2>&1
fi

nans=`grep -wi "Floating point exception" stanout | wc -l`
if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi


