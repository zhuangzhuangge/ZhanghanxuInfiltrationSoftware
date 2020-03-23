# coding:utf-8
import threading, Queue, sys
import ftplib,socket


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
                # sys.stdout.write('execute: %s\n' % number)

            except:
                continue


def main():
    work = []
    txt = 'C:\Users\zhx\PycharmProjects\untitled\passwd.txt'
    try:
        with open(txt, 'r') as f:
            for each in f:
                each = each.replace('\n', '')
                work.append(each)
            f.close()
    except:
        print("打开字典失败！")
    thread_count = 40
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