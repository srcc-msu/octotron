#!/bin/bash
set -u

#
# parameteres from octotron system will look like:
# $1 - event type
# $2 - json log entry
# $3, ... - event messages
#

# this is general format for reporting about events
# trying to extract `tag` and `msg` from
# user messages to form a short subject string

DATA="[`date`]"

TAG=""
MSG=""

for param in "${@:3}"
do
	DATA+="\n\n$param"

	if [[ $param == *tag:* ]]
	then
		TAG+=$param
	fi

	if [[ $param == *msg:* ]]
	then
		MSG+=$param
	fi
done

SHORT="$1 $TAG $MSG"

DATA+="\n\n$2"
