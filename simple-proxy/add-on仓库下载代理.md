# add-on仓库下载代理

## 问题

在中国大陆区域，访问github有异常，会造成Supervisor中仓库会异常丢失，或者无法添加新的add-on仓库。

## 解决

1. 安装此add-on，启动（如果无法添加本仓库，可以将本目录中内容放置在本地的`addons`目录中，在本地安装与启动）

2. 登录到supervisor docker容器中

    `docker exec -it hassio_supervisor bash`

3. 运行

    `git config --global http.proxy http://homeassistant:7088`

4. 如果HomeAssistant社区仓库已经丢失，可以在前端手工添加

    `https://github.com/hassio-addons/repository`

若要取消以上设置，在第三步运行：

`git config --global --unset http.proxy`