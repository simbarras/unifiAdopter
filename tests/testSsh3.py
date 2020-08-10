import subprocess
import sys

HOST = "ubnt@10.11.100.68"
# Ports are handled in ~/.ssh/config since we use OpenSSH
COMMAND = "uname -a"

ssh = subprocess.Popen(["ssh", HOST, COMMAND],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
result = ssh.stdout.readlines()
if result == []:
    error = ssh.stderr.readlines()
    print >> sys.stderr, "ERROR: %s" % error
else:
    print(result)

