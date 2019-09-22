#!/usr/bin/env bash
cd $1
if [ ! -e ./pyvirtual ]
then
    python2 -m virtualenv pyvirtual
    ./pyvirtual/bin/pip install pyro-ppl==0.2.0 torch==0.4.0 numpy scipy

fi
curpath=`realpath eight_schools_020.template`
here=`realpath .`
initcontent=`cat eight_schools_020.py`
if [ -z $2 ]
then
(cd ../../../../translators && ./test.py $curpath -a SVI && mv eight_schools_020.py $here/eight_schools_020.py) > output 2>&1
else
(cd ../../../../translators && ./test.py $curpath -a SVI -it $2 && mv eight_schools_020.py $here/eight_schools_020.py) > output 2>&1
fi
if [ $? -ne 0 ]; then
echo "Translate failed"
echo "Failed"
exit 2
fi


curcontent=`cat eight_schools_020.py`
diff <(echo "$initcontent") <(echo "$curcontent")

echo "Running pyro program..."
./pyvirtual/bin/python eight_schools_020.py >> output  2>&1

err=`grep -i "Expected object of type torch.FloatTensor but found type torch.LongTensor" output | wc -l`
if [ $err -gt 0 ]; then
echo "Passed"
else
echo "Failed"
echo "***************error**************"
cat output
echo "**************error-end***********"
fi