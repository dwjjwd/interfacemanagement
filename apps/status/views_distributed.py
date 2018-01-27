# -*-coding:utf-8-*- 
__author__ = 'DingWenJing'
_date_ = '2018/1/16 9:46'
from django.shortcuts import render
from django.views.generic.base import View

from .models import StatuTCPserver, OpenInterface,StatusInterface
from socket import *
from time import  ctime
import  threading
import json
import os
import time
import shutil
# Create your views here.


distributedport = None              #分配地址服务端口
tcpSerSockDisribu = None            #分配地址服务端对象
distributcpserver = None            #分配地址服务器对象
addrsocksDisribu = {}               #缓存连接对象
distribuServer = {}                 #端口分配成功或失败对象的地址和端口


class distributedServer(View):
    def get(self, request):
        global tcpSerSockDisribu
        global distribuServer, distributcpserver, distributedport
        distributedport = request.GET.get('distributedport')
        openwatch = request.GET.get('openwatch')
        watchport = request.GET.get('watchport')
        if watchport is not None:
            return render(request, 'watch/watch_%s.html' % watchport, {'port':watchport})
        if distributedport is not None:
            distributcpserver = StatuTCPserver.objects.get(port=distributedport)
            if distributcpserver is None:
                return render(request, 'DistributedOnline.html', {"errorstatuserver_distribu":'端口出现错误！','distributedport':distributedport})
            if openwatch == 'on':       #开启服务
                if request.session['distributetcpserver'] == None:
                    request.session['distributetcpserver'] = 'ok'
                    try:
                        t = threading.Thread(target=openthreadDistribute)
                        HOST = distributcpserver.ip
                        PORT = distributcpserver.port
                        ADDR = (HOST,PORT)
                        tcpSerSockDisribu=socket(AF_INET,SOCK_STREAM)
                        try:
                            tcpSerSockDisribu.bind(ADDR)
                            distributcpserver.booleanTCP = 'on'
                            distributcpserver.save()
                        except Exception,e:
                            return render(request, 'Error.html',{'distributedport':distributedport})
                        tcpSerSockDisribu.listen(5)
                        t.start()
                    except Exception,e1:
                        print(e1)
                    if distribuServer.__len__() == 0 :
                        return render(request, 'DistributedOnline.html',{'distributcpserver':distributcpserver,'distributedport':distributedport})
                    return render(request, 'DistributedOnline.html',{'distributcpserver':distributcpserver, 'distribuServer':distribuServer,'distributedport':distributedport})
                else:
                    if distribuServer.__len__() == 0 :
                        return render(request, 'DistributedOnline.html',{'distributcpserver':distributcpserver,'distributedport':distributedport})
                    return render(request, 'DistributedOnline.html',{'distributcpserver':distributcpserver, 'distribuServer':distribuServer,'distributedport':distributedport})

            if openwatch == 'flush':          #刷新
                if request.session['distributetcpserver'] == None:
                    return render(request, 'DistributedOnline.html', {"distributed_tcpclinend":'请先开启服务','distributedport':distributedport})
                if distribuServer.__len__() == 0 :
                    return render(request, 'DistributedOnline.html',{'distributcpserver':distributcpserver,'distributedport':distributedport})
                return render(request, 'DistributedOnline.html',{'distributcpserver':distributcpserver, 'distribuServer':distribuServer,'distributedport':distributedport})

            if openwatch == 'off':          #关闭服务
                request.session['distributetcpserver'] = None
                if tcpSerSockDisribu is not None:
                    try:
                        print('关闭开始')
                        tcpSerSockDisribu.shutdown(2)
                    except Exception:
                        tcpSerSockDisribu.close()
                        for sk,sv in addrsocksDisribu.items():
                            sk.close()
                        detlastontconn()
                        time.sleep(1)
                        distribuServer = {}
                        distributcpserver.booleanTCP = 'off'
                        distributcpserver.save()
                        print('关闭成功')
                    statuTCPserverbefor = StatuTCPserver.objects.get(port=distributcpserver.port)
                    statuTCPserverbefor.beforenummax = 0
                    statuTCPserverbefor.save()
                return render(request, 'DistributedOnline.html',{"distributed_tcpserveroff":'已关闭服务','distributedport':distributedport})
            return render(request, 'DistributedOnline.html',{'distributedport':distributedport})
        statuTCPserver = StatuTCPserver.objects.all()
        statuTCPserver_distribu = {}
        statuTCPserver_response = {}
        statuTCPserver_booleanTemplate = {}
        for stcp in statuTCPserver:
            if stcp.booleanTemplate:
                if stcp.id == 1:
                    if stcp.beforenummax >= stcp.nummax:
                        statuTCPserver_distribu[stcp] = 'max'
                    elif stcp.booleanTCP == 'on':
                        statuTCPserver_distribu[stcp] = 'on'
                    elif stcp.booleanTCP == 'off':
                        statuTCPserver_distribu[stcp] = 'off'
                else:
                    if stcp.beforenummax >= stcp.nummax:
                        statuTCPserver_response[stcp] = 'max'
                    elif stcp.booleanTCP == 'on':
                        statuTCPserver_response[stcp] = 'on'
                    elif stcp.booleanTCP == 'off':
                        statuTCPserver_response[stcp] = 'off'
            else:
                statuTCPserver_booleanTemplate[stcp] = 'none'
        return render(request, 'Distributed.html', {"statuTCPserver_distribu":statuTCPserver_distribu, 'statuTCPserver_response':statuTCPserver_response,'statuTCPserver_booleanTemplate':statuTCPserver_booleanTemplate})
    def post(self, request):
        pass

