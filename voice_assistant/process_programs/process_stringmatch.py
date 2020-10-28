'''
模糊匹配用户输入的语音命令，分别进行处理。
'''

from fuzzywuzzy import process
import ha_api

# 根据实际需求改写这部分内容
commands = { 1:'现在几度',
             2:'温度多少',
             3:'打开客厅灯',
             4:'关上客厅灯',
             5:'打开厨房灯',
             6:'关上厨房灯'
            }

def on_wake( va_config ):
  """唤醒后的处理函数"""
  ha_api.play_audio_file(va_config["media_player"], "ding.wav")

def on_command( va_config ):
  """语音命令接收完成后的处理函数"""
  ha_api.play_tts( '收到！', va_config["tts_service"], va_config["media_player"] )

def on_react( speech_in, va_config ):
  """获得语音命令文本后的处理函数"""

  match = process.extractOne( speech_in, commands )
  if match[1] < 10:
    command_num = 0
  else:
    command_num = match[2]

  # 根据实际情况改写这部分内容
  speech_out = None
  if command_num==1 or command_num==2:
    speech_out = "当前室外%s度"%(ha_api.get_state('weather.wo_de_jia','temperature'))
  elif command_num==3:
    ha_api.post_service( "light.turn_on", {"entity_id": "light.xiaomi_light"})
    speech_out = "客厅灯已打开"
  elif command_num==4:
    ha_api.post_service( "light.turn_off", {"entity_id": "light.xiaomi_light"})
    speech_out = "客厅灯已关闭"
  elif command_num==5:
    ha_api.post_service( "light.turn_on", {"entity_id": "light.chu_light"})
    speech_out = "厨房灯已打开"
  elif command_num==6:
    ha_api.post_service( "light.turn_off", {"entity_id": "light.chu_light"})
    speech_out = "厨房灯已关闭"
  else:
    speech_out = "对不起，我不懂你在说什么"

  if speech_out:
    ha_api.play_tts( speech_out, va_config["tts_service"], va_config["media_player"] )
