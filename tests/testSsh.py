import paramiko

ip = '10.11.100.66'
port = 22
username = 'ubnt'
password = 'ubnt'
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password)

    #stdin, stdout, stderr = ssh.exec_command("uname -a")
    #stdin, stdout, stderr = ssh.exec_command("info")
    # stdin, stdout, stderr = ssh.exec_command("reboot")
    #stdin, stdout, stderr = ssh.exec_command("/bin/ash info")
    stdin, stdout, stderr = ssh.exec_command(" /usr/bin/mca-cli-op set-inform http://unifi.telecomservices.ch:55880/inform")

    outlines = stdout.readlines()
    errors = stderr.readlines()
    resp = ''.join(outlines)
    respErrors = ''.join(errors)
    print('Resp: '+resp)
    print('Err: '+respErrors)
    print('')# Output

except AttributeError:
    print("Erreur inconnue" + stderr)
except TimeoutError:
    print("Erreur de connexion")


