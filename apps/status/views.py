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

class monitInterface(View):
    def get(self, request):
        statusInterfaces = StatusInterface.objects.all()
        return render(request, 'monitInterface.html', {"statusInterface_monitInterface":statusInterfaces})
    def post(self, request):
        pass

class monitServer(View):
    def get(self, request):
        statusserver = StatuTCPserver.objects.all()
        return render(request, 'monitServer.html', {"statusInterface_monitServer":statusserver})
    def post(self, request):
        pass


ONE_PAGE_OF_DATA = 2
def getBlogPosts(rquest):
    try:
        curPage = int(rquest.GET.get('curPage', '1'))
        allPage = int(rquest.GET.get('allPage','1'))
        pageType = str(rquest.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''

    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1

    startPos = (curPage - 1) * ONE_PAGE_OF_DATA
    endPos = startPos + ONE_PAGE_OF_DATA
    posts = StatuTCPserver.objects.all()[startPos:endPos]

    if curPage == 1 and allPage == 1:
        allPostCounts = StatuTCPserver.objects.count()
        allPage = allPostCounts / ONE_PAGE_OF_DATA
        remainPost = allPostCounts % ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1

    return render(rquest, "page.html",{'posts':posts, 'allPage':allPage, 'curPage':curPage})

