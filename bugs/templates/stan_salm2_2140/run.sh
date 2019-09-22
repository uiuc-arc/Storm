#!/bin/bash
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan_salm2_2140
cd $1
echo $pwd
if [ ! -d "cmdstan-2.14.0" ]; then
    mkdir -p cmdstan-2.14.0
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.14.0/cmdstan-2.14.0.tar.gz
    tar -xf cmdstan-2.14.0.tar.gz -C cmdstan-2.14.0/ --strip-components 1
fi
initcontent=`cat stan_salm2_2140.stan`
cd cmdstan-2.14.0
make build
if [ ! -d "stan_salm2_2140" ]; then
    mkdir stan_salm2_2140
fi
echo $pwd
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan_salm2_2140.template && cp stan_salm2_2140.stan $here/stan_salm2_2140.stan && cp stan_salm2_2140.data.R $here/stan_salm2_2140.data.R)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi
curcontent=`cat ../stan_salm2_2140.stan`
#diff ../stan_salm2_2140.stan stan_salm2_2140/stan_salm2_2140.stan
diff <(echo "$initcontent") <(echo "$curcontent")
#if [ $? -ne 0 ]; then
cp ../stan_salm2_2140.data.R ../*.stan stan_salm2_2140/
#fi
pwd
echo "making..."
rm -f stan_salm2_2140/stan_salm2_2140
make stan_salm2_2140/stan_salm2_2140
cd ./stan_salm2_2140/
pwd
if [ -z $2 ]
then
timeout 120 ./stan_salm2_2140 variational elbo_samples=10 eval_elbo=10 iter=100 tol_rel_obj=0.001 random seed=1524389580 data file=stan_salm2_2140.data.R > stanout 2>&1
else
echo "Iterations : $2"
timeout 120 ./stan_salm2_2140 variational elbo_samples=10 eval_elbo=10 iter=$2 tol_rel_obj=0.001 random seed=1524389580 data file=stan_salm2_2140.data.R > stanout 2>&1
fi

nans=`grep  -i "All proposed step-sizes failed" stanout | wc -l`
if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi
