# Home Assistant Add-on: Mycroft Precise

When some particular voice is caught, this add-on produce an event in HomeAssistant.

## About

[Mycroft Precise](https://github.com/MycroftAI/mycroft-precise)is a wake word listener service based on recurrent neural networks.

This Add-on is based on mycroft-precise. When it heard a particular voice, it produce an event in HomeAssistant.

## Config

#### `input_device`

The audio input device.

- The value can be `local_default`, which means to use the audio input device configed in the add-on configuration.

- remote microphone: `ip:port`, for example`192.168.1.120:3344`

There's more information about the remote microphone in the vedio lesson [HomeAssistant Practice](https://study.163.com/course/courseMain.htm?courseId=1006189053&share=2&shareId=400000000624093): [Remote Microphone Connected to HomeAssistant](https://study.163.com/course/courseLearn.htm?courseId=1006189053&share=2&shareId=400000000624093#/learn/video?lessonId=1279002359&courseId=1006189053)

You can also find the documents and programs about remote mic [here](https://github.com/zhujisheng/Home-Assistant-DIY/blob/master/%E5%8F%82%E8%80%83%E6%96%87%E6%A1%A3%EF%BC%8821-30%EF%BC%89/24.%E8%BF%9C%E7%A8%8B%E9%BA%A6%E5%85%8B%E9%A3%8E.pdf), [here](https://github.com/zhujisheng/audio-reactive-led-strip), or [here](https://github.com/zhujisheng/audio-reactive-led-strip/tree/master/DistributedMicrophone).

#### Option `model_file`

The model file of the wake voice.

Model file `/cough.pb` and `/hey-mycroft.pb` are fre-put in the add-on, which is waked by the voice of cough, and the pronoucation of 'hey, mycroft'

#### Option `threshold`

The trigger threshold. If the match level of current audio and model is bigger than te thresold, an event will appear in HomeAssistant. 

Both the threshold and match level, are numbers between 0 and 1.

#### Option `event_type`

The event type appears in HomeAssistant.

#### Option `show_match_level_realtime`

Value `true` or `false`.

It's the switch to turn on the logger of current match level in Add-on, once per second.

Notice: the logger can be used to determine the proper value of the option `threshold`, and the logger will only show after it's refreshed by hand.

## Create Your Own Wake Voice Model File

You can create your own wake voice model file in mycroft-precise.

- Creation

  [https://github.com/MycroftAI/mycroft-precise/wiki/Training-your-own-wake-word](https://github.com/MycroftAI/mycroft-precise/wiki/Training-your-own-wake-word)

- Configuration

  By using `Add-on:Samba`, you can put the model file `xxxxx.pb` and `xxxxx.pb.params`(or`xxx.net`) in the shared dir `share/`.

  Configure the option `model_file`, set it to be `/share/xxxxx.pb`(or `/share/xxxxx.net`).