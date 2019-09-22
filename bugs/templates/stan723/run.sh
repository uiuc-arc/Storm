#!/bin/sh
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan723
cd $1
echo $pwd
if [ ! -d "cmdstan" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.3.0/cmdstan-2.3.0.tar.gz
    tar -xf cmdstan-2.3.0.tar.gz
fi

cd cmdstan
make build
if [ ! -d "stan723" ]; then
    mkdir stan723
fi


# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan723.template && cp stan723.stan $here/stan723.stan)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi
echo $pwd
diff ../stan723.stan stan723/stan723.stan
#if [ $? -ne 0 ]; then
cp  ../*.stan stan723/
#fi
pwd
echo "making..."
rm -f stan723/stan723
make stan723/stan723 > stanout 2>&1

nans=`grep -wi "template argument deduction/substitution failed" stanout | wc -l`
if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi
