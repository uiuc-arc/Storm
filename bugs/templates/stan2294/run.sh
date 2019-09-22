#!/bin/sh
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan2294
cd $1
echo $pwd
if [ ! -d "cmdstan-2.15.0" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.15.0/cmdstan-2.15.0.tar.gz
    tar -xf cmdstan-2.15.0.tar.gz
fi

cd cmdstan-2.15.0
make build
if [ ! -d "stan2294" ]; then
    mkdir stan2294
fi
echo $pwd
# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan2294.template && cp stan2294.stan $here/stan2294.stan)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi
diff ../stan2294.stan stan2294/stan2294.stan
#if [ $? -ne 0 ]; then
cp ../*.data ../*.stan stan2294/
#fi
pwd
echo "making..."
rm -f stan2294/stan2294
make stan2294/stan2294
cd ./stan2294/
pwd
START=$(date +%N)
if [ -z $2 ]
then
./stan2294 sample random seed=4294967295 > stanout 2>&1
else
./stan2294 sample num_samples=$2 random seed=4294967295 > stanout 2>&1
fi

exception=`grep -i "failed after 100 attempts" stanout | wc -l`
if [ $exception -gt 0 ]; then
	echo "Passed"
else
	echo "Failed"
fi


