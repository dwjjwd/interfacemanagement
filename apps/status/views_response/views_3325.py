# _*_encoding:utf-8_*_
from django.shortcuts import render
from django.views.generic.base import View

from status.models import StatuTCPserver, OpenInterface,StatusInterface

from socket import *
from time import  ctime
import  threading
import json
import os
# Create your views here.
import time

BUFSIZ=1024
tcpSerSock = None
statuserver = None                   #当前响应式服务端数据库对象
socks=[]                             #放每个客户端的socket
addrsocks = {}
boolthread = True                    #控制线程
clientmessage = {}                   #缓存客户端数据
doornot = True                       #控制酒店接口是否开启或者关闭
Heartonline = []                     #缓存测试绑定客户端是否在线的结果


class openWatch3325(View):
    def get(self, request):
        watchport = request.GET.get('port')
        if watchport is None:
            return render(request, 'watch/watch_%s.html' % watchport, {'port':watchport})
        global tcpSerSock,boolthread,socks,addrsock,doornot,Heartonline,statuserver
        statuserver = StatuTCPserver.objects.get(port=int(watchport))
        openwatch = request.GET.get('openwatch')
        if addrsocks.__len__() != 0 :
            jianankong = []
            jianankongport = []
            for addrsock in addrsocks.values():
                ports = StatusInterface.objects.all()
                for port in ports:
                    if addrsock[1] == port.port:
                        jianankong.append(port)
                        jianankongport.append(port.port)
        if openwatch == 'on':
            boolthread = True
            doornot = True
            socks = []
            if request.session.get('tcpserver'+watchport) == None:
                request.session['tcpserver'+watchport] = 'ok'
                ts = threading.Thread(target=closePort)
                t = threading.Thread(target=openthread)
                HOST = statuserver.ip
                PORT = statuserver.port
                ADDR = (HOST,PORT)
                tcpSerSock=socket(AF_INET,SOCK_STREAM)
                try:
                    tcpSerSock.bind(ADDR)
                    statuserver.booleanTCP = 'on'
                    statuserver.save()
                except Exception,e:
                    request.session['tcpserver'+watchport] = None
                    return render(request, 'Error.html',{'port':watchport})
                tcpSerSock.listen(2)
                t.start()
                ts.start()
                if addrsocks.__len__() == 0 :
                    return render(request, 'watch/watch_%s.html' % watchport, {"tcpserver":statuserver,'port':watchport})
                return render(request, 'watch/watch_%s.html' % watchport, {"tcpserver":statuserver,"tcpclinend":addrsocks, "jianankong":jianankong,"jianankongport":jianankongport, 'clientmessage':clientmessage,'port':watchport})
            else:
                if addrsocks.__len__() == 0 :
                    return render(request, 'watch/watch_%s.html' % watchport, {"tcpserver":statuserver,'port':watchport})
                return render(request, 'watch/watch_%s.html' % watchport, {"tcpserver":statuserver,"tcpclinend":addrsocks, "jianankong":jianankong,"jianankongport":jianankongport,'clientmessage':clientmessage,'port':watchport})
        if openwatch == 'flush':
            boolthread = True
            if request.session['tcpserver'+watchport] == None:
                return render(request, 'watch/watch_%s.html' % watchport, {"tcpclinend":'请先开启服务','port':watchport})
            if addrsocks.__len__() == 0 :
                return render(request, 'watch/watch_%s.html' % watchport, {"tcpclinend2":statuserver,'port':watchport})
            return render(request, 'watch/watch_%s.html' % watchport, {"tcpclinend":addrsocks, "tcpclinend2":statuserver, "jianankong":jianankong,"jianankongport":jianankongport,'clientmessage':clientmessage,'port':watchport})
        if openwatch == 'off':
            # boolthread = False
            doornot = False
            if tcpSerSock is not None:
                try:
                    print('关闭开始')
                    tcpSerSock.shutdown(2)
                except Exception:
                    tcpSerSock.close()
                    for s in socks:
                        s.close()
                    detlastontconn()
                    time.sleep(1)
                    addrsocks.clear()
                    clientmessage.clear()
                    if statuserver is not None:
                        statuserver.beforenummax = 0
                        statuserver.booleanTCP = 'off'
                        statuserver.save()
                    print('关闭成功')
            statusinter_sjdinterfacestas = StatusInterface.objects.all()
            for statusinter_sjdinterfacesta in statusinter_sjdinterfacestas:
                statusinter_sjdinterfacesta.sjdinterfacesta = '未连接'
                statusinter_sjdinterfacesta.port = 0
                statusinter_sjdinterfacesta.save()
            request.session['tcpserver'+watchport] = None
            return render(request, 'watch/watch_%s.html' % watchport, {"tcpserveroff":'已关闭服务','port':watchport})
        if openwatch == 'delnobinding':
            if request.session['tcpserver'+watchport] == None:
                return render(request, 'watch/watch_%s.html' % watchport, {"tcpclinend":'请先开启服务','port':watchport})
            if addrsocks.__len__() == 0 :
                return render(request, 'watch/watch_%s.html' % watchport, {"tcpclinend2":statuserver,'port':watchport})
            for addrsock_clien,addrsock_addr in addrsocks.items():
                if addrsock_addr[1] not in jianankongport:
                    addrsock_clien.close()
                    del addrsocks[addrsock_clien]
            return render(request, 'watch/watch_%s.html' % watchport, {"tcpclinend":addrsocks, "tcpclinend2":statuserver, "jianankong":jianankong,"jianankongport":jianankongport,'clientmessage':clientmessage,'port':watchport})
        if openwatch == 'bindingheart' or openwatch == 'bindingheartflush' or openwatch == 'bindingheartclose' or openwatch == 'delbindingheart':
            if request.session['tcpserver'+watchport] == None:
                return render(request, 'watch/watch_%s.html' % watchport, {"tcpclinend":'请先开启服务','port':watchport})
            if addrsocks.__len__() == 0 :
                return render(request, 'watch/watch_%s.html' % watchport, {"tcpclinend2":statuserver,'port':watchport})
            if openwatch == 'bindingheart':
                Heartonline = []
                Heartonline.append('0000')
                bindingheartSend()
            if openwatch == 'bindingheartclose':
                del Heartonline[:]
                return render(request, 'watch/watch_%s.html' % watchport, {"tcpclinend":addrsocks, "tcpclinend2":statuserver, "jianankong":jianankong,"jianankongport":jianankongport,'clientmessage':clientmessage,'port':watchport})
            if openwatch == 'delbindingheart':
                port = request.GET.get('delport')
                delport(port)
                detportsta = StatusInterface.objects.get(port=int(port))
                detportsta.port = 0
                detportsta.sjdinterfacesta = '未连接'
                detportsta.save()
                jianankong.remove(detportsta)
            return render(request, 'watch/watch_%s.html' % watchport, {"tcpclinend":addrsocks, "tcpclinend2":statuserver, "jianankong":jianankong,"jianankongport":jianankongport,'clientmessage':clientmessage,'Heartonline':Heartonline,'port':watchport})
        if request.session['tcpserver'+watchport] == None or request.session['tcpserver'+watchport] == '':
            return render(request, 'watch/watch_%s.html' % watchport, {"tcpservergo":'服务未开启','port':watchport})
        else:
            return render(request, 'watch/watch_%s.html' % watchport, {"tcpservergo":statuserver,'port':watchport})
    def post(self, request):
        return render(request, 'Distributed.html', {"tcpserver":''})

