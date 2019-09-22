#!/usr/bin/env bash
cd $1
if [ ! -e ./pyvirtual ]
then
    python2 -m virtualenv pyvirtual
    ./pyvirtual/bin/pip install Cython==0.19 numpy
     ./pyvirtual/bin/pip install pystan==2.2.0.0
fi

# translate template to stan
here=`realpath .`
echo $here
(cd ../../../translators/ && ./teststan.py -o -j $here/stan543.template && cp stan543.stan $here/stan543.stan && cp stan543.json $here/stan543.json)

if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi

if [ -z $2 ]
then
echo "No iterations specified"
timeout 90 ./pyvirtual/bin/python driver.py sampling > stanout 2>&1
else
echo "Samples : $2"
timeout 90 ./pyvirtual/bin/python driver.py sampling $2 > stanout 2>&1
fi
status=$?
echo "$status"
if [ $status -eq 124 ] #timed out
then
    echo "Passed"
    exit 0
else
	nans=`grep -i "Scale parameter is 0:0" stanout | wc -l`
	if [ $nans -gt 0 ]; then
	echo "Passed"
	else
	echo "Failed"
	fi
fi
exit $status



