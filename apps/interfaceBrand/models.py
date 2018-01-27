# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

# Create your models here.

class InterType(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'接口类型')
    desc = models.CharField(max_length=100, verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'接口类型'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

class InterBrand(models.Model):
    typecourse = models.ForeignKey(InterType, verbose_name=u'接口类型')
    name = models.CharField(max_length=50, verbose_name=u'品牌名')
    desc = models.CharField(max_length=100, verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'接口品牌'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

class BrandVersion(models.Model):
    brandcourse = models.ForeignKey(InterBrand, verbose_name=u'所属品牌')
    verison = models.CharField(max_length=20, verbose_name=u"版本号")
    ButtMode = models.CharField(max_length=20, verbose_name=u"对接方式")
    function = models.CharField(max_length=50, verbose_name=u"具备功能")
    desc = models.CharField(max_length=100, verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'接口版本型号'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '%s %s' % (self.brandcourse, self.verison)

class SearchText(models.Model):
    searchtextw = models.CharField(max_length=200, verbose_name=u'搜索关键词')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')