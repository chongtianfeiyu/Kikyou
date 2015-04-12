#!/bin/bash
#获取服务器当前状态

PATH=$PATH:/usr/bin:/bin
eth_vlan="eth0"
disk_data="vg_252-lv_home"
disk_root="vg_252-lv_root"
log_dir="/data/forilen/Kikyou/logs"
rsync_srv="192.168.100.252"
rsync_dir="srvstatus"

ip_vlan=`/sbin/ifconfig $eth_vlan | grep Bcast |awk '{print $2}' |awk 'BEGIN {FS=":"} {print $2}'`
# echo "$ip_vlan"
cpu_load5=`cat /proc/loadavg | awk '{print $1}'`
cpu_load10=`cat /proc/loadavg | awk '{print $2}'`
cpu_load15=`cat /proc/loadavg | awk '{print $2}'`

# echo "$cpu_load5"
mem_used=`/usr/bin/free | grep Mem | awk '{print ($3/$2)}'`
tcp_estab=`netstat -tn | grep ESTABLISHED | wc -l | awk '{print $1}'`

traffic_be_in=`cat /proc/net/dev |grep $eth_vlan | awk -F: '{print $2}' | awk '{print $1}'`
traffic_be_out=`cat /proc/net/dev |grep $eth_vlan | awk -F: '{print $2}' | awk '{print $9}'`
sleep 10
traffic_af_in=`cat /proc/net/dev |grep $eth_vlan | awk -F: '{print $2}' | awk '{print $1}'`
traffic_af_out=`cat /proc/net/dev |grep $eth_vlan | awk -F: '{print $2}' | awk '{print $9}'`

# echo "$traffic_be_in"
# echo "$traffic_be_out"
# echo "$traffic_af_in"
# echo "$traffic_af_out"
eth_in=$[$[$traffic_af_in-$traffic_be_in]/5]
eth_out=$[$[$traffic_af_out-$traffic_be_out]/5]

# echo "$eth_in"
# echo "$eth_out"

disk_used_root=`df -h -P | grep $disk_root  |awk '{print $5}'`
disk_used_data=`df -h -P | grep $disk_data  |awk '{print $5}'`

inode_used_root=`df -i -P | grep $disk_root  |awk '{print $5}'`
inode_used_data=`df -i -P | grep $disk_data  |awk '{print $5}'`

alert_level=0
srv_status=1
ts=`date +"%Y-%m-%d %H:%M:%S"`

#*****alert discribtion*****
#cpu load =1
#eth in =2
#eth out=4
#disk used =8
#inode used =16

if [ -f "$log_dir/$ip_vlan.log" ]
then
	bf_eth_in=`cat $log_dir/$ip_vlan.log | awk '{print $8}'`
	bf_eth_out=`cat $log_dir/$ip_vlan.log | awk '{print $9}'`
	eth_in_min=$[$bf_eth_in/5]
	echo $eth_in
	echo $eth_in_min
	eth_in_max=$[$bf_eth_in*5]
	echo $eth_in_max
	eth_out_min=$[$bf_eth_out/5]
	eth_out_max=$[$bf_eth_out*5]

	if [ $eth_in -gt $eth_in_max -o $eth_in -lt $eth_in_min ]
	then
		alert_level=$[$alert_level+2]
		echo $alert_level
	fi
	if [ $eth_out -gt $eth_out_max -o $eth_out -lt $eth_out_min ]
	then
		alert_level=$[$alert_level+4]
	fi
	rm -rf $log_dir/$ip_vlan.log
fi

cpu_num=`cat /proc/cpuinfo | grep processor | wc -l`
if [ $cpu_load5 -gt $cpu_num -o $cpu_load5 -gt $cpu_num ]
then
	alert_level=$[$alert_level+1]
fi


echo -e "null \t$ip_vlan \t$cpu_load5 \t$cpu_load10 \t$cpu_load15 \t$mem_used \t$tcp_estab \t$eth_in \t$eth_out \t$disk_used_root \t$disk_used_data \t$inode_used_root \t$inode_used_data \t$alert_level \t$srv_status \t$ts" >>$log_dir/$ip_vlan.log

# /usr/local/mysql/bin/mysql -uroot -p1234 -e "load data infile '$log_dir/$ip_vlan.log' into table Kikyou.srvMonitor_srvstatus;"
# rsync -az $log_dir/$ip_vlan.log root@$rsync_srv::$rsync_dir