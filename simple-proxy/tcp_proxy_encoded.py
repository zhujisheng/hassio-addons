#!/usr/bin/env python3

import os
import json
import socket
import threading
from selectors import DefaultSelector, EVENT_READ

# Proxy开放的端口号
LOCAL_PORT = 7088
# 连接的远程服务器与端口，修改成你的远程服务器地址
REMOTE_ADDR = "hachinasp.duckdns.org"
REMOTE_PORT = 7088

def xor_encode( bstring ):
    """一个简单编码：两次编码后与原值相同"""
    MASK = 0x55
    ret = bytearray( bstring )
    for i in range(len(ret)):
        ret[i] ^= MASK
    return ret


def proxy_process_encoded( sock1, sock2 ):
    """在两个sockek之间转发数据：任何一个收到的，编码后转发到另一个"""
    sel = DefaultSelector()
    sel.register(sock1, EVENT_READ)
    sel.register(sock2, EVENT_READ)

    while True:
        events = sel.select()
        for (key,ev) in events:
            try:
                data_in = key.fileobj.recv(8192)
            except ConnectionResetError as e:
                print(key.fileobj, "\nreset receive!")
                sock1.close()
                sock2.close()
                return
            if data_in:
                if key.fileobj==sock1:
                    sock2.send(xor_encode(data_in))
                else:
                    sock1.send(xor_encode(data_in))
            else:
                sock1.close()
                sock2.close()
                return

def tcp_proxy(sock_in, addr):
    """新的代理请求连接时，进行相关处理"""
    print("新的连接: %s:%s..." % addr, flush=True)

    # 建立远程连接
    sock_remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_remote.settimeout(15)
    try:
        sock_remote.connect((REMOTE_ADDR, REMOTE_PORT))
    except Exception as e:
        print(e, flush=True)
        print( "Error when connect to", (REMOTE_ADDR, REMOTE_PORT), flush=True )
            
        sock_in.close()
        return

    # 在本地连接与远程连接间转发数据
    proxy_process_encoded( sock_in, sock_remote )


def start_server():
    """主服务函数"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", LOCAL_PORT))
    s.listen()
    print("等待客户端连接...", flush=True)

    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=tcp_proxy, args=(sock, addr))
        t.start()


if __name__ == "__main__":
    os.system("iptables -A INPUT -p tcp --sport {} --tcp-flags RST RST -j DROP".format(REMOTE_PORT))
    start_server()