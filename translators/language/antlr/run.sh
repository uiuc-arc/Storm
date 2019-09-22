#!/bin/bash
mydir=`pwd`
echo "[Updating grammar...]"
# first update the grammar repo
(cd ../grammars/ && git pull origin master)

# then build grammar
echo "[Building grammar...]"
(cd ../grammars/ && ./build.sh -l Python2 -o $mydir -p tool.parser -g template/Template2.g4)
echo "[Done...]"