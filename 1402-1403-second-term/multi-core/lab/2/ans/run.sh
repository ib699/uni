#!/bin/bash

#read -p "enter matrix x:" x
#read -p "enter matrix y:" y

#1 M
x=512
y=512

# 10 M
#x=1619
#y=1619

g++ -o matadd matadd.cpp -Im -fopenmp
./matadd $x $y
