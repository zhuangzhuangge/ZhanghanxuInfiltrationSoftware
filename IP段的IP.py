# coding:utf-8

IP1 = '211.64.160.0'
IP2 = '211.64.191.254'
a = IP1.split('.')[2]
b = IP2.split('.')[2]
c = IP1.split('.')[3]
d = IP2.split('.')[3]
e = IP1.split('.')[0]
f = IP1.split('.')[1]

ipd = []
if a == b:
    for i in range(int(c),int(d)+1):
        ip = str(e) + '.' + str(f) + '.' + str(a) + '.' + str(i)
        ipd.append(ip)
elif a < b:
    for i in range(int(a),int(b)+1):
        for j in range(int(c),int(d)+1):
            ip = str(e) + '.' + str(f) + '.' + str(i) + '.' + str(j)
            ipd.append(ip)
print ipd