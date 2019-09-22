#!/usr/bin/env bash

# dependencies
sudo apt -y update
sudo apt -y upgrade
sudo apt install maven make python2.7 python-pip python-virtualenv
sudo pip2 install antlr4-python2-runtime numpy==1.13.0 scipy==1.2.0 six
# install cmdstan or pyvirtual
for d in `ls -d bugs/templates/stan*`;
do
echo "$d"
dd=`find $d -name "cmdstan*"`
pyv=`find $d -name "pyvirtual*"`
if [  -z "$dd" ] && [ -z "$pyv" ]; then
  (cd $d; ./run.sh .)
fi
done

for d in `ls -d bugs/templates/probfuzz/*`;
do
echo "$d"
pyv=`find $d -name "pyvirtual*"`
if [ -z "$pyv" ]; then
  (cd $d; ./run.sh .)
fi
done

for d in `ls -d bugs/templates/pyro/*`;
do
echo "$d"
pyv="find $d -name \"pyvirtual*\""
if [ -z "$pyv" ]; then
  (cd $d; ./run.sh .)
fi
done



mvn package