def openthreadDistribute():
    global tcpSerSockDisribu, distribuServer
    print  u'分配地址线程监控已启动 %s ' % threading.current_thread().name
    print 'waiting for connecting...'
    while True:
        try:
            clientSock,addr = tcpSerSockDisribu.accept()
            print  '[分配地址线程监控]connected from:', addr
            clientSock.setblocking(0)
            addrsocksDisribu[clientSock]=addr
            distribuServer[addr] = 'NO'
            if distributcpserver is not None:
                statuTCPserverbefor = StatuTCPserver.objects.get(port=distributcpserver.port)
                statuTCPserverbefor.beforenummax = statuTCPserverbefor.beforenummax+1
                statuTCPserverbefor.save()
            t = threading.Thread(target=handle1, args=(clientSock, addr))
            t.setDaemon(True)
            t.start()
        except Exception,e:
            boolthread = False

def detlastontconn():
    global addrsocks
    try:
        if distributcpserver is not None:
            qw=socket(AF_INET,SOCK_STREAM)
            HOST = distributcpserver.ip
            PORT = distributcpserver.port
            ADDR = (HOST,PORT)
            qw.connect(ADDR)
            qw.send('ok LASTONe')
            qw.close()
            print("[分配地址线程监控]地址分配服务端已关闭")
    except Exception,e:
        print "[分配地址线程监控]关闭错误：%s" %e

def handle1(clientSock, addr):
    global distribuServer
    openmysef = True
    while openmysef:
        try:
            data = clientSock.recv(2048)
            if data is not None:
                print(addr,data)
                try:
                    nihao = json.loads(data)
                    #第一关截取 验证
                    kdt = nihao.get('kdt')
                    request = nihao.get('request')
                except Exception,e:
                    if not data:
                        del distribuServer[addr]
                        clientSock.close()
                        if distributcpserver is not None:
                            statuTCPserverbefor = StatuTCPserver.objects.get(port=distributcpserver.port)
                            statuTCPserverbefor.beforenummax = statuTCPserverbefor.beforenummax-1
                            statuTCPserverbefor.save()
                        break
                    message = "数据格式有误"
                    goout = {"result":"NO","message":message}
                    clientSock.send('%s' % goout)
                    continue
                statusInterfaces = StatusInterface.objects.all()
                allkdt = []
                for skdt in statusInterfaces:
                    allkdt.append(skdt.hootelname.hootelname.kdt)
                if kdt is not None and request is not None and request == 'port':
                    if kdt not in allkdt:
                        message = "未找到该酒店KDT相关数据"
                        goout = '{"result":"NO","message":"%s"}' % message
                        clientSock.send('%s' % json.loads(goout))
                        continue
                    statuTCPservers = StatuTCPserver.objects.all()
                    booleantcpport = True #用来判断是否成功分配端口
                    for statuTCPserver in statuTCPservers:
                        if statuTCPserver.port != int(distributedport) and statuTCPserver.booleanTCP == 'on' and statuTCPserver.beforenummax+1 <= statuTCPserver.nummax :
                            message = statuTCPserver.port
                            goout = '{"result":"OK","message":"%d"}' % message
                            clientSock.send('%s' % json.loads(goout))
                            clientSock.close()
                            distribuServer[addr] = message
                            booleantcpport = False
                            if distributcpserver is not None:
                                statuTCPserverbefor = StatuTCPserver.objects.get(port=distributcpserver.port)
                                statuTCPserverbefor.beforenummax = statuTCPserverbefor.beforenummax-1
                                statuTCPserverbefor.save()
                            break
                    if booleantcpport:
                        message = "服务器最大连接数已满，请联系联系管理员"
                        goout = '{"result":"NO","message":"%s"}' % message
                        clientSock.send('%s' % json.loads(goout))
                else:
                    message = "kdt或者请求端口为空"
                    goout = '{"result":"NO","message":"%s"}' % message
                    clientSock.send('%s' % json.loads(goout))
        except Exception,e:
            continue
        if not data:
            clientSock.close()
            continue

def buildresponserver(request):
    statuTCPservers = StatuTCPserver.objects.all()
    boolTeamAndView = {}
    for statuTCPserver in statuTCPservers:
        if statuTCPserver.booleanTemplate == False:
            path = os.getcwd()
            try:
                views_myself = 'views_%s.py' % statuTCPserver.port
                shutil.copyfile(os.getcwd()+"/apps/status/views_response/views_3321.py",os.getcwd()+"/apps/status/views_response/"+views_myself)
                print('生成客户端模版 %s' % views_myself)
                boolTeamAndView[views_myself] = 'ok'
            except Exception,e:
                boolTeamAndView[views_myself] = 'no'
                print('生成客户端模版出现错误 % s' % e)
            try:
                watch_myself = 'watch_%s.html' % statuTCPserver.port
                shutil.copyfile("templates/watch.html","templates/watch/"+watch_myself)
                print('生成HTML模版 %s' % watch_myself)
                boolTeamAndView[watch_myself] = 'ok'
            except Exception,e:
                boolTeamAndView[watch_myself] = 'no'
                print('生成HTML模版出现错误 % s' % e)
            statuTCPserver.booleanTemplate = True
            statuTCPserver.save()
    return render(request, 'bulidTemplate.html', {'boolTeamAndView':boolTeamAndView})