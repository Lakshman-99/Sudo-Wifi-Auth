import subprocess



lis = [['192.168.0.1', 'c8:3a:35:11:70:90', 'Tenda Technology Co., Ltd. (router)'], ['192.168.0.103', '70:5e:55:5e:8b:e7', 'Realme Chongqing MobileTelecommunications Corp Ltd'], ['192.168.0.106', '50:8f:4c:a7:7b:23', 'Xiaomi Communications Co Ltd']]
iface ="wlan0"
rmac = "c8:3a:35:11:70:90"

tar=[]
for i in lis:
    tar.append(i[1])

print(tar)

#
