## 【关于】

这是一个智能音箱add-on，在其中集成了以下应用：
- [mycroft-precise](https://github.com/MycroftAI/mycroft-precise/)唤醒词服务，
- google的云端语音识别服务（连接到`http://www.google.cn/speech-api/v2/recognize`）
- 语音命令处理过程可以自定义，其中可以方便调用HomeAssistant的API：
    - 获得HomeAssistant实体的状态和属性值
    - 调用HomeAssistant的服务
    - 触发HomeAssistant中的事件
    - `tts`文字语音播放服务
    - `conversation`和`intent_script`提供的API
- 自定义的语音命令处理过程，详见下面文档


## 【多个语音助理】

在`voice_assistant`下可以配置多个语音助理，每个语音助理对应以下配置参数：

- 一个音频输入设备
- 一个唤醒词模型，以及唤醒相应的参数
- 一个唤醒后调用的函数、一个语音命令输入后调用的函数、一个语音命令识别后调用的函数
- 一个在HomeAssistant中配置的media_player设备
- 一个在HomeAssistant中配置的tts服务

多个语音助理可以使用不同的或相同的配置参数，从而自由定义对不同音频输入设备上的不同唤醒词的不同处理方式。


## 【配置项】

#### `microphone`

音频输入设备。

取值：`local_default`，表示缺省的音频输入设备（在add-on的`audio`配置中选择）。

远程麦克风：配置格式为`ip地址:端口号`，例如`192.168.1.120:3344`

远程麦克风本身的安装与配置，参见相关课程[《HomeAssistant智能家居实战篇》](https://study.163.com/course/courseMain.htm?courseId=1006189053&share=2&shareId=400000000624093)中[《接入HomeAssistant的远程麦克风》](https://study.163.com/course/courseLearn.htm?courseId=1006189053&share=2&shareId=400000000624093#/learn/video?lessonId=1279002359&courseId=1006189053)

#### `wake_word_model`

唤醒词模型文件，系统根目录中带有`hey-mycroft.pb`和`cough.pb`两个模型，分别对应`嘿，麦克若福特`和咳嗽（口哨）音

你可以创建并配置自己的唤醒音模型文件：

- 创建

  参见：[https://github.com/MycroftAI/mycroft-precise/wiki/Training-your-own-wake-word](https://github.com/MycroftAI/mycroft-precise/wiki/Training-your-own-wake-word)

- 配置

  可以通过Add-on:Samba，将制作的模型文件`xxxxx.pb`和`xxxxx.pb.params`（或者`xxx.net`)放置在共享的`share/voice_assistant/`目录中

  在配置中，设置`wake_word_model`为`/share/voice_assistant/xxxxx.pb`(或者`/share/xxxxx.net`)

#### `threshold`

触发语音助理的门槛值：当前声音与模型的匹配度大于门槛值时，开始接收语音命令

匹配度为0到1之间的数；门槛值可设置为0到1之间的数。

门槛值越低，误唤醒概率越高，漏唤醒概率越低。

#### `show_match_level_realtime`

是否在日志中输出当前声音与唤醒词模型的的匹配度（每秒输出一次数据，日志需要刷新才会显示）

此配置项可以用于调试，以确定合适的`threshold`值

#### `on_wake`

唤醒后，调用的函数。你可以定义自己的`on_wake`处理函数。

配置格式：`文件名.函数名`。

函数参数:

- `va_config` 配置项的内容（仅本配置项），字典类型

#### `on_command_stage1`

接收完语音命令后，调用的函数。你可以定义自己的`on_command_stage1`处理函数。

配置格式：`文件名.函数名`。

函数参数:

- `va_config` 配置项的内容（仅本配置项），字典类型

#### `on_command_stage2`

语音命令转文字后，调用的函数。你可以定义自己的`on_command_stage2`处理函数。

配置格式：`文件名.函数名`。

函数参数有两个：

- `speech_in` 识别到的语音命令，字符串
- `va_config` 配置项的内容（仅本配置项），字典类型

#### `media_player`

音频输出设备，在HomeAssistant中的实体id，如：`media_player.mpd`

如果要在HomeAssistant中所有的`media_player`设备上进行播放，使用`all`

#### `tts_service`

HomeAssistant中的tts的服务名，例如：`tts.google_translate_say`或`tts.baidu_say`

## 【定义智能音箱处理过程函数】

![处理过程](https://github.com/zhujisheng/hassio-addons/raw/master/voice_assistant/process.JPG)

如上图，用户可以编写自己的`on_wake`、`on_command_stage1`和`on_command_stage2`三个函数。

将对应的python文件放置在`/share/voice_assistant`目录中。

#### 样例程序

- `process_none.py`
  + `on_wake`

    播放声音“叮”

  + `on_command`

    播放声音“咚”

  + `on_react`

    不做处理，仅语音播放识别到的声音。

- `process_signallight.py`
  + `on_wake`

    信号灯闪烁

  + `on_command`

    信号灯常亮

  + `on_react`

    语音播放识别到的声音；信号灯熄灭

- `process_ha_event.py`
  + `on_wake`

    触发事件`hotword_heard`，事件数据中包含`"event": "hotword_heard"`，以及引发本事件的配置信息。

  + `on_command`

    触发事件`hotword_heard`，事件数据中包含`"event": "command_received"`，以及引发本事件的配置信息。

  + `on_react`

    触发事件`hotword_heard`，事件数据中包含`"event": "command_sttd"`、`"command": 收到的语音命令文本`，以及引发本事件的配置信息。

- `process_ha_intent.py`
  + `on_wake`

    播放声音“叮”。

  + `on_command`

    播放声音“咚”

  + `on_react`

    使用HomeAssistant的`conversation`和`intent_script`组件完成智能处理过程。

    需要在HomeAssistant中配置[conversation](https://www.home-assistant.io/integrations/conversation/)与[intent_script](https://www.home-assistant.io/integrations/intent_script)组件，例如：

      ```
      # Example configuration.yaml entry
      conversation:
        intents:
          RoomTemperature:
            - "现在多热"
            - "现在[室内]几度"
            - "[需][要]开空调吗"
            - ".*(?:温度|冷).*"
          OpenLight:
            - "打开(?:小米|小米网关|过道)?灯"
            - "把(?:小米|小米网关|过道)?灯打开"
          CloseLight:
            - "关闭(?:小米|小米网关|过道)?灯"
            - "把(?:小米|小米网关|过道)?灯关闭"

      intent_script:
        RoomTemperature:
          speech:
            text: 当前室内{{states.sensor.entity_id.state}}度
        OpenLight:
          speech:
            text: 正在打开小米灯
          action:
            service: light.turn_on
            data: 
              entity_id: light.entity_id
        CloseLight:
          async_action: true
          speech:
            text: 正在关闭小米灯
          action:
            service: light.turn_off
            data: 
              entity_id: light.entity_id
      ```

- `process_stringmatch.py`
  + `on_wake`

    播放声音“请讲”。

  + `on_command`

    播放声音“收到”

  + `on_react`

    使用模糊匹配识别对应的输入命令，并进行相应处理（通过调用HomeAssistant的API）

#### `ha_api.py`

`ha_api.py`放置在`/share/voice_assistant`目录中，其中封装了对HomeAssistant API的调用，可以在自定义处理过程函数中使用。

- `headers`

  访问API时的headers，其中包含了必要的认证信息

- `ha_base_url`

  HomeAssistant的外部访问URL

- `get_state(entity_id, attribute=None)`

  获得HomeAssistant中某个实体的状态或者某个属性值

- `post_service( service, data=None )`

  调用HomeAssistant的服务

- `fire_event(event_type, enent_data)`

  触发HomeAssistant的事件

- `play_tts( speech_text, tts, media_player )`

  播放文本的音频

- `play_audio_file( media_player, filename )`

  播放声音媒体文件（ding&dong），媒体文件放置在`配置目录/local/voice_assistant/`目录中

- `intent_process( speech_in )`

  调用`conversation/intent_process`API（conversation和intent_script组件提供的API服务）。

  输入为语音命令，输出为反馈语音。

