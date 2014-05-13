#!/bin/bash
set -u

#
# parameteres from octotron system will look like:
# $1 - timestamp
# $2 - event ta
# $3 - mesagge
# $4 - object aatributes
# $5 - parent attributes or empty string
#

# this is general format for reporting about events
if [ "$#" -eq 5 ]
then
	event_time=`date -d @$1`
	MSG="event: $2\nmessage: $3\ntime: $event_time\nattributes: $4\nparent attributes: $5"
else
	echo "wrong number of parameteres, can not form the info message"
	exit -1
fi

