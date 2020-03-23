# coding:utf-8
import threading, Queue, sys
import urllib2

class RedisUN(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue
    def run(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        }
        while True:
            if self._queue.empty():
                break
            number = self._queue.get(timeout=0.5)
            BF = ['/www.zip','/www.rar','/root.zip','/root.rar','/admin.zip','/admin.rar','/1.rar','/1.zip','/123.zip','/123.rar','/wwwroot.zip','/wwwroot.rar','/backup.rar','/backup.zip','/back.rar','/back.zip','/web.rar','/web.zip','/test.zip','/test.rar']
            if 'www' in number:
                xz1='/' + str(number)+'.rar'
                BF.append(xz1)
                xz2='/' + str(number)+'.zip'
                BF.append(xz2)
                xz3 = '/' + number.split('.')[1] + '.rar'
                BF.append(xz3)
                xz4 = '/' + number.split('.')[1] + '.zip'
                BF.append(xz4)
            else:
                xz5 = '/' + number.split('.')[0] + '.rar'
                BF.append(xz5)
                xz6 = '/' + number.split('.')[0] + '.zip'
                BF.append(xz6)
            for i in BF:
                url = 'http://' + str(number)+str(i)
                try:
                    r = urllib2.Request(url,headers=headers)
                    response = urllib2.urlopen(r)
                    info = response.info()
                    size = int(info.getheaders("Content-Length")[0])
                    code = response.code
                    if code==200 and size>51200 :
                        print url
                except:
                    continue
def main():
    f1 = open("C:/Users/zhx/Desktop/YM.txt", "r")
    YM = f1.readlines()
    f1.close()
    thread_count = 50
    threads = []
    queue = Queue.Queue()

    for i in YM:
        queue.put(i.strip())
    for i in xrange(thread_count):
        threads.append(RedisUN(queue))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
if __name__ == '__main__':
    main()