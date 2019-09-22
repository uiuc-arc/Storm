#!/bin/sh
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan1443
cd $1
echo $pwd
if [ ! -d "cmdstan-2.6.2" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.6.2/cmdstan-2.6.2.tar.gz
    tar -xf cmdstan-2.6.2.tar.gz
fi

cd cmdstan-2.6.2
make build
if [ ! -d "stan1443" ]; then
    mkdir stan1443
fi
echo $pwd
# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan1443.template && cp stan1443.stan $here/stan1443.stan)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi

diff ../stan1443.stan stan1443/stan1443.stan
#if [ $? -ne 0 ]; then
cp ../*.data ../*.stan stan1443/
#fi
pwd
echo "making..."
rm -f stan1443/stan1443
make stan1443/stan1443
cd ./stan1443/
pwd
START=$(date +%N)
if [ -z $2 ]
then
./stan1443 sample > stanout 2>&1
else
./stan1443 sample num_samples=$2 > stanout 2>&1
fi

nans=`grep -wi "Segmentation fault" stanout | wc -l`
if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi



