# coding:utf-8
import threading, Queue, sys
import requests, re

class RedisUN(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue
    def run(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',}
        while True:
            if self._queue.empty():
                break
            number = self._queue.get(timeout=0.5)
            response = requests.get('https://site.ip138.com/' + str(number) , headers=headers)
            t = response.content
            b = re.findall(r'<li><span class="date">.*</span><a href="/(.*)/" target="_blank">.*</a></li>', t)
            file = open('C:/Users/zhx/Desktop/YM.txt', 'a+')
            # for i in b:
            try:
                # u = 'http://' + i
                u = 'http://' + b[0]
                r = requests.get(url=u, headers=headers,timeout=5).status_code
                if r == 200:
                    # sys.stdout.write('%s\n' % u)
                    # file.write(str(i) + '\n')
                    # file.write(str(i) + ' : ' + str(number) + '\n')
                    file.write(str(b[0]) + ' : ' + str(number) + '\n')
            except:
                continue
            file.close()
def main():
    # IP1 = input('起始IP:')
    # IP2 = input('终止IP:')
    IP1 = sys.argv[1]
    IP2 = sys.argv[2]
    # IP1 = '27.223.70.1'
    # IP2 = '27.223.70.128'
    a = IP1.split('.')[2]
    b = IP2.split('.')[2]
    c = IP1.split('.')[3]
    d = IP2.split('.')[3]
    e = IP1.split('.')[0]
    f = IP1.split('.')[1]
    ipd = []
    if a == b:
        for i in range(int(c), int(d) + 1):
            ip = str(e) + '.' + str(f) + '.' + str(a) + '.' + str(i)
            ipd.append(ip)
    elif a < b:
        for i in range(int(a), int(b) + 1):
            for j in range(int(c), int(d) + 1):
                ip = str(e) + '.' + str(f) + '.' + str(i) + '.' + str(j)
                ipd.append(ip)
    thread_count = 20
    threads = []
    queue = Queue.Queue()
    for i in ipd:
        queue.put(i)
    for i in xrange(thread_count):
        threads.append(RedisUN(queue))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
if __name__ == '__main__':
    main()