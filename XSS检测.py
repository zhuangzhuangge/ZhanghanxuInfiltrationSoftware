# coding:utf-8
import threading, Queue, sys
import requests, re,sys,os

class RedisUN5(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        while True:
            if self._queue.empty():
                break

            try:
                URLpayload = self._queue.get(timeout=0.5)
                URL = URLpayload.split("+")[0]
                payload = URLpayload.split("+")[-1]
                response = requests.get(URL, timeout=5)
                html_ = response.text
                if (html_.find(payload) != -1):
                    print("XSS found:%s" % URL)
                else:
                    print("该payload未检测到XSS")

            except:
                continue


def main():
    def urlsplit(url):
        main_url = url.split("?")[0]
        second_url = url.split("?")[-1]
        dict = {}  # 建立空的字典
        for val in second_url.split("&"):
            dict[val.split("=")[0]] = val.split("=")[-1]  # 给字典填如键和值
        urls = []
        for val in dict.values():
            new_url = main_url + '?' + second_url.replace(val, 'my_Payload')  # 结合
            urls.append(new_url)
        return urls

    XSSURL = []
    # url = input("域名:")
    url = 'https://wmathor.com/python/?a=1&b=2&c=3'
    urls=urlsplit(url)

    f = open("XSSlist","r")
    for i in f:
        for _urls in urls:
            _url = _urls.replace("my_Payload",i)
            _url = _url + '+' + i
            XSSURL.append(_url)

    thread_count = 50
    threads = []
    queue = Queue.Queue()

    for i in XSSURL:
        queue.put(i)
    for i in xrange(thread_count):
        threads.append(RedisUN5(queue))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__ == '__main__':
    main()