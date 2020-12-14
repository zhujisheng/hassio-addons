'''
调用tuling123 API
访问http://www.turingapi.com/，获得您自己的user_id和api_key
'''

import ha_api
import requests

tuling_user_id = '403981'
tuling_api_key = 'ddb64bbf5f47466eae4f3ccb5fab9410'

class tuling123(object):
    def __init__(self, user_id, api_key, base_url='http://openapi.tuling123.com/openapi/api/v2'):
        self._session = requests.Session()

        self._base_url = base_url
        self._base_data = { 'reqType': 0,
                            'userInfo': {
                                'apiKey': api_key,
                                'userId': user_id
                                },
                            'perception': {
                                'inputText': {
                                    'text': ''
                                    }
                                }
                            }


    def command(self, input_sentence):
        data = self._base_data
        data['perception']['inputText']['text'] = input_sentence

        r = self._session.post(url=self._base_url, json = data)
        output = r.json()

        ouput_sentence = None
        for result in output['results']:
            if result['resultType']=='text':
                ouput_sentence = result['values']['text']
                break

        return(ouput_sentence)

tuling = tuling123(user_id=tuling_user_id, api_key=tuling_api_key)


def on_wake( va_config ):
  """唤醒后的处理函数"""
  ha_api.play_audio_file(va_config["media_player"], "ding.wav")

def on_command( va_config ):
  """语音命令接收完成后的处理函数"""
  ha_api.play_audio_file(va_config["media_player"], "dong.wav")

def on_react( speech_in, va_config ):
  """获得语音命令文本后的处理函数"""

  speech_out = tuling.command(speech_in)

  if speech_out:
    ha_api.play_tts( speech_out, va_config["tts_service"], va_config["media_player"] )