def openthread():
    global tcpSerSock
    global boolthread
    print  u'我在%s线程中 ' % threading.current_thread().name
    print 'waiting for connecting...'
    while boolthread:
        try:
            clientSock,addr = tcpSerSock.accept()
            print  'connected from:', addr
            clientSock.setblocking(0)
            if statuserver is not None:
                statuTCPserverbefor = StatuTCPserver.objects.get(port=statuserver.port)
                if statuTCPserverbefor.beforenummax+1 <= statuTCPserverbefor.nummax :
                    socks.append(clientSock)
                    addrsocks[clientSock]=addr
                    statuTCPserverbefor.beforenummax = statuTCPserverbefor.beforenummax+1
                    statuTCPserverbefor.save()
                    t = threading.Thread(target=handle1, args=(clientSock, addr))
                    t.setDaemon(True)
                    t.start()
                else:
                    message = "端口已满，请访问分配数服务端重新获取端口"
                    goout = {"result":"NO","message":message}
                    clientSock.send('%s' % goout)
                    clientSock.close()
        except Exception,e:
            boolthread = False

def delport(port):
    global addrsocks,Heartonline
    for sk,sv in addrsocks.items():
        if sv[1] == int(port):
            sk.close()
            del addrsocks[sk]
            print('移除检测未通过的端口，%d ' % sv[1])

