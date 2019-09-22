#!/bin/sh
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan1241
cd $1
echo $pwd
if [ ! -d "cmdstan" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.5.0/cmdstan-2.5.0.tar.gz
    tar -xf cmdstan-2.5.0.tar.gz
fi

cd cmdstan
make build
if [ ! -d "stan1241" ]; then
    mkdir stan1241
fi

# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan1241.template && cp stan1241.stan $here/stan1241.stan)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi

diff ../stan1241.stan stan1241/stan1241.stan
#if [ $? -ne 0 ]; then
cp ../*.stan stan1241/
#fi
pwd
echo "making..."
rm -f stan1241/stan1241
make stan1241/stan1241
cd ./stan1241/
pwd
START=$(date +%N)
if [ -z $2 ]
then
./stan1241 sample > stanout 2>&1
else
./stan1241 sample num_samples=$2 > stanout 2>&1
fi

nans=`grep -wi "shapes must match" stanout | wc -l`
if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi


