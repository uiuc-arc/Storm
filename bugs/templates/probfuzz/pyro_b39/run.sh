#!/usr/bin/env bash
cd $1
if [ ! -e ./pyvirtual ]
then
     python2 -m virtualenv pyvirtual
    ./pyvirtual/bin/pip install https://download.pytorch.org/whl/cpu/torch-0.3.0.post4-cp27-cp27mu-linux_x86_64.whl
    ./pyvirtual/bin/pip install pyro-ppl==0.1.2
fi

curpath=`realpath pyro_b39.template`
here=`realpath .`
initcontent=`cat pyro_b39.py`
if [ -z $2 ]
then
(cd ../../../../translators && ./test012.py $curpath -a SVI && mv pyro_b39.py $here/pyro_b39.py) > output 2>&1
else
(cd ../../../../translators && ./test012.py $curpath -a SVI -it $2 && mv pyro_b39.py $here/pyro_b39.py) > output 2>&1
fi
if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi

curcontent=`cat pyro_b39.py`
diff <(echo "$initcontent") <(echo "$curcontent")

echo "Running pyro program..."
./pyvirtual/bin/python pyro_b39.py >> output 2>&1

err=`grep -i "domain error in arguments" output | wc -l`
if [ $err -gt 0 ]; then
echo "Passed"
else
echo "Failed"
echo "***************error**************"
cat output
echo "**************error-end***********"
fi
