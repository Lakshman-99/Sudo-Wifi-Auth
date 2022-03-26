from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import random, time, datetime
import string, subprocess, os
import asyncio, json
from net_scan import scan
from net_govern import net_kill
from check import scan
import pandas as pd
import pyrcrack_Modified as pyrcrack
from pymongo import MongoClient
from who_is_on_my_wifi import who

airmon = pyrcrack.AirmonNg()
loop = asyncio.get_event_loop()

app = Flask(__name__)
app.secret_key = 'Sudooo123321'

app.config["MONGO_URI"] = "mongodb+srv://codesploit:codesploit@cluster0.xcehq.mongodb.net/test"
client = MongoClient("mongodb+srv://codesploit:codesploit@cluster0.xcehq.mongodb.net/test")
db = client['SudoWifiAuth']
coll = db["users"]
col = db["NetworkAnalysis"]

async def func():
	lis = [a.asdict() for a in await airmon.interfaces]
	return lis

def conv(dic):
	neslist = []
	for i in dic:
		nl=[]
		lis = list(i.values())
		nl.append(lis[0])
		nl.append(lis[1])
		nl.append(lis[2])
		neslist.append(nl)
	return neslist

@app.route('/',methods=['GET','POST'])
def index():
	return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
	if(request.method == "POST"):
		pas = request.form.get("logpass")
		name = request.form.get("logname")
		email = request.form.get("logemail")
		session['email']=email
		if(name == None):
			detail = coll.find_one({"Email":email})
			print(detail)
			if(detail != None):
				ck = col.find_one({"Email": email})["DeauthCount"]
				if(ck == "0"):
					session['newuser']=True
				else:
					session['newuser']=False
				coll.find_one_and_update({"Email": email },{"$push":{"Activity":{"Status":"User_Logined","Time stamp": datetime.datetime.now() }}})
				return redirect('/iface')
			else:
				return render_template('login.html', msg="Invalid login details!!")
		else:
			coll.insert_one({"Name": name ,"Email": email ,"password": pas,"Time": datetime.datetime.now(),"Activity":[] })
			col.insert_one({"Name":name, "Email":email, "DeauthCount":"0", "interface":"null", "WifiName":"null", "Wifichannel":"null", "WifiMac":"null", "WifiEncyrption":"null", "Superuser":[], "AuthorizedClient":[], "BlackList":[], "Activity":[]})

	return render_template('login.html')

@app.route('/hostss')
def net_view_welcome():
    return render_template('net_view.html',
                           version=''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))

#============================================>

@app.route('/iface',methods=['GET','POST'])
def iface():
	if(request.method == "POST"):
		iface = request.form.get('button')
		session['iface']=iface
		print("interface is " + iface)
		col.find_one_and_update({"Email": session['email'] },{'$set': { "interface" : iface }})
		return redirect('/essid')
	print('* Scanning network')
	hosts = loop.run_until_complete(func())
	print(f'* Deploying hosts: {hosts}')
	ll = []
	for i in hosts:
		v = list(i.values())
		ll.append(v)
	print(ll)
	return render_template('iface.html',host = ll, len=len(ll))

#============================================>

@app.route('/essid', methods=['GET', 'POST'])
def essid():
	print("Inside essid")
	if(request.method == "POST"):
		det = request.form.get('button')
		ess, channel, mac, enc = det.split("=")
		session['Essid']=ess
		session['channel']=channel
		col.find_one_and_update({"Email": session['email'] },{'$set': { "WifiName":ess, "Wifichannel":channel, "WifiMac":mac, "WifiEncyrption":enc }})
		return redirect('/mon')
	return render_template('essid.html')

@app.route('/essid2', methods=['GET', 'POST'])
def essid2():
	iface = session['iface']
	print("Scanning wifi networks!!")
	info = scan(iface)
	print(jsonify(info))
	return jsonify(info)

#============================================>

