# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Userinfo(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'姓名')
    department = models.CharField(max_length=30, verbose_name=u'部门')
    mobile = models.CharField(max_length=11, blank=True)
    image = models.ImageField(upload_to='image/%Y/%m',default=u'image/default.png', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'注册时间')

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(verbose_name=u'验证码类型', choices=(('register', u'注册'), ('forget', u'找回密码')), max_length=10)
    send_time = models.DateTimeField(verbose_name=u'发送时间', default=datetime.now)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        # return self.email
        return '{0}({1})'.format(self.code, self.email)