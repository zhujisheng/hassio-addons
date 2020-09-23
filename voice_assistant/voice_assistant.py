import os
from requests import post

# 开放的http服务主机名和端口（其中包含ding.wav和dang.wav）
with open('/etc/hostname') as r:
  hostname = r.read().split('\n')[0]
  port = 8000

# 访问HA的http请求head
headers = {
    "Authorization": "Bearer " + os.getenv('SUPERVISOR_TOKEN'),
    "content-type": "application/json",
}

def play_media( media_player, filename ):
  """HomeAssistant API调用: 播放媒体文件。"""
  url = "http://supervisor/core/api/services/media_player/play_media"
  data = { "entity_id": media_player,
           "media_content_id": "http://%s:%d/%s"%(hostname,port,filename),
           "media_content_type": "music"
         }
  return post(url, headers=headers, json=data)

def play_tts( speech_out, tts, media_player ):
  """HomeAssistant API调用: 播放文本的音频"""
  url = "http://supervisor/core/api/services/%s"%(tts.replace('.','/'))
  data = { "entity_id": media_player,
           "message": speech_out
         }
  return post(url, headers=headers, json=data)


def intent_process( speech_in ):
  """HomeAssistant API调用: conversation/process"""
  url = "http://supervisor/core/api/conversation/process"
  data = { "text": speech_in }
  r = post(url, headers=headers, json=data)
  try:
    return r.json()['speech']['plain']['speech']
  except:
    print("The intents return format is wrong: ", r.text, flush=True)
    return r.text

def waken( tts='tts.google_translate_say', media_player='all' ):
  """唤醒后的处理函数"""
  play_media(media_player, "ding.wav")

def recvd( tts='tts.google_translate_say', media_player='all' ):
  """读入语音命定后的处理函数"""
  play_media(media_player, "dong.wav")

def react( speech_in, tts='tts.google_translate_say', media_player='all' ):
  """获得语音命令文本后的处理函数"""
  speech_out = intent_process( speech_in )
  play_tts( speech_out, tts, media_player )
