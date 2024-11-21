#!/bin/bash

# remove previous executions
echo "> Removing 'output.mp4' 'sendcmd.txt'"
rm -rf output.mp4 sendcmd.txt

# generate the sendcmd temp file
python3 generate_sendcmd.py ./example1/input.csv

echo ""
echo "============= SENDCMD ============="
echo ""
cat sendcmd.txt
echo "==================================="
echo ""

ffmpeg -hide_banner -y -i ./example1/input.mp4 -vf 'sendcmd=f=sendcmd.txt,drawbox,drawtext=fontfile=FreeSans.ttf:text=' output.mp4

ffplay output.mp4