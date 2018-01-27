# -*-coding:utf-8-*-
__author__ = 'DingWenJing'
_date_ = '2018/1/9 15:12'

import socket
import threading, time
import json


socketser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketser.bind(('127.0.0.1', 1122))
socketser.listen(5)

def tcpser():
    global socketser
    while True:
        sock,addr = socketser.accept()
        print('TCP/Client coneection ',addr)
        t = threading.Thread(target=monitor,args=(sock, addr))
        t.setDaemon(True)
        t.start()


def monitor(sock, addr):
    global socketser
    while True:
        data = sock.recv(1024)
        print(data.decode('gbk'))
        if not data or data.decode('gbk') == 'exit':
            print('已经移除该客户端 %s%s ' % addr)
            break
        message = "KDT或者验证码有误，请核查"
        goout = '{"result":"NO","message":"%s"}' % message
        print(goout)
        sock.send('%s' % json.loads(goout))
        if data == 'close':
            try:
                socketser.shutdown(2)
            except Exception,e:
                socketser.close()
                print('服务端关闭')
        sock.send(('hello,%s' % data.decode('GBK')).encode('GBK'))
        sock.close
        print('Connection from %s:%s closed.' % addr)

tcpser()