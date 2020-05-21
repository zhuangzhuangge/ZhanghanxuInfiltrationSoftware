#! /usr/bin/env python
#coding=utf-8

import requests
import zlib
import json

def whatweb(url):
    response = requests.get(url,verify=False)
    whatweb_dict = {"url":response.url,"text":response.text,"headers":dict(response.headers)}
    whatweb_dict = json.dumps(whatweb_dict)
    whatweb_dict = whatweb_dict.encode()
    whatweb_dict = zlib.compress(whatweb_dict)
    data = {"info":whatweb_dict}
    return requests.post("http://whatweb.bugscaner.com/api.go",files=data)

if __name__ == '__main__':
    ym = raw_input('请输入网址:')
    request = whatweb(ym)
    # request=whatweb("http://www.xue338.com/")
    print(u"识别结果")
    print(request.json())