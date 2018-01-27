from django.shortcuts import render

# Create your views here.
import re
import urllib2
from bs4 import BeautifulSoup as bs
from django.views.generic.base import View


class wduanzi(View):
    def get(self, request):
        requst = urllib2.Request("http://www.tduanzi.com/tweets/118246.html")
        respon = urllib2.urlopen(requst)
        content = respon.read()
        soup = bs(content, 'html.parser')
        s = soup.find_all('span', attrs={"class":"content_f"})
        ss = s.get_text()
        return render(request, 'wduanzi.html', {'wduanzi':ss})