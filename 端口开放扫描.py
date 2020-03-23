# coding:utf-8
import threading, Queue, sys
import requests, re
import telnetlib



class RedisUN(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        while True:
            if self._queue.empty():
                break
            try:
                ip = '27.223.70.2'
                port = self._queue.get(timeout=0.5)
                # sys.stdout.write('execute: %s\n' % number)
                get_ip_status(ip,port)
            except:
                continue


def main():
    # ip = input('IP:')
    work = []
    for port in range(1, 65535):
        work.append(port)
    thread_count = 100
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
def get_ip_status(ip, port):
    server = telnetlib.Telnet()  # 创建一个Telnet对象
    try:
        server.open(ip, port)  # 利用Telnet对象的open方法进行tcp链接
        print('{0} port {1} is open'.format(ip, port))
    except Exception as err:
        1
    finally:
        server.close()

if __name__ == '__main__':
    main()