@app.route('/connect', methods=['GET', 'POST'])
def connect():
	essid = session['Essid']
	print("olll")
	if(request.method == "POST"):
		essid = session['Essid']
		pas = request.form.get('pass')
		iface = session['iface']
		print("HEEYYY")
		os.system(f'sudo sh managed.sh {iface}')
		time.sleep(10)
		subprocess.call(f'nmcli dev wifi connect {essid} password {pas}', shell=True)
		print("HIIIII")
		time.sleep(10)
		return redirect('/mon')

	return render_template('connect.html',name=essid )

#============================================>

@app.route('/mon', methods=['GET', 'POST'])
def mon():
	email=session['email']
	if(request.method=="POST"):
		print("hiii")
		chn = col.find_one({"Email":email})["Wifichannel"]
		iface = session['iface']
		subprocess.call(f"airmon-ng start {iface} {chn}", shell=True)
		return redirect('/brutemon')

	if(session['newuser']):
		return render_template('monitor1.html')
	else:
		chn = col.find_one({"Email":email})["Wifichannel"]
		iface = session['iface']
		subprocess.call(f"airmon-ng start {iface} {chn}", shell=True)
		return redirect('/brutemon')

@app.route('/mon2', methods=['GET', 'POST'])
def mon2():
	WHO = who(40)
	data=[]
	for j in range(0, len(WHO)):
		device=[]
		device.append(WHO[j][1])
		device.append(WHO[j][3])
		device.append(WHO[j][5])
		data.append(device)
	print(data)
	return jsonify(data)

@app.route('/usersel', methods=['GET', 'POST'])
def usersel():
	email=session['email']
	ck = request.form.get('data')
	value = request.form.get("value")
	ip, mac, name = value.split('=')
	print(ip, mac)
	if(ck == "yes"):
		col.find_one_and_update({"Email": email },{"$push":{"AuthorizedClient":{"IpAddress":ip, "MacAddress":mac, "DeviceName":name, "time":datetime.datetime.now()}}})
	else:
		col.find_one_and_update({"Email": email },{"$push":{"BlackList":{"IpAddress":ip, "MacAddress":mac, "DeviceName":name, "time":datetime.datetime.now()}}})
		rmac = col.find_one({"Email":email})["WifiMac"]
		chn = col.find_one({"Email":email})["Wifichannel"]
		iface = session['iface']
		net_kill(mac, rmac, chn, iface)
	return "done"

#============================================>

@app.route('/brutemon', methods=['GET', 'POST'])
def brutemon():
	return render_template('monitor2.html')

@app.route('/brutemon2', methods=['GET', 'POST'])
def brutemon2():
	WHO = who(20)
	data=[]
	for j in range(0, len(WHO)):
		device=[]
		device.append(WHO[j][1])
		device.append(WHO[j][3])
		device.append(WHO[j][5])
		data.append(device)
	print(data)
	email = session['email']
	conuser = col.find_one({"Email":email})["AuthorizedClient"]
	bluser = col.find_one({"Email":email})["BlackList"]
	l_conuser = conv(conuser)
	l_bluser = conv(conuser)
	print("the l_user is "+str(l_conuser))
	print("the l_bluser is "+str(l_bluser))
	newlist1 = [item for item in data if item not in l_conuser]
	print(newlist1)

	black = [item for item in newlist1 if item in l_bluser]
	print(black)

	newu = [item for item in newlist1 if item not in l_bluser]
	print(newu)

	deau = []
	if(black != None):
		for i in black:
			deau.append(i[1])

	return jsonify(data, newu, deau)

#============================================>

@app.route('/hosts')
def net_view_main():
    print('* Scanning network')
    hosts = scan()
    print(f'* Deploying hosts: {hosts}')
    return jsonify(hosts)

@app.route('/deauth', methods=['GET', 'POST'])
def deauth():
	email=session['email']
	ck = request.form.get('data')
	value = request.form.get('value')
	ip, mac, name = value.split('=')
	col.find_one_and_update({"Email": email },{"$push":{"BlackList":{"IpAddress":ip, "MacAddress":mac, "DeviceName":name, "time":datetime.datetime.now()}}})
	rmac = col.find_one({"Email":email})["WifiMac"]
	chn = col.find_one({"Email":email})["Wifichannel"]
	iface = session['iface']
	net_kill(mac, rmac, chn, iface)
	return "done"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
