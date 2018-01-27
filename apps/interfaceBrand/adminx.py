# -*-coding:utf-8-*- 
__author__ = 'DingWenJing'
_date_ = '2017/12/14 10:37'

import xadmin

from .models import InterType,InterBrand,BrandVersion


class InterTypeAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name','add_time']


class InterBrandAdmin(object):
    list_display = ['name', 'typecourse','desc', 'add_time']
    search_fields = ['name','typecourse__name' ]
    list_filter = ['name','typecourse', 'add_time']

class BrandVersionAdmin(object):
    list_display = ['verison', 'brandcourse', 'ButtMode', 'function', 'desc', 'add_time']
    search_fields = ['verison', 'brandcourse__name', 'ButtMode', 'function']
    list_filter = [ 'brandcourse', 'ButtMode',  'add_time']

xadmin.site.register(InterType, InterTypeAdmin)
xadmin.site.register(InterBrand, InterBrandAdmin)
xadmin.site.register(BrandVersion, BrandVersionAdmin)