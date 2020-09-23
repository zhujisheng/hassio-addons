#!/usr/bin/with-contenv bashio

python3 -m http.server -d /audio/ 8000 > /dev/null 2>&1 &

python3 run.py 2>&1

#while [[ true ]]; do
#    sleep 1
#done