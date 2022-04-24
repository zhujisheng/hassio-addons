#!/usr/bin/with-contenv bashio

if [ ! -e /share/voice_assistant ]; then
    mkdir -p /share/voice_assistant
    cp /process_programs/* /share/voice_assistant 
fi

if [ ! -e /media/voice_assistant ]; then
    mkdir -p /media/voice_assistant
    cp /audio/* /media/voice_assistant/
fi

python3 run.py 2>&1

#while [[ true ]]; do
#    sleep 1
#done