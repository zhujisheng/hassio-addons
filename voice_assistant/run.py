#!/usr/bin/env python3

import json, time, wave, io, subprocess, re, socket, sys, os
#import dns.resolver
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from threading import Thread
from runner import PreciseEngine, TriggerDetector

class SocketReadStream(object):
  """
  A Class only read the socket
  """
  def __init__(self, conn_str):
    r=re.match(r'^(.*):(\d+)$',conn_str)
    self._server = (r.group(1),int(r.group(2)))
    self._buffer = b''
    self._SocketInit()

  def _SocketInit(self):
    self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._sock.settimeout(5)
    self._connected = False

  def read(self, n):
    while len(self._buffer)<n:
      try:
        if not self._connected:
            self._sock.connect(self._server)
            self._connected = True;
            print('Connecting to %s:%d'%self._server, flush=True)

        recvData = self._sock.recv(n-len(self._buffer))
        if len(recvData)==0:
            self._sock.close()
            self._SocketInit()
            print('Receive none from %s:%d, Disconnect it.'%self._server, flush=True)

        self._buffer += recvData

      except socket.timeout:
        print('%s:%d Timeout. Reconnecting ...'%self._server, flush=True)
        self._sock.close()
        self._SocketInit()
      except (socket.error, OSError):
        print('%s:%d Connection failed. Reconnecting after 5s ...'%self._server, flush=True)
        self._sock.close()
        time.sleep(5)
        self._SocketInit()

    chunk = self._buffer[:n]
    self._buffer = self._buffer[n:]
    return chunk

def get_input_stream( name ):
  if(name=="local_default"):
    import pyaudio
    pa = pyaudio.PyAudio()
    stream = pa.open(16000, 1, pyaudio.paInt16, True, frames_per_buffer=CHUCK_SIZE)
    stream.read = lambda x: pyaudio.Stream.read(stream, x // 2, False)
  elif(re.match(r'^.*:\d+$',name)):
    stream = SocketReadStream(name)
  else:
    print("configuration microphone format error",flush=True)
    stream = None
  return stream

def get_func( func_str ):
  import_file = func_str.rsplit('.',1)[0]
  try:
    exec("import " + import_file)
    return eval(func_str)
  except Exception as e:
    print("Can't import", func_str, "----", e)
    return None
  
def get_wav_data( raw_data ):
        # generate the WAV file contents
        with io.BytesIO() as wav_file:
            with wave.open(wav_file, "wb") as wav_writer:
                wav_writer.setframerate(16000)
                wav_writer.setsampwidth(2)
                wav_writer.setnchannels(1)
                wav_writer.writeframes(raw_data)
                wav_data = wav_file.getvalue()
                wav_writer.close()
        return wav_data

def get_flac_data( wav_data ):

  process = subprocess.Popen(["/usr/bin/flac",
                              "--stdout", "--totally-silent",
                              "--best",
                              "-",
                              ],
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=None)
  flac_data, stderr = process.communicate(wav_data)
  return flac_data

def recognize_google_cn(flac_data, language="zh-CN", pfilter=0, show_all=False):

        key = "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"

#        server = 'www.google.com.cn'
#        resolver = dns.resolver.Resolver(configure=False)
#        resolver.nameservers=['8.8.8.8']
#        google_ip=resolver.query(server,'A')[0].address
#
#        url = "http://{}/speech-api/v2/recognize?{}".format(
#                  google_ip,
#                  urlencode({
#                  "client": "chromium",
#                  "lang": language,
#                  "key": key,
#                  "pFilter": pfilter
#                  }))
#        request = Request(url,
#                          origin_req_host=server,
#                          data=flac_data,
#                          headers={"Content-Type": "audio/x-flac; rate=16000"})
        url = "http://www.google.cn/speech-api/v2/recognize?{}".format(urlencode({
                  "client": "chromium",
                  "lang": language,
                  "key": key,
                  "pFilter": pfilter
                  }))
        request = Request(url, data=flac_data, headers={"Content-Type": "audio/x-flac; rate=16000"})

        # obtain audio transcription results
        try:
            response = urlopen(request)
        except HTTPError as e:
            print("recognition request failed: {}".format(e.reason),flush=True)
        except URLError as e:
            print("recognition connection failed: {}".format(e.reason),flush=True)
        response_text = response.read().decode("utf-8")

        # ignore any blank blocks
        actual_result = []
        for line in response_text.split("\n"):
            if not line: continue
            result = json.loads(line)["result"]
            if len(result) != 0:
                actual_result = result[0]
                break

        # return results
        if show_all: return actual_result
        if not isinstance(actual_result, dict) or len(actual_result.get("alternative", [])) == 0:
            print("recognition result error",flush=True)
            return ""

        if "confidence" in actual_result["alternative"]:
            # return alternative with highest confidence score
            best_hypothesis = max(actual_result["alternative"], key=lambda alternative: alternative["confidence"])
        else:
            # when there is no confidence available, we arbitrarily choose the first hypothesis.
            best_hypothesis = actual_result["alternative"][0]
        if "transcript" not in best_hypothesis:
            print("recognition result format error",flush=True)
            return ""
        return best_hypothesis["transcript"]


def handle_predictions( va_config, va_index ):
  """Continuously check Precise process output"""
  microphone = va_config["microphone"]
  wake_word_model = va_config["wake_word_model"]
  threshold = va_config["threshold"]
  show_match_level_realtime = va_config["show_match_level_realtime"]
  on_wake = va_config["on_wake"]
  on_command_stage1 = va_config["on_command_stage1"]
  on_command_stage2 = va_config["on_command_stage2"]
  key = "/".join([microphone, wake_word_model, str(threshold), str(va_index)])
  matches[key] = []

  stream_in = get_input_stream(microphone)
  detector = TriggerDetector(CHUCK_SIZE, 1.0-threshold)
  engine = PreciseEngine('/precise-engine/precise-engine',
                         wake_word_model,
                         chunk_size = CHUCK_SIZE)
  func_on_wake = get_func( on_wake )
  func_on_command_stage1 = get_func( on_command_stage1 )
  func_on_command_stage2 = get_func( on_command_stage2 )
  engine.start()

  try:
    while True:
      chunk = stream_in.read(CHUCK_SIZE)
      prob = engine.get_prediction(chunk)
      if show_match_level_realtime:
        matches[key].append(prob)
      if detector.update(prob):
        print(microphone, "waked", flush=True)
        func_on_wake(va_config)
        audio = stream_in.read(CHUCK_SIZE*CHUCKS_TO_READ)
        func_on_command_stage1(va_config)
        wav_data = get_wav_data( audio )
        flac_data = get_flac_data(wav_data)
        speech_in = recognize_google_cn(flac_data)
        print(microphone, "catch the input speech: ", speech_in, flush=True)
        func_on_command_stage2(speech_in, va_config)
  except Exception as e:
    print("crashed!!!")
    print(e)
    os._exit(1)


sys.path.insert(0,'/share/voice_assistant')

CHUCK_SIZE = 2048
CHUCKS_TO_READ = int(4.5*2*16000/2048)

CONFIG_PATH = "/data/options.json"
with open(CONFIG_PATH) as fp:
  config = json.load(fp)

matches = {}
va_index = 1
for va in config["voice_assistant"]:
  thread = Thread(target=handle_predictions,
                  args=(va, va_index,),
                  daemon=True)
  va_index += 1
  thread.start()


while(True):
    time.sleep(1)
    for key in matches:
      if(len(matches[key])>0):
        max_match = max(matches[key])
        matches[key].clear()
        print('the match level of %s: %.2f' % (key, max_match), flush=True)
