#!/usr/bin/env bash
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan1121
cd $1
echo $pwd
if [ ! -d "cmdstan" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.5.0/cmdstan-2.5.0.tar.gz
    tar -xf cmdstan-2.5.0.tar.gz
fi

cd cmdstan
make build
if [ ! -d "stan1121" ]; then
    mkdir stan1121
fi
echo $pwd

# translate template to stan
here=`realpath ../`
echo $here

(cd ../../../../translators/ && ./teststan.py -o $here/stan1121.template && cp stan1121.stan $here/stan1121.stan && cp stan1121.data.R $here/stan1121.data.R)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi

diff ../stan1121.stan stan1121/stan1121.stan
diff ../stan1121.data.R stan1121/stan1121.data.R
#if [ $? -ne 0 ]; then
cp ../*.R ../*.stan stan1121/
#fi
pwd
echo "making..."
rm -f stan1121/stan1121
make stan1121/stan1121 > /dev/null >&2
cd ./stan1121/

if [ -z $2 ]
then
./stan1121 sample save_warmup=1 random seed=2205139738 data file=stan1121.data.R > stanout 2>&1
else
./stan1121 sample num_samples=$2 save_warmup=1 random seed=2205139738 data file=stan1121.data.R > stanout 2>&1
fi

nans=`grep -wi "not symmetric" stanout | wc -l`
if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi
#END=$(date +%N)
#DIFF=$(( ($END - $START)/1000 ))
#echo $DIFF >> stanout