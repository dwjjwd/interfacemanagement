# -*-encoding:utf-8-*-
__author__ = 'DingWenJing'
_date_ = '2017/12/27 13:51'

import xadmin
from .models import Hotelid,OpenInterface,StatuTCPserver,StatusInterface
from xadmin import views

class GlobalSetting(object):
    site_title = '西软科技'   #设置头标题
    site_footer = '杭州西软科技'  #设置脚标题

class HotelidAdmin(object):
    list_display = ['hootelname', 'kdt', 'hotelid','add_time']
    search_fields = ['hootelname', 'kdt', 'hotelid','add_time']
    list_filter =  ['hootelname', 'kdt', 'hotelid','add_time']

class OpenInterfaceAdmin(object):
    list_display = ['hootelname', 'verison', 'booleaninter', 'add_time']
    search_fields = ['hootelname', 'verison', 'booleaninter', 'add_time']
    list_filter =  ['hootelname', 'verison', 'booleaninter', 'add_time']

class StatusInterfaceAdmin(object):
    list_display = ['hootelname', 'sjdinterfacesta', 'port', 'portvercode', 'up_time', 'cq_time']
    search_fields = ['sjdinterfacesta']
    list_filter = ['hootelname', 'up_time', 'cq_time']

class StatuTCPserverAdmin(object):
    list_display = ['ip', 'port', 'nummax', 'beforenummax', 'booleanTCP', 'booleanTemplate']

xadmin.site.register(Hotelid, HotelidAdmin)
xadmin.site.register(OpenInterface, OpenInterfaceAdmin)
xadmin.site.register(StatusInterface, StatusInterfaceAdmin)
xadmin.site.register(StatuTCPserver, StatuTCPserverAdmin)
xadmin.site.register(views.CommAdminView, GlobalSetting)