#!/usr/bin/env python3

import os, re, socket, json, time
from requests import post
from runner import PreciseEngine, PreciseRunner

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
    return None
  elif(re.match(r'^.*:\d+$',name)):
    stream = SocketReadStream(name)
  else:
    print("configuration input_device format error, use local_default",flush=True)
    stream = None
  return stream

CONFIG_PATH = "/data/options.json"
with open(CONFIG_PATH) as fp:
  config = json.load(fp)

options = config['models']

matches = {}
def on_prediction(show, input_device, model, prob):
    if show:
        matches[(input_device,model)].append(prob)

headers = {
    "Authorization": "Bearer " + os.getenv('SUPERVISOR_TOKEN'),
    "content-type": "application/json",
}

for option in options:
    input_device = option["input_device"]
    model_file = option["model_file"]
    threshold = option["threshold"]
    show_match_level_realtime = option["show_match_level_realtime"]
    url = "http://supervisor/core/api/events/" + option["event_type"]
    matches[(input_device,model_file)]=[]
    stream_in = get_input_stream(input_device)
    engine = PreciseEngine('/precise-engine/precise-engine',
                           model_file)
    runner = PreciseRunner(engine,
                           stream = stream_in,
                           on_activation=eval("lambda: post('%s', headers=headers)"%(url)),
                           on_prediction=eval("lambda x: on_prediction(%s, '%s', '%s', x)"%(show_match_level_realtime,input_device,model_file)),
                           sensitivity = 1.0-option["threshold"]
                           )
    runner.start()

while(True):
    time.sleep(1)
    for m in matches:
      if(len(matches[m])>0):
        max_match = max(matches[m])
        matches[m].clear()
        print('the match level of %s-%s: %.2f' % (m[0], m[1], max_match), flush=True)
