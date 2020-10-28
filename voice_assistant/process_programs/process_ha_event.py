'''
当智能音箱被唤醒、输入语音命令、语音命令转化为文字后，触发HomeAssistant的事件（事件类型voice_assistant）
'''

import ha_api

def on_wake( va_config ):
  """唤醒后的处理函数"""
  event_data = { "event": "hotword_heard" }
  event_data.update(va_config)
  ha_api.fire_event( "voice_assistant", event_data )

def on_command( va_config ):
  """语音命令接收完成后的处理函数"""
  event_data = { "event": "command_received" }
  event_data.update(va_config)
  ha_api.fire_event( "voice_assistant", event_data )

def on_react( speech_in, va_config ):
  """获得语音命令文本后的处理函数"""
  event_data = { "event": "command_sttd",
                 "command": speech_in }
  event_data.update(va_config)
  ha_api.fire_event( "voice_assistant", event_data )
