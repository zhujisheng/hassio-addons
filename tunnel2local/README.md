# Home Assistant Add-on: tunnel2local

通过frp隧道，使局域网中的homeassistant可以通过公网访问。

## 关于

[frp](https://github.com/fatedier/frp/blob/master/README_zh.md)是一个可用于内网穿透的高性能的反向代理应用。

本Add-on可以连接到frp服务，实现http或者tcp的反向代理。

缺省配置对应于一台公网上的测试服务器，仅供测试。如果你需要稳定的反向代理服务，需要在公网上搭建自己的frps服务。

## 配置

#### Option `frp_server`

frp服务器

#### Option `frp_server_port`

frp服务端口

#### Option `frp_token`

frp服务连接token

#### Option `local_host`

需要反向代理的本地服务器（如果是Home Assistant，仅需要填`homeassistant`)

#### Option `local_port`

需要反向代理的本地服务端口

#### Option `tunnel_type`

`tcp`或者`http`

#### Option `http_domain`

http反向代理后，访问的域名后缀

#### Option `http_subdomain_host`

http反向代理后，访问的域名头；如果为空，则使用系统中的随机UUID

#### Option `tcp_remote_port`

tcp反向代理后，服务器上对外开放的端口

## frps服务搭建

你可以使用缺省配置中的frps服务，但对应的服务器仅用于测试，不保证稳定性。

您可以搭建并使用自己的frp服务器端——前提条件是：您控制一台公网能直接访问到的服务器（云主机）。

搭建过程：

使用下载的frp包中的frps程序，在服务器上运行。

tcp反向代理的配置文件`frps.ini`如下：
```ini
[common]
bind_port = 7000
token = 12345678
```

如果要实现http虚拟主机代理，增加以下配置项：
```ini
[common]
bind_port = 7000
token = 12345678

vhost_http_port = 80
subdomain_host = xxxx.yyyy.com
```
*注：http虚拟主机代理模式，你必须要将域名`*.xxxx.yyyy.com`全部指向你的主机。*

其余的配置项可以参见frps项目的配置说明

## 注意

1. 缺省配置仅对应测试服务，不保证服务质量
2. add-on中使用的frp客户端版本为0.32.1，如果你自己搭建服务器，建议使用对应版本
3. 启动后，供Internet访问的URL，可以在log中查看