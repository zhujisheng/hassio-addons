# 在hassio中使用中国大陆下载点

通过设置docker的下载点为国内的点，可以加速hassio安装过程中下载docker镜像的速度；通过设置pip安装下载点为国内的点，可以加速python依赖包的安装——如果你是在中国大陆的话。

## 【设置docker镜像下载点】

- 编辑文件`/etc/docker/daemon.json`，内容：

  ```json
  { 
    "registry-mirrors": [ 
    "https://rw21enj1.mirror.aliyuncs.com",
    "https://dockerhub.azk8s.cn",
    "https://reg-mirror.qiniu.com",
    "https://hub-mirror.c.163.com",
    "https://docker.mirrors.ustc.edu.cn"
    ]
  }
  ```

- 重新加载服务

  `sudo systemctl daemon-reload`

- 重新启动系统

  `sudo reboot`

- 检查

  运行`docker info`，查看其中`Registry Mirrors`信息

你也可以将以下脚本保存到本地直接执行：

```bash
#!/bin/bash
if [ ! -d /etc/docker ];then
   sudo mkdir -p /etc/docker
fi
cat << EOF | sudo tee /etc/docker/daemon.json 
{ 
    "registry-mirrors": [ 
    "https://rw21enj1.mirror.aliyuncs.com",
    "https://dockerhub.azk8s.cn",
    "https://reg-mirror.qiniu.com",
    "https://hub-mirror.c.163.com",
    "https://docker.mirrors.ustc.edu.cn"
    ]
}
EOF
sudo systemctl daemon-reload
sudo reboot
```

## 【HomeAssistant Core中设置python依赖库下载点】

- 进入HomeAssistant容器： `docker exec -it homeassistant bash`

  *注：如果正在升级HomeAssistant，需要新的HomeAssiantant容器启动后才能进入，但不必等待HomeAssisant前端可访问。**

- 创建文件`/etc/pip.conf`，内容：

  ```
  [global]
  index-url=https://mirrors.aliyun.com/pypi/simple/
  ```

- 重新启动homeassistant，或重启整个机器
