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
                response = requests.get(number,timeout=5)
                c = response.text
                d = re.findall(r'src="(.*.jpg)" alt=', c)
                sys.stdout.write('%s %s\n' %(d,number))

            except:
                continue


def main():
    # work = [1,2, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    work = []
    for i in range(1, 11):
        j = 'https://m.51tietu.net/pic/cosplay/' + str(i)
        work.append(j)
    works = []
    for i in work:
        response = requests.get(i)
        a = response.text
        b = re.findall(r'href="(.*?.html)" title=', a)

        # sys.stdout.write('%s\n' % b)
        for j in b:
            j = 'https://m.51tietu.net/' + j
            works.append(str(j))
    thread_count = 5
    threads = []
    queue = Queue.Queue()

    for i in works:
        queue.put(i)
    for i in xrange(thread_count):
        threads.append(RedisUN(queue))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    main()