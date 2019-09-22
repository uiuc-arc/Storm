#!/usr/bin/env bash
cd $1
if [ ! -e ./pyvirtual ]
then
    python2 -m virtualenv pyvirtual
    ./pyvirtual/bin/pip install Cython==0.19 numpy scipy
    ./pyvirtual/bin/pip install pystan==2.1.0.0

fi

# translate template to stan
here=`realpath .`
echo $here
(cd ../../../translators/ && ./teststan.py -o -j $here/stan499.template && cp stan499.stan $here/stan499.stan && cp stan499.json $here/stan499.json)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi

if [ -z $2 ]
then
echo "No iterations specified"
./pyvirtual/bin/python driver.py sampling >  stanout 2>&1

else
echo "Iterations : $2"
./pyvirtual/bin/python driver.py sampling $2 >  stanout 2>&1

fi
nans=`grep -wi "require matching sizes" stanout | wc -l`

if [ $nans -gt 0 ]; then
echo "Passed"
else
echo "Failed"
fi