def bindingheartSend():
    statusInterface_booleaninter = StatusInterface.objects.all()
    for statusInterfacebooleaninter in statusInterface_booleaninter:
        for addrsockk,addrsockv in addrsocks.items():
            if statusInterfacebooleaninter.port == addrsockv[1] :
                message = "heart on line"
                goout = {"onheart":"server","message":message}
                addrsockk.send('%s' % goout)
                vercodeobj_name =  '%s%s' % (statusInterfacebooleaninter.hootelname.verison.brandcourse,statusInterfacebooleaninter.hootelname.verison.verison)
                mkdir(statusInterfacebooleaninter.hootelname.hootelname.kdt,vercodeobj_name,None,'Reserve %s' % message)

def detlastontconn():
    global addrsocks
    try:
        statusInterface_booleaninter = StatusInterface.objects.all()
        for statusInterfacebooleaninter in statusInterface_booleaninter:
            message = "监控服务端已关闭"
            vercodeobj_name =  '%s%s' % (statusInterfacebooleaninter.hootelname.verison.brandcourse,statusInterfacebooleaninter.hootelname.verison.verison)
            mkdir(statusInterfacebooleaninter.hootelname.hootelname.kdt,vercodeobj_name,None,'Reserve %s' % message)
        qw=socket(AF_INET,SOCK_STREAM)
        HOST = statuserver.ip
        PORT = statuserver.port
        ADDR = (HOST,PORT)
        qw.connect(ADDR)
        qw.send('ok LASTONe')
        qw.close()
    except Exception,e:
        print "[响应式客户端]连接错误：%s" %e


def closePort():
    global doornot
    while doornot:
        statusInterface_booleaninter = StatusInterface.objects.all()
        for statusInterfacebooleaninter in statusInterface_booleaninter:
            for addrsockk,addrsockv in addrsocks.items():
                if statusInterfacebooleaninter.port == addrsockv[1] and statusInterfacebooleaninter.hootelname.booleaninter == 'off':
                    message = "接口监控已关闭"
                    goout = {"result":"NO","message":message}
                    addrsockk.send('%s' % goout)
                    vercodeobj_name =  '%s%s' % (statusInterfacebooleaninter.hootelname.verison.brandcourse,statusInterfacebooleaninter.hootelname.verison.verison)
                    mkdir(statusInterfacebooleaninter.hootelname.hootelname.kdt,vercodeobj_name,None,'Reserve %s' % '已后台关闭该接口服务')
                    del addrsocks[addrsockk]
                    addrsockk.close()
                    statusInterfacebooleaninter.sjdinterfacesta = '未连接'
                    statusInterfacebooleaninter.port = 0
                    statusInterfacebooleaninter.save()
                    print('关闭该接口')
                    openmysef = False
                    break
        time.sleep(5)

