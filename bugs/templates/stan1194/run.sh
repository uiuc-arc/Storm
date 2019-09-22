#!/bin/sh
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan1194
cd $1
echo $pwd
if [ ! -d "cmdstan-2.14.0" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.14.0/cmdstan-2.14.0.tar.gz
    tar -xf cmdstan-2.14.0.tar.gz
fi

cd cmdstan-2.14.0
make build
if [ ! -d "stan1194" ]; then
    mkdir stan1194
fi
echo $pwd
# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan1194.template && cp stan1194.stan $here/stan1194.stan)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi

diff ../stan1194.stan stan1194/stan1194.stan
#if [ $? -ne 0 ]; then
cp  ../*.stan stan1194/
#fi
pwd
echo "making..."
rm -f stan1194/stan1194
make stan1194/stan1194
cd ./stan1194/
pwd
if [ -z $2 ]
then
./stan1194 sample > stanout 2>&1
else
./stan1194 sample num_samples=$2 > stanout 2>&1
fi

nans=`grep -wi "std::bad_alloc" stanout | wc -l`
if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi
