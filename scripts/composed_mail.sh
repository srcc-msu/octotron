#!/bin/bash
#
# aggregates mails to send them in big chunks
# sends the mail if the time threshold is reached (MTIME_LIMIT)
# or if mail threshold is reached (MAIL_LIMIT)
#
# $1 - recipient
# $2 - subject
# $3 - msg
set -u

MTIME_LIMIT=30
MAIL_LIMIT=100

# exit if empty recipient
if [ -z "$1" ]; then
	echo "error: empty recipient"
    exit 1
fi

HASH=`echo $1 | md5sum| cut -f1 -d" "`

LOCK_FILE=/tmp/octo_$HASH.lock
OUT_FILE=/tmp/octo_$HASH.tmp
SUBJ=Subject

# get lock
lockfile $LOCK_FILE

# add to the buffer
echo >> $OUT_FILE
echo '***' >> $OUT_FILE
echo >> $OUT_FILE
echo $SUBJ : "$2" >> $OUT_FILE
echo -e "$3" >> $OUT_FILE

rm -f $LOCK_FILE

sleep $MTIME_LIMIT
sleep 2 # o_O # some addititional sleep to ensure correct time

lockfile $LOCK_FILE

cur_time=`date +%s`
mod_time=`stat -c %Y $OUT_FILE`

MAILS=`cat $OUT_FILE | grep $SUBJ | wc -l`

DANGER=`cat $OUT_FILE | grep $SUBJ | grep DANGER | wc -l`
CRITICAL=`cat $OUT_FILE | grep $SUBJ | grep CRITICAL | wc -l`
WARNING=`cat $OUT_FILE | grep $SUBJ | grep WARNING | wc -l`
INFO=`cat $OUT_FILE | grep $SUBJ | grep INFO | wc -l`
RECOVER=`cat $OUT_FILE | grep $SUBJ | grep RECOVER | wc -l`

# if it is true - probably i was last who changed the file
# if i was not - it does not matter, i can check conditions anyway
if [ $(($cur_time - $mod_time)) -gt $MTIME_LIMIT ]
then

# send all if the time file is too old and there are some data
	if [[ "$MAILS" -gt 1 ]]
	then
		echo "sending - old data"
		cat $OUT_FILE | mail -s "Octotron($MAILS): CRITICAL: $CRITICAL DANGER: $DANGER WARNING: $WARNING INFO: $INFO RECOVER: $RECOVER" "$1"
		> $OUT_FILE
	fi

# send if there is just one
	if [[ "$MAILS" -eq 1 ]]
	then
		echo "sending - single"
		subj=`sed -n '4p' $OUT_FILE`
		msg=`tail -n+5 $OUT_FILE`
		bash ./single_mail.sh "$1" "$subj" "$msg"
		> $OUT_FILE
	fi
# send if there are too many data
elif [[ "$MAILS" -gt $MAIL_LIMIT ]];
then
	echo "sending - many data"
	cat $OUT_FILE | mail -s "Octotron($MAILS): CRITICAL: $CRITICAL DANGER: $DANGER WARNING: $WARNING INFO: $INFO RECOVER: $RECOVER" "$1"
	> $OUT_FILE
fi

rm -f $LOCK_FILE
