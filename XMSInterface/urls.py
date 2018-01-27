"""XMSInterface URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin

from interfaceBrand.views import searchView, detailSearch
from status.views import monitInterface, monitServer, getBlogPosts
from status.views_distributed import distributedServer, buildresponserver
from status.views_response.views_3322 import openWatch3322
from status.views_response.views_3323 import openWatch3323
from status.views_response.views_3324 import openWatch3324
from status.views_response.views_3325 import openWatch3325
from status.views_response.views_3326 import openWatch3326
from status.views_response.views_3327 import openWatch3327
from spider.views import wduanzi

urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^foot/$', TemplateView.as_view(template_name='foot.html'), name='foot'),
    url(r'^head/$', TemplateView.as_view(template_name='header.html'), name='head'),
    url(r'^search/', searchView.as_view(), name='interfaceBrand_search'),
    url(r'^search_detail', detailSearch.as_view(), name='details_search'),
    url(r'^register/$', TemplateView.as_view(template_name='register.html'), name='foot'),
    # url(r'^watch/$', openWatch.as_view(), name='watch'),
    url(r'^watchview_3322/$', openWatch3322.as_view(), name='distributed'),
    url(r'^watchview_3323/$', openWatch3323.as_view(), name='distributed'),
    url(r'^watchview_3324/$', openWatch3324.as_view(), name='distributed'),
    url(r'^watchview_3325/$', openWatch3325.as_view(), name='distributed'),
    url(r'^watchview_3326/$', openWatch3326.as_view(), name='distributed'),
    url(r'^watchview_3327/$', openWatch3327.as_view(), name='distributed'),
    url(r'^monitInterface/$', monitInterface.as_view(), name='monitinter'),
    url(r'^monitServer/$', monitServer.as_view(), name='monitserver'),
    url(r'^distributed/$', distributedServer.as_view(), name='distributed'),
    # url(r'^distributed', destributes.as_view(), name='distributedno2'),
    url(r'^buildresponserver/$', buildresponserver, name='distributed'),
    url(r'^page/$', getBlogPosts, name='getBlogPosts'),
]
