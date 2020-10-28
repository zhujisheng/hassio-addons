'''
叮咚提示音
使用ha的tts服务进行回复
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
  speech_out = f"你对我说，{speech_in}。但是我还没有想好怎么处理它。"
  ha_api.play_tts( speech_out, va_config["tts_service"], va_config["media_player"] )
