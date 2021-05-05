import requests as req
from scp import SCPClient
import paramiko
import uuid
import sys
import time

uuid = uuid.uuid1()

if len(sys.argv) != 3:
	print("USAGE: python3 stress.py bad_ip bad_fqdn")
	exit()
bad_ip = sys.argv[1]
bad_host = sys.argv[2]

c = 1

while c == 1:
	# benign web traffic
	print("Benign traffic")
	req.get("https://gamesgames.com")
	req.get("http://website.org")
	# benign remote file download
	print("Benign remote file download")
	download = req.get("https://pbs.twimg.com/media/EFDZ8YFXYAELYLW.jpg")
	open('possum', 'wb').write(download.content)
	# malicious web traffic
	print("Malicious web")
	try:
		req.get("https://{bad_ip}")
	except:
		pass
	try:
		req.get("http://{bad_host}")
	except:
		pass
	# malicious remote file download
	print("EICAR 1-4")
	try:
		e1 = req.get("https://secure.eiccar.org/eicar.com")
		open('eicar.com', 'wb').write(e1.content)
	except:
		print("Couldn't reach network")
	try:
		e2 = req.get("https://secure.eiccar.org/eicar.com.txt")
		open('eicar.com.txt', 'wb').write(e2.content)
	except:
		print("Couldn't reach network")
	try:
		e3 = req.get("https://secure.eiccar.org/eicar_com.zip")
		open('eicar_com.zip', 'wb').write(e3.content)
	except:
		print("Couldn't reach network")
	try:
		e4 = req.get("https://secure.eiccar.org/eicarcom2.zip")
		open('eicarcom2.zip', 'wb').write(e4.content)
	except:
		print("Couldn't reach network")
	# ssh to host
	print("SSH access")
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
	client.connect('192.168.1.4', 22, 'sshuser', 'weakpassword')
	stdin, stdout, stderr = client.exec_command('pwd')
	# internal file transfer
	print("SCP")
	scp = SCPClient(client.get_transport())
	scp.put('possum', f'scp_possum_{uuid}')
	# zip file transfer
	print("Zip transfers")
	scp.put('eicar_com.zip', f'bad_file_{uuid}')
	scp.put('test.zip', f'test_zip_{uuid}')
	c = 0
