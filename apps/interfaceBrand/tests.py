# _*_ encoding:utf-8 _*_
from django.test import TestCase
import json
import socket
import threading
import os
import os
import time
# def mkdir(kdt,intername,neirong):
#     path =  os.path.expanduser('~')+'\\pythonXMSLogs'
#     txtpath = path+"\\"+kdt
#     interfacepath = txtpath+"\\"+intername
#     isexists = os.path.exists(path)
#     if not isexists:
#         os.makedirs(path)
#     isexists2 = os.path.exists(txtpath)
#     if not isexists2:
#         os.makedirs(txtpath)
#     isexists3 = os.path.exists(interfacepath)
#     filename = interfacepath+"\\"+time.strftime("%Y-%m-%d", time.localtime())+'.txt'
#     if not isexists3:
#         os.makedirs(interfacepath.decode('utf-8'))
#     f = open(filename.decode('utf-8'), 'a')
#     f.write(time.strftime("%H:%M:%S", time.localtime())+"  "+neirong+"\n")
#     f.close()
#
# s = [1,2,3,4,5,6,7,8]

# for ss in s :
#     if ss != 5:
#         print(ss)
#     else:
#         break

import shutil
print os.path.abspath(__file__)
print(os.getcwd())
# watch_mysel = 'watch_ 3322'
# shutil.copyfile("tests.py","tests_3.py")

path =  os.path.abspath(__file__)
views_myself = 'views_%s.py' % 9999
shutil.copyfile(os.getcwd()+"/apps/status/views.py",os.getcwd()+"/apps/status/views_response/"+views_myself)
watch_myself = 'watch_%s.html' % 9999
shutil.copyfile("templates/watch.html","templates/watch/"+watch_myself)













