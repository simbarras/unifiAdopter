import paramiko

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname='10.11.100.68',
                       username='ubnt',
                       password='ubnt')
stdin, stdout, stderr = ssh_client.exec_command('info')

out = stdout.read().decode().strip()
error = stderr.read().decode().strip()

if error:
    raise Exception('There was an error pulling the runtime: {}'.format(error))
ssh_client.close()

print(out)