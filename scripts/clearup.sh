#!/bin/bash
work_dir="/data/forilen/Kikyou/logs"
cd $work_dir 
sleep 20

cat *.log > db.data
/usr/local/mysql/bin/mysql -uroot -p1234 -e "load data infile '$work_dir/db.data' into table Kikyou.srvMonitor_srvstatus;"
rm *.log
