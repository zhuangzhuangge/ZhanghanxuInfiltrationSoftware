# coding:utf-8
import socket
socket.setdefaulttimeout(1)
import ipaddr,time,sys,socket,threading, Queue,requests
class RedisUN(threading.Thread):
    def __init__(self, queue, ports):
        threading.Thread.__init__(self)
        self._queue = queue
        self._ports = ports
    def run(self):
        while True:
            if self._queue.empty():
                break
            try:
                ip = self._queue.get(timeout=0.5)
                for port in self._ports:
                    addr = (str(ip), port)
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        s.connect(addr)
                        s.settimeout(1)
                        sys.stdout.write('http://'+'%s:%d\n' % (ip, port))
                    except Exception,e:
                        s.close()
                        continue
            except:
                continue
def main():
    ports = [80, 81,82,88,90,8001,8008, 8080, 8081,8082,7001, 8090,9080,9090,9001,8888]
    IPduan = raw_input('输入IP段:')  # 接收输入IP段
    IPs = ipaddr.IPNetwork(IPduan)
    thread_count = 10
    threads = []
    queue = Queue.Queue()
    for ip in IPs:
        queue.put(ip)
    for i in xrange(thread_count):
        threads.append(RedisUN(queue, ports))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
if __name__ == '__main__':
    time1 = time.time()
    main()
    print time.time()-time1