# unifiAdopter
Python project who add automaticly all antenna from a subnet to a distant controller

This application tests all the addresses of a subnet and if it is a Unifi antenna, it automatically adds it to the controller.
It starts by reading the file `files/config.xml` and takes the following parameters: User, password, controller URL, maximum timeout and subnet. Then, it reads a list of banned addresses from `files/ignoredIp.xml` to save time. Finally, it tests all the addresses and ends up rendering a time statistic and the number of ok, ignored and empty addresses.
Before scanning the network, it is possible to change the settings and stop the application.
The `-noAsk` argument allows you to not require an answer to the question.

# Install on Raspberry

How to install unifiAdopter on Raspberry.
- Download and write the 'Raspberry Pi OS (32-bit) with desktop' image.
- Configure the Raspberry
- Download and configure the 'TeamViewer' application.
- Enable booting on the console.
- Perform the following commands:
```
sudo echo '' > install-unifiAdopter.sh
sudo chown root_root install-unifiAdopter.sh
sudo chmod 4777 install-unifiAdopter.sh
sudo nano install-unifiAdopter.sh
```
Write this to the file:
```
#!/bin/bash

# Name		Install-unifiAdopter
# Autor	Simon.Barras02@gmail.com
# Version	1.0
# Date		12.08.2020
# Descrition	Install the following GitHub project: https://github.com/simbarras/unifiAdopter
############################################################################################

apt-get update -y
apt-get upgrade -y

apt-get install python3 -y
apt-get install python3-pip -y

DESKTOP='/home/pi/'
SOURCE='/home/pi/src/unifiadopter/src/'

pip3 install -e git+https://github.com/simbarras/unifiAdopter.git#egg=unifiAdopter -U

echo '#!/bin/bash' > $DESKTOP'config-unifiAdopter.sh'
echo '#!/bin/bash' > $DESKTOP'ignoredIp-unifiAdopter.sh'
echo '#!/bin/bash' > $DESKTOP'run-unifiAdopter.sh'
echo '#!/bin/bash' > $DESKTOP'runNoAsk-unifiAdopter.sh'
echo '#!/bin/bash' > $DESKTOP'update-unifiAdopter.sh'

echo 'nano '$SOURCE'files/config.xml' >> $DESKTOP'config-unifiiAdopter.sh'
echo 'nano '$SOURCE'files/ignpredIp.xml' >> $DESKTOP'ignoredIp-unifiiAdopter.sh'
echo 'python3 '$SOURCE'unifiAdopter.py' >> $DESKTOP'run-unifiiAdopter.sh'
echo 'python3 '$SOURCE'unifiAdopter.py -noAsk' >> $DESKTOP'runNoAsk-unifiiAdopter.sh'
echo 'pip3 install -e git+https://github.com/simbarras/unifiAdopter.git#egg=unifiAdopter -U' >> $DESKTOP'update-unifiiAdopter.sh'

chown root:root $DESKTOP'config-unifiiAdopter.sh'
chown root:root $DESKTOP'ignoredIp-unifiiAdopter.sh'
chown root:root $DESKTOP'run-unifiiAdopter.sh'
chown root:root $DESKTOP'runNoAsk-unifiiAdopter.sh'
chown root:root $DESKTOP'update-unifiiAdopter.sh'

chmod 4777 $DESKTOP'config-unifiiAdopter.sh'
chmod 4777 $DESKTOP'ignoredIp-unifiiAdopter.sh'
chmod 4777 $DESKTOP'run-unifiiAdopter.sh'
chmod 4777 $DESKTOP'runNoAsk-unifiiAdopter.sh'
chmod 4777 $DESKTOP'update-unifiiAdopter.sh'

#rm /home/pi/install-unifiAdopter.sh

echo 'finish'

#
````
# Use
- Configure the parameters:
`sudo ./config-unfiAdopter.sh`

- Configure the list of IPs ignored:
`sudo ./ignoredIp-unfiAdopter.sh`

- Launch the application:
`sudo ./run-unfiAdopter.sh`

- Launch the application without questioning:
`sudo./runNoAsk-unfiAdopter.sh`

- Update the application:
`sudo ./update-unifiAdopter.sh`