def handle1(clientSock, addr):
    openmysef = True
    vercodeobj_name = None
    clientneirong = None
    reserverneirong = None
    global Heartonline
    while openmysef:
        try:
            data = clientSock.recv(BUFSIZ)
            if data is not None:
                print(addr,data)
                try:
                    nihao = json.loads(data)
                    #第一关截取 验证
                    kdt = nihao.get('kdt')
                    vercode = nihao.get('vercode')
                    if vercode is not None:
                        vercodeobj = StatusInterface.objects.filter(portvercode=vercode)
                        if vercodeobj.__len__() == 1:
                            vercodeobj_name = '%s%s' % (vercodeobj[0].hootelname.verison.brandcourse,vercodeobj[0].hootelname.verison.verison)
                except Exception,e:
                    if not data:
                        statusInterfaces = StatusInterface.objects.all()
                        for stats in statusInterfaces:
                            if stats.port == addr[1]:
                                stats.port = 0
                                stats.sjdinterfacesta = u'未连接'
                                stats.save()
                        del addrsocks[clientSock]
                        clientSock.close()
                        try:
                            del clientmessage[addr[1]]
                        except:
                            pass
                        if statuserver is not None:
                            statuTCPserverbefor = StatuTCPserver.objects.get(port=statuserver.port)
                            statuTCPserverbefor.beforenummax = statuTCPserverbefor.beforenummax-1
                            statuTCPserverbefor.save()
                        mkdir(kdt,vercodeobj_name,clientneirong,'Reserve %s' % '接口已关闭')
                    message = "数据格式有误"
                    goout = {"result":"NO","message":message}
                    clientSock.send('%s' % goout)
                    mkdir(kdt,vercodeobj_name,clientneirong,'Reserve %s' % message)
                    openmysef = False
                    continue
                #判断是否已经绑定接口
                statusInterface_kdt = StatusInterface.objects.all()
                statusInterfacekdts = {}
                statusInterfacevercodes = {}
                for statusInterfacekdt in statusInterface_kdt:
                    statusInterfacevercodes[statusInterfacekdt.portvercode] = statusInterfacekdt.hootelname.hootelname.kdt
                    statusInterfacekdts[statusInterfacekdt.portvercode] = statusInterfacekdt.port
                if vercode in statusInterfacevercodes and statusInterfacevercodes[vercode] == kdt and statusInterfacekdts[vercode] != 0:
                    if addr[1] != statusInterfacekdts[vercode]:
                        message = "socket已连接，请勿重复连接"
                        goout = '{"result":"NO","message":"%s"}' % message
                        clientSock.send('%s' % json.loads(goout))
                        clientSock.close()
                        mkdir(kdt, vercodeobj_name, 'Client %s' %data, 'Reserve %s' %goout)
                        break
                    get_data = nihao.get('data')
                    if get_data is not None:
                        get_message = get_data.get('message')
                        get_heart = get_data.get('onheart')
                        if get_heart is not None and get_heart == 'yes':
                            Heartonline.append(addr[1])
                        clientmessage[addr[1]] = get_message
                        goout = '{"result":"OK","message":""}'
                    else:
                        message = "data数据包不能为空"
                        goout = '{"result":"NO","message":"%s"}' % message
                    clientSock.send('%s' % json.loads(goout))
                    mkdir(kdt, vercodeobj_name, 'Client %s' %data, 'Reserve %s' %goout)
                else:
                    if kdt is not None and vercode is not None:
                        try:
                            statusInterface = StatusInterface.objects.filter(portvercode=vercode)
                            if statusInterface is not None and statusInterface.__len__() == 1:
                                statusInterface_1 = StatusInterface.objects.get(portvercode=vercode)
                                getstatu = statusInterface_1.hootelname.booleaninter
                                if getstatu == 'on':
                                    kdt_1 = statusInterface_1.hootelname.hootelname.kdt
                                    if kdt_1 == kdt:
                                        goout = '{"result":"OK","message":""}'
                                        statusInterface_1.sjdinterfacesta = u'已连接'
                                        statusInterface_1.port = addr[1]
                                        statusInterface_1.save()
                                    else:
                                        message = "KDT或者验证码有误，请核查"
                                        goout = '{"result":"NO","message":"%s"}' % message
                                else:
                                    message = "该接口监控未开启，请先开启服务"
                                    goout = '{"result":"NO","message":"%s"}' % message
                            else:
                                message = "验证码有误"
                                goout = '{"result":"NO","message":"%s"}' % message
                        except Exception,e:
                            message = "数据匹配出现错误"
                            goout = '{"result":"NO","message":"%s"}' % message
                    else:
                        message = "kdt或者验证码为空"
                        goout = '{"result":"NO","message":"%s"}' % message
                    clientSock.send('%s' % json.loads(goout))
                    mkdir(kdt, vercodeobj_name, 'Client %s' %data, 'Reserve %s' %goout)
        except Exception,e:
            continue
        if not data:
            del addrsocks[clientSock]
            clientSock.close()
            del clientmessage[addr[1]]
            openmysef = False
            mkdir(kdt, vercodeobj_name,None,clientneirong, 'Reserve %s' % '接口已关闭')
            continue

def mkdir(kdt,intername,clientneirong,reserverneirong):
    if kdt is None:
        kdt = '0000'
    if intername is None:
        intername = '未知接口'
    path =  os.path.expanduser('~')+'\\pythonXMSLogs'
    txtpath = path+"\\"+kdt
    interfacepath = txtpath+"\\"+intername
    isexists = os.path.exists(path)
    if not isexists:
        os.makedirs(path)
    isexists2 = os.path.exists(txtpath)
    if not isexists2:
        os.makedirs(txtpath)
    isexists3 = os.path.exists(interfacepath)
    filename = interfacepath+"\\"+time.strftime("%Y-%m-%d", time.localtime())+'.txt'
    if not isexists3:
        os.makedirs(interfacepath.decode('utf-8'))
    f = open(filename.decode('utf-8'), 'a')
    if clientneirong is not None:
        f.write(time.strftime("%H:%M:%S", time.localtime())+"  "+clientneirong+"\n")
    if reserverneirong is not None:
        f.write(time.strftime("%H:%M:%S", time.localtime())+"  "+reserverneirong+"\n")
    f.close()


