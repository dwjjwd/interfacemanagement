from django.test import TestCase

# Create your tests here.
import re
import urllib2
from bs4 import BeautifulSoup as bs

requst = urllib2.Request("http://www.tduanzi.com/tweets/118246.html")
respon = urllib2.urlopen(requst)
content = respon.read()
soup = bs(content, 'html.parser')
s = soup.find_all('span', attrs={"class":"content_f"})#, Class='content_f'
for ss in s:
    print(ss.get_text())