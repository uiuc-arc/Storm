#!/bin/sh
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan2311
cd $1
echo $pwd
if [ ! -d "cmdstan-2.15.0" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.15.0/cmdstan-2.15.0.tar.gz
    tar -xf cmdstan-2.15.0.tar.gz
fi

cd cmdstan-2.15.0
make build
if [ ! -d "stan2311" ]; then
    mkdir stan2311
fi
echo $pwd
# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan2311.template && cp stan2311.stan $here/stan2311.stan)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi
diff ../stan2311.stan stan2311/stan2311.stan
#if [ $? -ne 0 ]; then
cp ../*.data ../*.stan stan2311/
#fi
pwd
echo "making..."
rm -f stan2311/stan2311
make stan2311/stan2311
cd ./stan2311/
pwd
START=$(date +%N)
if [ -z $2 ] 
then
./stan2311 sample random seed=4294967295 > stanout 2>&1
else
./stan2311 sample num_samples=$2 random seed=4294967295 > stanout 2>&1
fi

nans=`grep -wi "100 attempts" stanout | wc -l`
if [ $nans -gt 0 ]; 
then
echo "Passed"
else
echo "Failed"
fi



