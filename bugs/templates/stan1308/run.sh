#!/bin/sh
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan1308
cd $1
echo $pwd
if [ ! -d "cmdstan-2.6.0" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.6.0/cmdstan-2.6.0.tar.gz
    tar -xf cmdstan-2.6.0.tar.gz
fi

cd cmdstan-2.6.0
make build
if [ ! -d "stan1308" ]; then
    mkdir stan1308
fi

# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan1308.template && cp stan1308.stan $here/stan1308.stan && cp stan1308.data.R $here/stan1308.data.R)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi

echo $pwd
diff ../stan1308.stan stan1308/stan1308.stan
#if [ $? -ne 0 ]; then
cp ../*.R ../*.stan stan1308/
#fi
pwd
echo "making..."
rm -f stan1308/stan1308
make stan1308/stan1308
cd ./stan1308/
pwd
START=$(date +%N)
./stan1308 diagnose data file=stan1308.data.R random seed=5 > stanout 2>&1

nans=`grep -wi "\-nan" stanout | wc -l`
if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi


