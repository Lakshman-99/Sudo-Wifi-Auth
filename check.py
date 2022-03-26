import subprocess
import numpy as np
import pandas as pd
import requests
import time
import os

from pandas import DataFrame
import sys, select


def scan(iface):
    p = subprocess.Popen(['airodump-ng','-w hi',iface], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)       # line-1.1
    time.sleep(20)                                                                                                                    # line-1.2
    p.kill()                                                                                                                          # line-1.3 running airodump-ng
    df=pd.read_csv(" hi-01.csv", usecols=[0,13,3,4,5,7])
    data=df.dropna()
    lis = data.values.tolist()
    print(lis)
    for i in lis:
        for j in range(len(i)):
            i[j] = i[j].strip()
            print(i[j])

    print(lis)

    subprocess.run(['rm',' hi-01.csv'])
    subprocess.run(['rm',' hi-01.log.csv'])
    subprocess.run(['rm',' hi-01.kismet.csv'])
    subprocess.run(['rm',' hi-01.kismet.netxml'])
    subprocess.run(['rm',' hi-01.cap'])
    return lis
