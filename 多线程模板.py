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
                sys.stdout.write('execute: %s\n' % number)
            except:
                continue


def main():
    work = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    thread_count = 5
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