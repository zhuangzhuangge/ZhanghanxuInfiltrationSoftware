# coding:utf-8
import threading, Queue, sys
import requests, re

class RedisUN(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        while True:
            if self._queue.empty():
                break
            try:
                number = self._queue.get(timeout=0.5)
                code = requests.get(number,timeout=5).status_code
                if code==200:
                    print number

                # sys.stdout.write('execute: %s\n' % number)
            except:
                continue


def main():
    url = raw_input('请输入网址:')
    txt = raw_input('请输入网站类型(默认php):')
    tc = raw_input('请输入线程数:')
    work = []
    if txt == '':
        txt = 'C:\Users\zhx\PycharmProjects\untitled\PHP.txt'
    elif txt == 'asp' or 'ASP':
        txt = 'C:\Users\zhx\PycharmProjects\untitled\ASP.txt'
    elif txt == 'aspx':
        txt = 'C:\Users\zhx\PycharmProjects\untitled\ASPX.txt'
    elif txt == 'php':
        txt = 'C:\Users\zhx\PycharmProjects\untitled\PHP.txt'
    elif txt == 'jsp':
        txt = 'C:\Users\zhx\PycharmProjects\untitled\JSP.txt'
    else:
        print '输入的网站类型错误!'
    try:
        with open(txt, 'r') as f:
            for each in f:
                each = each.replace('\n', '')
                each = url + each
                work.append(each)
            f.close()
    except:
        print("打开字典失败！")
    thread_count = int(tc)
    threads = []
    queue = Queue.Queue()

    for i in work:
        queue.put(i)
    for i in xrange(thread_count):
        threads.append(RedisUN(queue))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    main()