#!/bin/bash
set -u

#
# parameteres from octotron system will look like:
# $1 - timestamp
# $2 - event type
# $3, ... - event messages
#

# this is general format for reporting about events
event_time=`date -d @$1 "+%x %X"`

MSG="[$event_time] -- $2: $3"

for param in "${@:4}"
do
	MSG+="\n\n$param"
done
