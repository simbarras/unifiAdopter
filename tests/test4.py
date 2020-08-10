import os
hostname = "ubnt@10.11.100.68" #example
response = os.system("ssh " + hostname)

#and then check the response...
if response == 0:
  print(hostname, 'is up!')
else:
  print(hostname, 'is down!')