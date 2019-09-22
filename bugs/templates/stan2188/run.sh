#!/bin/sh
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan2188
cd $1
echo $pwd
if [ ! -d "cmdstan-2.13.1" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.13.1/cmdstan-2.13.1.tar.gz
    tar -xf cmdstan-2.13.1.tar.gz
fi

cd cmdstan-2.13.1
make build
if [ ! -d "stan2188" ]; then
    mkdir stan2188
fi
echo $pwd
# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan2188.template && cp stan2188.stan $here/stan2188.stan)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi
diff ../stan2188.stan stan2188/stan2188.stan
#if [ $? -ne 0 ]; then
cp  ../*.stan stan2188/
#fi
pwd
echo "making..."
rm -f stan2188/stan2188	
make stan2188/stan2188
cd ./stan2188/
pwd
START=$(date +%N)
if [ -z $2 ]; then
./stan2188 variational elbo_samples=10 eval_elbo=10 iter=100 tol_rel_obj=0.001 random seed=3125502058 > stanout 2>&1
else
./stan2188 variational elbo_samples=10 eval_elbo=10 iter=$2 tol_rel_obj=0.001 random seed=3125502058 > stanout 2>&1
fi

nans=`grep -wi "100 attempts" stanout | wc -l`
if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi


