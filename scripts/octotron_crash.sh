#!/bin/bash
#
# $1 - filename with error description -
# it will be generated by the system
#
set -u
cd "$(dirname "$0")"

source ./mail_config.sh

if [ $# -eq 1 ]
then
	msg=`cat $1`
else
	msg=""
fi

if [ -z "$msg" ]
then
	msg="Unknown error"
fi

bash ./single_mail.sh "$RECIPIENT" "$PREFIX Octotron CRASHED" "$msg"
