#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import re
response = requests.get('https://site.ip138.com/27.223.70.78/')
a=response.text
b=re.findall( r'<li><span class="date">.*</span><a href="/(.*)/" target="_blank">.*</a></li>',a)
print b
