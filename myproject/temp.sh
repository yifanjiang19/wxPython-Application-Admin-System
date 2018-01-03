#!/bin/sh
#
# Script prints gdb stack of the process with a specified pid

if [ -z $1 ]; then
	echo "Usage: $0 pid"
	exit 1
fi

PID=$1
BINARY=`ps -o comm= -p $PID`
SCRIPT_DIR=`dirname $0`

if [ -z "$BINARY" ]; then
	echo "Cannot determine binary"
	exit 1
fi

TMPFILE=`mktemp -t pstack.XXXXXX` || exit 1
trap "rm -f $TMPFILE" exit
echo "thread apply all bt\ndetach\nquit" > $TMPFILE

/usr/local/bin/gdb -q -x $TMPFILE "$BINARY" $PID
