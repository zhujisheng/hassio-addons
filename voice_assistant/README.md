# Home Assistant Add-on: voice_assistant

一个智能音箱。

## 【关于】

这是一个智能音箱add-on，在其中集成了以下应用：
- [mycroft-precise](https://github.com/MycroftAI/mycroft-precise/)唤醒词服务，
- google的云端语音识别服务（连接到`http://www.google.cn/speech-api/v2/recognize`）
- 缺省的语音命令处理过程：
    - HomeAssistant中的`media_player.play_media`服务
    - HomeAssistant中的`tts.google_translate_say`服务
    - HomeAssistant中的`conversation/process`API（需要在HomeAssistant中配置[conversation](https://www.home-assistant.io/integrations/conversation/)与[intent_script](https://www.home-assistant.io/integrations/intent_script)组件）
- 自定以的语音命令处理过程，详见下面文档。


## 【多个语音助理】

在`voice_assistant`下可以配置多个语音助理，每个语音助理对应

- 一个音频输入设备
- 一个音频输出设备
- 一个唤醒词模型，以及唤醒相应的参数
- 一个唤醒后调用函数、一个语音命令输入后的调用函数、一个语音命令识别后的调用函数

多个语音助理可以使用不同的或相同的音频输入设备、音频输出设备、唤醒词、处理函数，从而自由定义对不同音频输入设备上的不同唤醒词的不同处理方式。

## 【HomeAssitant中的配置】

使用本语音助手，需要事先在HomeAssistant中配置以下项目：

- 一个或多个媒体播放器
- 一个或多个tts服务
- 如果使用缺省的反馈处理函数，需要配置[conversation](https://www.home-assistant.io/integrations/conversation/)与[intent_script](https://www.home-assistant.io/integrations/intent_script)组件，例如：

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

## 【配置项】

#### `input_device`

音频输入设备。

取值：`local_default`，表示缺省的音频输入设备（在add-on的`audio`配置中选择）。

远程麦克风：配置格式为`ip地址:端口号`，例如`192.168.1.120:3344`

远程麦克风本身的安装与配置，参见相关课程[《HomeAssistant智能家居实战篇》](https://study.163.com/course/courseMain.htm?courseId=1006189053&share=2&shareId=400000000624093)中[《接入HomeAssistant的远程麦克风》](https://study.163.com/course/courseLearn.htm?courseId=1006189053&share=2&shareId=400000000624093#/learn/video?lessonId=1279002359&courseId=1006189053)

#### `output_entity_id`

音频输出设备，在HomeAssistant中的实体id，如：`media_player.mpd`

如果要在HomeAssistant中所有的`media_player`设备上进行播放，使用`all`

#### `tts_service`

调用的HomeAssistant中的tts的服务名，例如：`tts.google_translate_say`或`tts.baidu_say`

#### `model_file`

唤醒词模型文件，系统根目录中带有`hey-mycroft.pb`和`cough.pb`两个模型，分别对应`嘿，麦克若福特`和咳嗽（口哨）音

你可以创建并配置自己的唤醒音模型文件

- 创建

  参见：[https://github.com/MycroftAI/mycroft-precise/wiki/Training-your-own-wake-word](https://github.com/MycroftAI/mycroft-precise/wiki/Training-your-own-wake-word)

- 配置

  可以通过Add-on:Samba，将模型文件`xxxxx.pb`和`xxxxx.pb.params`（或者`xxx.net`)放置在共享的`share/`目录中

  在配置中，设置`model_file`为`/share/xxxxx.pb`(或者`/share/xxxxx.net`)

#### `threshold`

触发语音助理的门槛值：当前声音与模型的匹配度大于门槛值时，开始接收语音命令

匹配度为0到1之间的数；门槛值可设置为0到1之间的数。

门槛值越低，误唤醒概率越大，漏唤醒概率越低；门槛值越高，误唤醒概率越低，漏唤醒概率越大。

#### `show_match_level_realtime`

是否在日志中输出当前声音与唤醒词模型的的匹配度（每秒输出一次数据，日志需要刷新才会显示）

此配置项可以用于调试，以确定合适的`threshold`值

#### `op_waken`

唤醒后，调用的函数。缺省的`voice_assistant.waken`播放声音`叮`

你可以定义自己的`op_waken`处理函数。

#### `op_recvd`

接收完语音命令后，调用的函数。缺省的`voice_assistant.recvd`播放声音`咚`

你可以定义自己的`op_recvd`处理函数。

#### `op_react`

语音命令转文字后，调用的函数。缺省的`voice_assistant.react`调用HomeAssistant的API`conversation/process`服务对语音命令文本进行处理，并调用tts服务进行反馈语音播放

你可以定义自己的`op_react`处理函数。


## 【定义自己的处理函数】

![处理过程](https://github.com/zhujisheng/hassio-addons/raw/master/voice_assistant/process.JPG)

如上图，用户可以编写自己的`op_waken`、`op_recvd`和`op_react`三个函数。

#### 样例

- [my_process.py](https://github.com/zhujisheng/hassio-addons/blob/master/voice_assistant/my_process.py)

  将此文件保存在Samba共享的`/share`目录中

  注：另一个样例程序[my_process_remote.py](https://github.com/zhujisheng/hassio-addons/blob/master/voice_assistant/my_process_remote.py)也可以参考，区别在于以远程麦克风上的灯来提示唤醒，而不是使用`叮咚`声。

- add-on中配置

  ```
  op_waken: share.my_process.waken
  op_recvd: share.my_process.recvd
  op_react: share.my_process.react
  ```

 注：如果放置位置为`/share`的子目录，比如`/share/voice_assistant/`，那么必须在`/share/voice_assistant/`中构建一个空的`__init__.py`文件。此时配置为：`op_waken: share.voice_assistant.my_process.waken`

#### 样例说明

- 你可以修改程序中的`commands`定义，以及`react`函数中针对不同command的处理过程，以获得你想要的效果
- 程序使用了模糊匹配，以获得输入语音命令的最佳匹配结果。最佳匹配项匹配度需大于10（程序中定义）
- add-on开放了8000端口的http服务，其中有两个文件`ding.wav`和`dong.wav`供使用。在样例中，`waken`函数中播放了`ding.wav`

#### `op_waken`

唤醒后，调用的函数。两个调用参数:

- `tts` HomeAssistant中的tts服务，也就是配置项中的`tts_service`
- `media_player` HomeAssistant中的媒体播放器，也就是配置项中的`output_entity_id`

#### `op_recvd`

接收完语音命令后，调用的函数。两个调用参数:

- `tts` HomeAssistant中的tts服务，也就是配置项中的`tts_service`
- `media_player` HomeAssistant中的媒体播放器，也就是配置项中的`output_entity_id`

#### `op_react`

语音命令转文字后，调用的函数。调用参数有三个：

- `speech_in` 识别到的语音命令，字符串
- `tts` HomeAssistant中的tts服务，也就是配置项中的`tts_service`
- `media_player` HomeAssistant中的媒体播放器，也就是配置项中的`output_entity_id`
