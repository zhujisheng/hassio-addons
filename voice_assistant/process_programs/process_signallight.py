'''
使用信号灯完成语音输入的相关提示
'''

import ha_api

signal_light = "light.miclight"

def on_wake( va_config ):
  """唤醒后的处理函数: 闪烁远程麦克风上的灯"""
  data = { "entity_id": signal_light,
           "effect": "Strobe"
         }
  ha_api.post_service( "light.turn_on", data )

def on_command( va_config ):
  """语音命令接收完成后的处理函数"""
  data = { "entity_id": signal_light,
           "effect": "None",
           "brightness": 255
         }
  ha_api.post_service( "light.turn_on", data )

def on_react( speech_in, va_config ):
  """获得语音命令文本后的处理函数"""
  speech_out = f"你对我说，{speech_in}。但是我还没有想好怎么处理它。"
  ha_api.play_tts( speech_out, va_config["tts_service"], va_config["media_player"] )

  data = { "entity_id": signal_light }
  ha_api.post_service( "light.turn_off", data )