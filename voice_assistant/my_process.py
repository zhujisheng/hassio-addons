import os, json
from requests import post, get
from fuzzywuzzy import process

# 根据实际需求改写这部分内容
commands = { 1:'现在几度',
             2:'温度多少',
             3:'打开客厅灯',
             4:'关上客厅灯',
             5:'打开厨房灯',
             6:'关上厨房灯'
            }

# 开放的http服务主机名和端口（其中包含ding.wav和dang.wav）
with open('/etc/hostname') as r:
  hostname = r.read().split('\n')[0]
  port = 8000

# 访问HA的http请求head
headers = {
    "Authorization": "Bearer " + os.getenv('SUPERVISOR_TOKEN'),
    "content-type": "application/json",
}

def get_state(entity_id, attribute=None):
  """获得HomeAssistant中某个实体的状态或者某个属性值"""
  url = "http://supervisor/core/api/states/%s"%(entity_id)
  value = get(url, headers=headers)
  try:
    if attribute:
      return value.json()["attributes"][attribute]
    else:
      return value.json()["state"]
  except:
    print("The intents return format is wrong: ", value.text, flush=True)
    return value.text

def post_service( service, data=None ):
  """调用HomeAssistant的服务"""
  url = "http://supervisor/core/api/services/%s"%(service.replace('.','/'))
  return post(url, headers=headers, json=data)


def play_tts( speech_out, tts, media_player ):
  """HomeAssistant API调用: 播放文本的音频"""
  url = "http://supervisor/core/api/services/%s"%(tts.replace('.','/'))
  data = { "entity_id": media_player,
           "message": speech_out
         }
  return post(url, headers=headers, json=data)

def waken( tts='tts.google_translate_say', media_player='all' ):
  """唤醒后的处理函数"""
  data = { "entity_id": media_player,
           "media_content_id": "http://%s:%d/%s"%(hostname,port,"ding.wav"),
           "media_content_type": "music"
         }
  post_service( "media_player.play_media", data )

def recvd( tts='tts.google_translate_say', media_player='all' ):
  """语音命令接收完成后的处理函数"""
  play_tts( '收到！', tts, media_player )

def react( speech_in, tts='tts.google_translate_say', media_player='all' ):
  """获得语音命令文本后的处理函数"""

  match = process.extractOne( speech_in, commands )
  if match[1] < 10:
    command_num = 0
  else:
    command_num = match[2]

  # 根据实际情况改写这部分内容
  speech_out = None
  if command_num==1 or command_num==2:
    speech_out = "当前室外%s度"%(get_state('weather.wo_de_jia','temperature'))
  elif command_num==3:
    post_service( "light.turn_on", {"entity_id": "light.xiaomi_light"})
    speech_out = "客厅灯已打开"
  elif command_num==4:
    post_service( "light.turn_off", {"entity_id": "light.xiaomi_light"})
    speech_out = "客厅灯已关闭"
  elif command_num==5:
    post_service( "light.turn_on", {"entity_id": "light.chu_light"})
    speech_out = "厨房灯已打开"
  elif command_num==6:
    post_service( "light.turn_off", {"entity_id": "light.chu_light"})
    speech_out = "厨房灯已关闭"
  else:
    speech_out = "对不起，我不懂你在说什么"

  if speech_out:
    play_tts( speech_out, tts, media_player )
