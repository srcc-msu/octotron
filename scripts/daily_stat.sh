#!/bin/bash
set -u
cd "$(dirname "$0")"

source ./mail_config.sh

DATE=`date +%Y_%m_%d`
FILE="../log/octotron.events.verbose.log."$DATE

if [ -e $FILE ]
then
	python daily_stat.py -f $FILE 2> log/daily.errors.`date`.log | bash ./single_mail.sh "$RECIPIENT" "$PREFIX[daily]: all events for $DATE"
else
	bash ./single_mail.sh "$RECIPIENT" "$PREFIX [daily]: no events for $DATE" "no events"
fi
