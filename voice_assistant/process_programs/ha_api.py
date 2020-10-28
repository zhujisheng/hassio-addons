import os
from requests import get, post

# 访问HA的http请求head
headers = {
    "Authorization": "Bearer " + os.getenv('SUPERVISOR_TOKEN'),
    "content-type": "application/json",
}

discovery_info = get("http://supervisor/core/api/discovery_info", headers=headers).json()
ha_base_url = discovery_info["internal_url"] or discovery_info["external_url"]

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

def fire_event(event_type, event_data):
  """触发HomeAssistant的事件"""
  url = f"http://supervisor/core/api/events/{event_type}"
  result = post(url, headers=headers, json=event_data)
  return result.ok

def play_tts( speech_text, tts, media_player ):
  """HomeAssistant API调用: 播放文本的音频"""
  data = { "entity_id": media_player,
           "message": speech_text
         }
  return post_service(tts, data=data)

def play_audio_file( media_player, filename ):
  """HomeAssistant API调用: 播放媒体文件（ding&dong）。"""
  data = { "entity_id": media_player,
           "media_content_id": f"{ha_base_url}/local/voice_assistant/{filename}",
           "media_content_type": "music"
         }
  return post_service("media_player.play_media", data=data)

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
