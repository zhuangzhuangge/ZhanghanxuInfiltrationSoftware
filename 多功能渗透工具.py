# -*- coding: utf-8 -*-
import wx
import wx.xrc
import threading, Queue, sys,requests, re,telnetlib,ipaddr,socket,urllib2,traceback

class YMFC(wx.Frame):    #域名反查框体

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"输入起始IP", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer2.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.input1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.input1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL, 5)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"输入终止IP", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer2.Add(self.m_staticText2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.input2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.input2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_button1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer2)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button1.Bind(wx.EVT_BUTTON, self.start1)

    def __del__(self):
        pass

    def start1(self, event):
        IP1 = self.input1.GetValue()
        IP2 = self.input2.GetValue()
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
            threads.append(RedisUN1(queue))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

class RedisUN1(threading.Thread):   #域名反查多线程
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

class HTSM(wx.Frame):   #后台扫描框体

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, u"输入网址", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)
        bSizer3.Add(self.m_staticText6, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.input3 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer3.Add(self.input3, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText7 = wx.StaticText(self, wx.ID_ANY, u"网站类型", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)
        bSizer3.Add(self.m_staticText7, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.input4 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer3.Add(self.input4, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText8 = wx.StaticText(self, wx.ID_ANY, u"线程数", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)
        bSizer3.Add(self.m_staticText8, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.input5 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer3.Add(self.input5, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_button3 = wx.Button(self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer3.Add(self.m_button3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer3)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button3.Bind(wx.EVT_BUTTON, self.start2)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def start2(self, event):
        # url = raw_input('请输入网址:')
        # txt = raw_input('请输入网站类型(默认php):')
        # tc = raw_input('请输入线程数:')
        url = self.input3.GetValue()
        txt = self.input4.GetValue()
        tc = self.input5.GetValue()
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
            with open(txt, 'r') as fi:
                for each in fi:
                    each = each.replace('\n', '')
                    each = str(url) + each
                    work.append(each)
                fi.close()
        except Exception as e:
            print("打开字典失败！")
            print 'str(e):\t\t', str(e)
            traceback.print_exc()
            print 'traceback.format_exc():\n%s' % traceback.format_exc()

        thread_count = int(tc)
        threads = []
        queue = Queue.Queue()

        for i in work:
            queue.put(i)
        for i in xrange(thread_count):
            threads.append(RedisUN2(queue))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
class RedisUN2(threading.Thread):   #扫描后台多线程
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        while True:
            if self._queue.empty():
                break
            file = open('C:/Users/zhx/Desktop/HT.txt', 'a+')
            try:
                number = self._queue.get(timeout=0.5)
                code = requests.get(number,timeout=5).status_code
                if code==200:
                    file.write(number + '\n')
                    # print number

                # sys.stdout.write('execute: %s\n' % number)
            except:
                continue
            file.close()

class DKSM(wx.Frame):    #端口扫描框体

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText9 = wx.StaticText(self, wx.ID_ANY, u"输入IP", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)
        bSizer4.Add(self.m_staticText9, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.input6 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.input6, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        self.m_button5 = wx.Button(self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_button5, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer4)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button5.Bind(wx.EVT_BUTTON, self.start3)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def start3(self, event):
        ip = self.input6.GetValue()
        # ip = '27.223.70.2'
        work = []
        for port in range(1, 65535):
            work.append(port)
        thread_count = 100
        threads = []
        queue = Queue.Queue()

        for i in work:
            queue.put(i)
        for i in xrange(thread_count):
            threads.append(RedisUN3(queue, ip))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

class RedisUN3(threading.Thread):    #端口扫描多线程
    def __init__(self, queue,ip):
        threading.Thread.__init__(self)
        self._queue = queue
        self._ip = ip

    def run(self):
        while True:
            if self._queue.empty():
                break
            try:
                port = self._queue.get(timeout=0.5)
                ip = self._ip
                # sys.stdout.write('execute: %s\n' % number)
                file = open('C:/Users/zhx/Desktop/KFDK.txt', 'a+')
                server = telnetlib.Telnet()  # 创建一个Telnet对象
                try:
                    server.open(ip, port,timeout=2)  # 利用Telnet对象的open方法进行tcp链接
                    # print('{0} port {1} is open'.format(ip, port))
                    file.write('{0} port {1} is open'.format(ip, port)+ '\n')
                except Exception as err:
                    1
                finally:
                    server.close()
                file.close()
            except:
                continue

class CDSM(wx.Frame):       #C段扫描框体

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText10 = wx.StaticText(self, wx.ID_ANY, u"输入IP段", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)
        bSizer5.Add(self.m_staticText10, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.input7 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer5.Add(self.input7, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        self.m_button7 = wx.Button(self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer5.Add(self.m_button7, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer5)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button7.Bind(wx.EVT_BUTTON, self.start4)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def start4(self, event):
        ports = [80, 81, 82, 88, 90, 8001, 8008, 8080, 8081, 8082, 7001, 8090, 9080, 9090, 9001, 8888]
        # IPduan = raw_input('输入IP段:')  # 接收输入IP段
        IPduan = self.input7.GetValue()
        IPs = ipaddr.IPNetwork(IPduan)
        thread_count = 10
        threads = []
        queue = Queue.Queue()
        for ip in IPs:
            queue.put(ip)
        for i in xrange(thread_count):
            threads.append(RedisUN4(queue, ports))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

class RedisUN4(threading.Thread):    #C段扫描多线程
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
                    file = open('C:/Users/zhx/Desktop/CDSM.txt', 'a+')
                    try:
                        s.connect(addr)
                        s.settimeout(1)
                        # sys.stdout.write('http://'+'%s:%d\n' % (ip, port))

                        file.write('http://'+'%s:%d\n' % (ip, port) + '\n')

                    except Exception,e:
                        s.close()
                        continue
                    file.close()
            except:
                continue

class WZBF(wx.Frame):   #网站备份扫描框体

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        self.m_button16 = wx.Button(self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer6.Add(self.m_button16, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer6)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button16.Bind(wx.EVT_BUTTON, self.start5)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def start5(self, event):
        f1 = open("C:/Users/zhx/Desktop/YM.txt", "r")
        YM = f1.readlines()
        f1.close()
        thread_count = 50
        threads = []
        queue = Queue.Queue()

        for i in YM:
            queue.put(i.strip())
        for i in xrange(thread_count):
            threads.append(RedisUN5(queue))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

class RedisUN5(threading.Thread):     #网站备份多线程
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
                file = open('C:/Users/zhx/Desktop/BF.txt', 'a+')
                try:
                    r = urllib2.Request(url,headers=headers)
                    response = urllib2.urlopen(r)
                    info = response.info()
                    size = int(info.getheaders("Content-Length")[0])
                    code = response.code
                    if code==200 and size>51200 :
                        file.write(url + '\n')
                except:
                    continue
                file.close()

class HOME(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.s1 = wx.Button(self, wx.ID_ANY, u"域名反查", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.s1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.s2 = wx.Button(self, wx.ID_ANY, u"后台扫描", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.s2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.s3 = wx.Button(self, wx.ID_ANY, u"端口开放扫描", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.s3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.s4 = wx.Button(self, wx.ID_ANY, u"C段HTTP扫描", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.s4, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.s5 = wx.Button(self, wx.ID_ANY, u"网站备份扫描", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.s5, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.s1.Bind(wx.EVT_BUTTON, self.switch1)
        self.s2.Bind(wx.EVT_BUTTON, self.switch2)
        self.s3.Bind(wx.EVT_BUTTON, self.switch3)
        self.s4.Bind(wx.EVT_BUTTON, self.switch4)
        self.s5.Bind(wx.EVT_BUTTON, self.switch5)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def switch1(self, event):
        event.Skip()
        F1 = YMFC (frame)
        F1.Show()

    def switch2(self, event):
        event.Skip()
        F2 = HTSM(frame)
        F2.Show()

    def switch3(self, event):
        event.Skip()
        F3 = DKSM(frame)
        F3.Show()

    def switch4(self, event):
        event.Skip()
        F4 = CDSM(frame)
        F4.Show()

    def switch5(self, event):
        event.Skip()
        F5 = WZBF(frame)
        F5.Show()


if __name__ == '__main__':
    app = wx.App()  # 实例化APP
    frame = HOME (None)  # frame的实例
    frame.Show();
    app.MainLoop()  # wxpython的启动函数
