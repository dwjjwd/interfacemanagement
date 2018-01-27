# _*_ encoding:utf-8 _*_
from django.test import TestCase

from socket import *
from time import  ctime
import  threading
import time
HOST=''
PORT=2159
BUFSIZ=1024
ADDR = (HOST,PORT)

tcpSerSock=socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(2)
socks=[]                             #放每个客户端的socket
addrsocks = {}


def handle():
    while True:
        for s in socks:
            try:
                data = s.recv(BUFSIZ)     #到这里程序继续向下执行
                print(addrsocks.get(s),data)
                if data == '1':
                    print('关闭开始')
                    try:
                        tcpSerSock.shutdown(2)
                    except Exception,e:
                        oq2 = tcpSerSock.close()
                    print('关闭结束')
            except Exception, e:
                continue
            if not data:
                socks.remove(s)
                print('移除完毕,')
                continue
            s.send('[%s],%s' % (ctime(), data))

t = threading.Thread(target=handle)             #子线程
if __name__ == '__main__':
    t.start()
    print  u'我在%s线程中 ' % threading.current_thread().name    #本身是主线程
    print 'waiting for connecting...'
    while True:
        clientSock,addr = tcpSerSock.accept()
        print  'connected from:', addr
        clientSock.setblocking(0)
        socks.append(clientSock)
        addrsocks[clientSock]=addr

# from socket import *
# from time import  ctime
# import  threading
# import time
# HOST=''
# PORT=2159
# BUFSIZ=1024
# ADDR = (HOST,PORT)
#
# tcpSerSock=socket(AF_INET,SOCK_STREAM)
# tcpSerSock.bind(ADDR)
# tcpSerSock.listen(5)
# socks=[]                             #放每个客户端的socket
#
# def handle():
#     while True:
#         for s in socks:
#             try:
#                 data = s.recv(BUFSIZ)     #到这里程序继续向下执行
#                 print(s)
#             except Exception, e:
#                 continue
#             if not data:
#                 socks.remove(s)
#                 print('移除完毕,')
#                 continue
#             s.send('[%s],%s' % (ctime(), data))
#
# t = threading.Thread(target=handle)             #子线程
# if __name__ == '__main__':
#     t.start()
#     print  u'我在%s线程中 ' % threading.current_thread().name    #本身是主线程
#     print 'waiting for connecting...'
#     while True:
#         clientSock,addr = tcpSerSock.accept()
#         print  'connected from:', addr
#         clientSock.setblocking(0)
#         socks.append(clientSock)