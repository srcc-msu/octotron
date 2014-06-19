#!/bin/bash
set -u

#
# parameteres from octotron system will look like:
# $1 - timestamp
# $2 - event type
# $3 - event description
# $4 - object attributes
# $5 - parent attributes or empty string
#

# this is general format for reporting about events
if [ "$#" -eq 5 ]
then
	event_time=`date -d @$1`

	if [ -z "$5" ]
	then
		MSG="event: $2\ndescription: $3\ntime: $event_time\nattributes: $4"
	else
		MSG="event: $2\ndescription: $3\ntime: $event_time\nattributes: $4\nparent attributes: $5"
	fi
else
	echo "wrong number of parameteres, can not form the info message"
	exit -1
fi

