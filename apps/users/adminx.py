# -*-coding:utf-8-*-
__author__ = 'DingWenJing'
_date_ = '2017/12/26 10:05'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord

class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
