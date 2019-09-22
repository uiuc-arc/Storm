#!/bin/sh
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan1435
cd $1
echo $pwd
if [ ! -d "cmdstan-2.6.2" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.6.2/cmdstan-2.6.2.tar.gz
    tar -xf cmdstan-2.6.2.tar.gz
fi

cd cmdstan-2.6.2
make build
if [ ! -d "stan1435" ]; then
    mkdir stan1435
fi
echo $pwd
# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan1435.template && cp stan1435.stan $here/stan1435.stan && cp stan1435.data.R $here/stan1435.data.R)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi

diff ../stan1435.stan stan1435/stan1435.stan
diff ../stan1435.data.R stan1435/stan1435.data.R
#if [ $? -ne 0 ]; then
cp ../*.R ../*.stan stan1435/
#fi
pwd
echo "making..."
rm -f stan1435/stan1435
make stan1435/stan1435
cd ./stan1435/
pwd
START=$(date +%N)
./stan1435 optimize data file=stan1435.data.R > stanout 2>&1

nans=`grep -wi "_M_range_check" stanout | wc -l`
if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi


