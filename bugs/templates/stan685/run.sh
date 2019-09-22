#!/bin/sh
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan685
cd $1
echo $pwd
if [ ! -d "cmdstan" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.3.0/cmdstan-2.3.0.tar.gz
    tar -xf cmdstan-2.3.0.tar.gz
fi

cd cmdstan
make build
if [ ! -d "stan685" ]; then
    mkdir stan685
fi


# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan685.template && cp stan685.stan $here/stan685.stan)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi
diff ../stan685.stan stan685/stan685.stan
#if [ $? -ne 0 ]; then
cp ../*.data ../*.stan stan685/
#fi
pwd
echo "making..."
rm -f stan685/stan685
make stan685/stan685
cd ./stan685/
pwd
START=$(date +%N)
if [ -z $2 ]
then
./stan685 sample random seed=4294967295 > stanout 2>&1
else
./stan685 sample num_samples=$2 random seed=4294967295 > stanout 2>&1
fi

nans=`grep -wi "100 attempts" stanout | wc -l`
if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi





