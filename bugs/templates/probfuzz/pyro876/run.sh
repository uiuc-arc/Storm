#!/usr/bin/env bash
cd $1
if [ ! -e ./pyvirtual ]
then
    python2 -m virtualenv pyvirtual
    ./pyvirtual/bin/pip install pyro-ppl==0.1.2 torch==0.3.1 numpy scipy

fi
curpath=`realpath pyro876.template`
here=`realpath .`
initcontent=`cat pyro876.py`
if [ -z $2 ]
then
(cd ../../../../translators && ./test012.py $curpath -a SVI && mv pyro876.py $here/pyro876.py) > output 2>&1
else
(cd ../../../../translators && ./test012.py $curpath -a SVI -it $2 && mv pyro876.py $here/pyro876.py) > output 2>&1
fi
if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi


curcontent=`cat pyro876.py`
diff <(echo "$initcontent") <(echo "$curcontent")

echo "Running pyro program..."
./pyvirtual/bin/python pyro876.py >> output  2>&1

err=`grep -i "double without overflow" output | wc -l`
if [ $err -gt 0 ]; then
echo "Passed"
else
echo "Failed"
echo "***************error**************"
cat output
echo "**************error-end***********"
fi