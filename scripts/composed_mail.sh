#!/bin/bash
#
# aggregates mails to send them in big chunks
# sends the mail if the time threshold is reached ($MTIME_LIMIT)
# if aggregated count is low (less than $SEP_LIMIT) - sends them separately
#
# $1 - recipient
# $2 - subject
# $3 - msg
set -u

source ./mail_config.sh

script_loc=$(readlink -f "$0")
cd "$(dirname "$script_loc")"

MTIME_LIMIT=30
SEP_LIMIT=3

# exit if have not got enough params
if [ $# -ne 3 ]
then
	echo "error: wrong params"
    exit 1
fi

HASH=`echo $1 | md5sum | cut -f1 -d" "`
MAIL_DIR=/tmp/octo_$HASH

# assuming dir exists
function add_mail
{
	until echo -e "$SUBJ_STR: $2\n$3" > `mktemp --tmpdir=$MAIL_DIR`
	do
		echo "failed to add mail, retrying" >&2
		sleep 1
		exec $script_loc "$1" "$2" "$3"
	done
}

SUBJ_STR="Subject"

# if i am the owner
if mkdir $MAIL_DIR &> /dev/null
then
	add_mail "$1" "$2" "$3"

	sleep $MTIME_LIMIT

	SEND_DIR=$MAIL_DIR.$$
	mv $MAIL_DIR $SEND_DIR

	COUNT=`ls -1 $SEND_DIR | wc -l`

	if [[ $COUNT -le $SEP_LIMIT ]]
	then
		for file in $SEND_DIR/*
		do
			SUBJ=`head -n1 $file`
			tail -n+2 $file | bash ./single_mail.sh "$1" "$SUBJ"
		done

	else
		OUT_FILE=`mktemp`

		for file in $SEND_DIR/*
		do
			echo >> $OUT_FILE
			echo '***' >> $OUT_FILE
			echo >> $OUT_FILE
			cat $file >> $OUT_FILE
		done

		DANGER=`cat $OUT_FILE | grep $SUBJ_STR | grep DANGER | wc -l`
		CRITICAL=`cat $OUT_FILE | grep $SUBJ_STR | grep CRITICAL | wc -l`
		WARNING=`cat $OUT_FILE | grep $SUBJ_STR | grep WARNING | wc -l`
		INFO=`cat $OUT_FILE | grep $SUBJ_STR | grep INFO | wc -l`
		RECOVER=`cat $OUT_FILE | grep $SUBJ_STR | grep RECOVER | wc -l`

		cat $OUT_FILE | sed 's/Subject: //' | bash ./single_mail.sh "$1" "$PREFIX Octotron($COUNT): Critical: $CRITICAL Danger: $DANGER Warning: $WARNING Info: $INFO Recover: $RECOVER"
		rm $OUT_FILE
	fi
		rm -rf $SEND_DIR
else
	add_mail "$1" "$2" "$3"
fi
