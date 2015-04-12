#!/bin/bash
PROJDIR="/data/forilen/Kikyou/Kikyou_web" 
PIDFILE="$PROJDIR/Kikyou_web.pid" 
SOCKET="$PROJDIR/Kikyou_web.sock" 
cd $PROJDIR 
if [ -f $PIDFILE ]
then 
	kill cat -- $PIDFILE 
	rm -f — $PIDFILE 
fi 
/usr/bin/python ./manage.py runfcgi socket=$SOCKET pidfile=$PIDFILE 
# /bin/chown root.root $SOCKET