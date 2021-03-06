# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-28 10:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BrandVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verison', models.CharField(max_length=20, verbose_name='\u7248\u672c\u53f7')),
                ('ButtMode', models.CharField(max_length=20, verbose_name='\u5bf9\u63a5\u65b9\u5f0f')),
                ('function', models.CharField(max_length=50, verbose_name='\u5177\u5907\u529f\u80fd')),
                ('desc', models.CharField(max_length=100, verbose_name='\u63cf\u8ff0')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u63a5\u53e3\u7248\u672c\u578b\u53f7',
                'verbose_name_plural': '\u63a5\u53e3\u7248\u672c\u578b\u53f7',
            },
        ),
        migrations.CreateModel(
            name='InterBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u54c1\u724c\u540d')),
                ('desc', models.CharField(max_length=100, verbose_name='\u63cf\u8ff0')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u63a5\u53e3\u54c1\u724c',
                'verbose_name_plural': '\u63a5\u53e3\u54c1\u724c',
            },
        ),
        migrations.CreateModel(
            name='InterType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u63a5\u53e3\u7c7b\u578b')),
                ('desc', models.CharField(max_length=100, verbose_name='\u63cf\u8ff0')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u63a5\u53e3\u7c7b\u578b',
                'verbose_name_plural': '\u63a5\u53e3\u7c7b\u578b',
            },
        ),
        migrations.CreateModel(
            name='SearchText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('searchtextw', models.CharField(max_length=200, verbose_name='\u641c\u7d22\u5173\u952e\u8bcd')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
            ],
        ),
        migrations.AddField(
            model_name='interbrand',
            name='typecourse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interfaceBrand.InterType', verbose_name='\u63a5\u53e3\u7c7b\u578b'),
        ),
        migrations.AddField(
            model_name='brandversion',
            name='brandcourse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interfaceBrand.InterBrand', verbose_name='\u6240\u5c5e\u54c1\u724c'),
        ),
    ]
