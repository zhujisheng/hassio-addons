# Home Assistant Add-on: Mycroft Precise

声音唤醒——当识别到某个声音时，生成一条HomeAssistant中的事件

## 关于

[Mycroft Precise](https://github.com/MycroftAI/mycroft-precise)是一个基于神经网络的声音唤醒服务。

本Add-on运行mycroft-precise，并且在识别到对应的声音后，在HomeAssistant中生成一条对应的事件。

## 配置

#### `input_device`

音频输入设备。

取值：`local_default`，表示缺省的音频输入设备（在add-on的`audio`配置中选择）。

远程麦克风：配置格式为`ip地址:端口号`，例如`192.168.1.120:3344`

远程麦克风本身的安装与配置，参见相关课程[《HomeAssistant智能家居实战篇》](https://study.163.com/course/courseMain.htm?courseId=1006189053&share=2&shareId=400000000624093)中[《接入HomeAssistant的远程麦克风》](https://study.163.com/course/courseLearn.htm?courseId=1006189053&share=2&shareId=400000000624093#/learn/video?lessonId=1279002359&courseId=1006189053)

#### Option `model_file`

唤醒词声音模型文件

add-on中预置了文件`/cough.pb`和`/hey-mycroft.pb`，对应咳嗽声音与`嘿，麦克若福特`

#### Option `threshold`

触发事件的门槛值：当前声音与模型的匹配度大于门槛值时，会触发HomeAssistant中的事件

匹配度为0到1之间的数；门槛值可设置为0到1之间的数。

#### Option `event_type`

触发的HomeAssistant中的事件类型

#### Option `show_match_level_realtime`

是否在日志中输出当前声音的匹配度（每秒输出一次数据，日志需要刷新才会显示）

此配置项可以用于调试，以确定合适的`threshold`值

## 创建自己的唤醒音模型

你可以创建并配置自己的唤醒音模型文件

- 创建

  参见：[https://github.com/MycroftAI/mycroft-precise/wiki/Training-your-own-wake-word](https://github.com/MycroftAI/mycroft-precise/wiki/Training-your-own-wake-word)

- 配置

  可以通过Add-on:Samba，将模型文件`xxxxx.pb`和`xxxxx.pb.params`（或者`xxx.net`)放置在共享的`share/`目录中

  在配置中，设置`model_file`为`/share/xxxxx.pb`(或者`/share/xxxxx.net`)