#!/bin/bash
#cd /data/forilen/Kikyou/Kikyou_web
nohup uwsgi --ini /usr/local/nginx/conf/uwsgi.ini &
echo -e "Kikyou start ok!"
