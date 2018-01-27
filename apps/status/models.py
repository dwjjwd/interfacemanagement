# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models

from datetime import datetime
from interfaceBrand.views import BrandVersion
import uuid
# Create your models here.

class Hotelid(models.Model):
    hootelname = models.CharField(max_length=50, verbose_name=u'酒店名')
    kdt = models.CharField(max_length=5, verbose_name=u'KDT')
    hotelid = models.CharField(max_length=10, verbose_name=u'酒店id')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'酒店信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.hootelname

class OpenInterface(models.Model):
    hootelname = models.ForeignKey(Hotelid, verbose_name=u'所属酒店')
    verison = models.ForeignKey(BrandVersion, verbose_name=u'监控接口')
    booleaninter = models.CharField(max_length=6, choices=(('on', u'开'), ('off', u'关')), default='off', verbose_name=u'开启状态')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'接口监控'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        s = '%s[%s%s]' % (self.hootelname.hootelname,self.verison.brandcourse,self.verison.verison)
        return s

class StatusInterface(models.Model):
    hootelname = models.OneToOneField(OpenInterface, verbose_name=u'酒店接口')
    sjdinterfacesta = models.CharField(max_length=20, null=False, verbose_name=u'接口状态')
    port = models.IntegerField(default=0000 , verbose_name=u'监控端口')
    sgo = uuid.uuid1()
    portvercode = models.CharField(max_length=150, default='%s' % sgo, verbose_name=u'接口验证码')
    up_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    cq_time = models.DateTimeField(verbose_name=u'重启时间')

    class Meta:
        verbose_name = u'接口运行状态'
        verbose_name_plural = verbose_name

    # def __unicode__(self):
    #     return self.hootelname

class StatuTCPserver(models.Model):
    ip = models.CharField(max_length=20, verbose_name=u'IP')
    port = models.IntegerField(verbose_name=u'端口')
    nummax = models.IntegerField(verbose_name=u'最大连接数')
    beforenummax = models.IntegerField(verbose_name=u'当前连接数', default=0)
    booleanTCP = models.CharField(max_length=6, choices=(('on', u'开'), ('off', u'关')), default='off', verbose_name=u'开/关')
    booleanTemplate = models.BooleanField(default=False, verbose_name=u'模版生成是/否')
    class Meta:
        verbose_name = u'服务端'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.ip