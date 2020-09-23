# 在hassio中使用本代理

以下内容阐述如何通过本代理，完成add-on的下载与升级，以及HomeAssistant依赖python库的安装下载。

*注：作为在中国大陆加速的另一种方法，你也可以直接[使用国内的下载点](../在hassio中使用中国大陆下载点.md)*

## 【安装并启动本代理】

安装并启动`add-on：Simple Proxy`

*注：在仓库`https://github.com/zhujisheng/hassio-addons`中*

## 【设置docker镜像下载的proxy】

- 登录底层操作系统，运行`sudo mkdir -p /etc/systemd/system/docker.service.d`
- 创建文件`/etc/systemd/system/docker.service.d/http-proxy.conf`，内容：

  ```
  [Service]
  Environment="HTTP_PROXY=http://127.0.0.1:7088/"
  ```

- 运行`sudo systemctl daemon-reload`
- 重新启动：`sudo reboot`
- 检查proxy是否生效：`systemctl show --property=Environment docker`

  如果生效，能看到设置的proxy信息

## 【HomeAssistant Core中安装python依赖库使用proxy】

- 进入HomeAssistant容器： `docker exec -it homeassistant bash`

  *注：如果正在升级HomeAssistant，需要新的HomeAssiantant容器启动后才能进入，但不必等待HomeAssisant前端可访问。**

- 创建文件`/etc/pip.conf`，内容：

  ```
  [global]
  proxy = http://127.0.0.1:7088
  ```

- 重新启动homeassistant，或重启整个机器