'''
使用HomeAssistant的conversation和intent_script组件完成智能处理过程
'''

import ha_api

def on_wake( va_config ):
  """唤醒后的处理函数"""
  ha_api.play_audio_file(va_config["media_player"], "ding.wav")

def on_command( va_config ):
  """读入语音命定后的处理函数"""
  ha_api.play_audio_file(va_config["media_player"], "dong.wav")

def on_react( speech_in, va_config ):
  """获得语音命令文本后的处理函数"""
  speech_out = ha_api.intent_process( speech_in )
  ha_api.play_tts( speech_out, va_config["tts_service"], va_config["media_player"] )
