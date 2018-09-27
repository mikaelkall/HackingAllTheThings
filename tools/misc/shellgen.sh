#!/bin/bash 
# Mikael Kall
# Use objdump to get the output in opcode format. 

if [ $# == 0 ]; 
then
    echo "Usage: ${0} <filename>"
    exit 0
fi 

filename=${1}

if [ ! -e ${filename} ]; 
then
    echo "${filename} does not exist"
    exit 2
fi

opcodes=$(for i in $(objdump -d ${filename} |grep "^ " |cut -f2); do echo -n '\x'$i; done; echo)
echo ${opcodes}
