    #!/bin/sh
# first argument is the directory where everthing should be setup

# cd ../TestMin/bugs/stan1366
cd $1
echo $pwd
if [ ! -d "cmdstan" ]; then
    wget https://github.com/stan-dev/cmdstan/releases/download/v2.5.0/cmdstan-2.5.0.tar.gz
    tar -xf cmdstan-2.5.0.tar.gz
fi

cd cmdstan
make build
if [ ! -d "stan1366" ]; then
    mkdir stan1366
fi
echo $pwd

# translate template to stan
here=`realpath ../`
echo $here
(cd ../../../../translators/ && ./teststan.py -o $here/stan1366.template && cp stan1366.stan $here/stan1366.stan)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi

diff ../stan1366.stan stan1366/stan1366.stan
#if [ $? -ne 0 ]; then
cp  ../*.stan stan1366/
#fi
pwd
echo "making..."
rm -f stan1366/stan1366
make stan1366/stan1366
cd ./stan1366/
pwd
START=$(date +%N)
if [ -z $2 ]
then
./stan1366 sample > stanout 2>&1
else
./stan1366 sample num_samples=$2 > stanout 2>&1
fi


nans=`grep -wi "shapes must match" stanout | wc -l`
if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi


