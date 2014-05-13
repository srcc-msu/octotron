#!/bin/bash
# sends a single mail
# $1 - recipient
# $2 - subject
# $3 - msg, if $3 not specified - stdin will be used

if [ $# -eq 3 ]
then
	echo -e "$3" | mail -s "$2" "$1"
elif [ $# -eq 2 ]
then
	mail -s "$2" "$1" <&0
else
	echo "wrong params count"
fi
