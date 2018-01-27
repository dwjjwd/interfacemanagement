# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.contrib.auth.backends import  ModelBackend
from django.views.generic.base import View
from django.db.models import Q

from .models import InterType,InterBrand,BrandVersion,SearchText
import json
# Create your views here.


class searchView(View):
    def get(self, request):
        return render(request, 'index.html', {})
    def post(self, request):
        searchtext = request.POST.get('search_text', '')
        SearchText.objects.create(searchtextw=searchtext)
        s1 = InterBrand.objects.filter(Q(name__icontains=searchtext) | Q(typecourse__name__icontains=searchtext))
        s2 = BrandVersion.objects.filter(Q(verison__icontains=searchtext) | Q(brandcourse__name__icontains=searchtext))
        if s1.__len__() == 0 and s2.__len__() != 0:
            s1 = []
            for ss in s2:
                s1.append(ss.brandcourse)
            return render(request, 'search.html', {'branverlist1':s1, 'branverlist2':s2})
        if s1.__len__() != 0 and s2.__len__() == 0:
            s2 = []
            for ss in s1:
                sg = BrandVersion.objects.filter(brandcourse=ss)
                if sg.__len__() != 0:
                    for sg1 in sg:
                        s2.append(sg1)
            return render(request, 'search.html', {'branverlist1':s1, 'branverlist2':s2})
        return render(request, 'search.html', {'branverlist1':s1, 'branverlist2':s2})

class detailSearch(View):
    def get(self, request):
        interbrandid = request.GET.get('interbrandid')
        brandversionid = request.GET.get('brandversionid')
        if interbrandid is not None:
            intbrand = InterBrand.objects.get(id=interbrandid)
            return render(request, 'detail.html', {"InterBrand":intbrand})
        if brandversionid is not None:
            branver = BrandVersion.objects.get(id=brandversionid)
            return render(request, 'detail.html', {"BrandVersion":branver})
    def post(self, request):
        return render(request, 'search.html', {})
