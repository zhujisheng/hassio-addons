#!/usr/bin/with-contenv bashio

if [ ! -e /share/voice_assistant ]; then
    mkdir -p /share/voice_assistant
    cp /process_programs/* /share/voice_assistant 
fi

#if [ ! -e /config/www ]; then
#    mkdir -p /config/www
####    ha core restart
#fi

if [ ! -e /config/www/voice_assistant ]; then
    mkdir -p /config/www/voice_assistant
    cp /audio/* /config/www/voice_assistant/
fi

python3 run.py 2>&1

#while [[ true ]]; do
#    sleep 1
#done