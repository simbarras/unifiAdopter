# unifiAdopter
Python project who add automatically all antenna from a subnet to a distant controller

This application tests all the addresses of a subnet and if it is a Unifi antenna, it automatically adds it to the controller.
It starts by reading the file `files/config.xml` and takes the following parameters: User, password, controller URL, maximum timeout and subnet. Then, it reads a list of banned addresses from `files/ignoredIp.xml` to save time. Finally, it tests all the addresses and ends up rendering a time statistic and the number of ok, ignored and empty addresses.
Before scanning the network, it is possible to change the settings and stop the application.
The `-noAsk` argument allows you to not require an answer to the question.

## Install on Raspberry

How to install unifiAdopter on Raspberry.
- Download and write the 'Raspberry Pi OS (32-bit) with desktop' image.
- Configure the Raspberry
- Download and configure the 'TeamViewer' application.
- Add this line `hdmi_safe=1` and `hdmi_force_hotplug=1` to `/boot/config.txt`
- Perform the following commands:
```
echo '' > install-unifiAdopter.sh
chmod 775 install-unifiAdopter.sh
nano install-unifiAdopter.sh
```
Write this to the file and execute him with `sudo ./install-unifiAdopter.sh`:
```
#!/bin/bash

# Name		Install-unifiAdopter
# Autor     Simon.Barras02@gmail.com
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
BASHALIASES='/home/pi/.bash_aliases'

pip3 install -e git+https://github.com/simbarras/unifiAdopter.git#egg=unifiAdopter -U

sudo -i -u pi bash << EOF
echo '#!/bin/bash' > $DESKTOP'config-unifiAdopter.sh'
echo '#!/bin/bash' > $DESKTOP'ignoredIp-unifiAdopter.sh'
echo '#!/bin/bash' > $DESKTOP'run-unifiAdopter.sh'
echo '#!/bin/bash' > $DESKTOP'runNoAsk-unifiAdopter.sh'
echo '#!/bin/bash' > $DESKTOP'update-unifiAdopter.sh'
echo '#!/bin/bash' > $DESKTOP'remove-unifiAdopter.sh'
echo '#!/bin/bash' > $DESKTOP'restore-unifiAdopter.sh'

echo 'nano '$SOURCE'files/config.xml' >> $DESKTOP'config-unifiAdopter.sh'
echo 'nano '$SOURCE'files/ignoredIp.xml' >> $DESKTOP'ignoredIp-unifiAdopter.sh'
echo 'python3 '$SOURCE'unifiAdopter.py' >> $DESKTOP'run-unifiAdopter.sh'
echo 'python3 '$SOURCE'unifiAdopter.py -noAsk' >> $DESKTOP'runNoAsk-unifiAdopter.sh'
echo 'python3 '$SOURCE'unifiAdopter.py -restore' >> $DESKTOP'restore-unifiAdopter.sh'

echo 'pip3 install -e git+https://github.com/simbarras/unifiAdopter.git#egg=unifiAdopter -U' >> $DESKTOP'update-unifiAdopter.sh'
echo 'chmod 666 $SOURCE'files/ignoredIp.xml' >> $DESKTOP'update-unifiAdopter.sh'
echo 'chmod 666 $SOURCE'files/config.xml' >> $DESKTOP'update-unifiAdopter.sh'
echo 'chown -R pi:pi /home/pi/src' >> $DESKTOP'update-unifiAdopter.sh'


echo 'pip3 uninstall unifiAdopter -y' >> $DESKTOP'remove-unifiAdopter.sh'
echo 'rm '$DESKTOP'config-unifiAdopter.sh' >> $DESKTOP'remove-unifiAdopter.sh'
echo 'rm '$DESKTOP'ignoredIp-unifiAdopter.sh' >> $DESKTOP'remove-unifiAdopter.sh'
echo 'rm '$DESKTOP'run-unifiAdopter.sh' >> $DESKTOP'remove-unifiAdopter.sh'
echo 'rm '$DESKTOP'runNoAsk-unifiAdopter.sh' >> $DESKTOP'remove-unifiAdopter.sh'
echo 'rm '$DESKTOP'update-unifiAdopter.sh' >> $DESKTOP'remove-unifiAdopter.sh'
echo 'rm '$DESKTOP'restore-unifiAdopter.sh' >> $DESKTOP'remove-unifiAdopter.sh'
echo 'rm '$DESKTOP'unifiAdopter.help' >> $DESKTOP'remove-unifiAdopter.sh'
echo 'rmdir '$DESKTOP'src --ignore-fail-on-non-empty' >> $DESKTOP'remove-unifiAdopter.sh'
echo 'rm '$DESKTOP'remove-unifiAdopter.sh' >> $DESKTOP'remove-unifiAdopter.sh'

echo 'UnifiAdopter help' > $DESKTOP'unifiAdopter.help'
echo 'unifiA-config: Open the unifiAdopter configuration file' >> $DESKTOP'unifiAdopter.help'
echo 'unifiA-ignoredIp: Open the ignored Ip list' >> $DESKTOP'unifiAdopter.help'
echo 'unifiA-run: Run the unifiAdopter application' >> $DESKTOP'unifiAdopter.help'
echo 'unifiA-runNoAsk: Run the unifiAdopter application without questionning' >> $DESKTOP'unifiAdopter.help'
echo 'unifiA-update: Update the unifiAdopter application' >> $DESKTOP'unifiAdopter.help'
echo 'unifiA-restore: Restore the configuration files' >> $DESKTOP'unifiAdopter.help'
echo 'unifiA-remove: Remove the unifiAdopter application' >> $DESKTOP'unifiAdopter.help'

echo 'alias unifiA-="tail '$DESKTOP'unifiAdopter.help"' > $BASHALIASES
echo 'alias unifiA-config="nano '$SOURCE'files/config.xml"' >> $BASHALIASES
echo 'alias unifiA-ignoredIp="nano '$SOURCE'files/ignoredIp.xml"' >> $BASHALIASES
echo 'alias unifiA-run="python3 '$SOURCE'unifiAdopter.py"' >> $BASHALIASES
echo 'alias unifiA-runNoAsk="python3 '$SOURCE'unifiAdopter.py -noAsk"' >> $BASHALIASES
echo 'alias unifiA-restore="python3 '$SOURCE'unifiAdopter.py -restore"' >> $BASHALIASES
echo 'alias unifiA-update="sudo '$DESKTOP'update-unifiAdopter.sh"' >> $BASHALIASES
echo 'alias unifiA-remove="sudo '$DESKTOP'remove-unifiAdopter.sh"' >> $BASHALIASES

chmod 770 $DESKTOP'config-unifiAdopter.sh'
chmod 770 $DESKTOP'ignoredIp-unifiAdopter.sh'
chmod 770 $DESKTOP'run-unifiAdopter.sh'
chmod 770 $DESKTOP'runNoAsk-unifiAdopter.sh'
chmod 770 $DESKTOP'update-unifiAdopter.sh'
chmod 770 $DESKTOP'remove-unifiAdopter.sh'
chmod 660 $DESKTOP'unifiAdopter.help'
sudo chmod 666 $SOURCE'files/ignoredIp.xml'
sudo chmod 666 $SOURCE'files/config.xml'
sudo chown -R pi:pi /home/pi/src

#rm /home/pi/install-unifiAdopter.sh

echo 'Finish'
echo 'Reboot for the command'
#
````
## Use
You need to use the user "pi" and make the command `cd` to be in the folder `/home/pi`.
- Help:
`tail ./unifiAdopter.help` or `unifiA-`

- Configure the parameters:
`./config-unifiAdopter.sh` or `unifiA-config`

- Configure the list of IPs ignored:
`./ignoredIp-unifiAdopter.sh` or `unifiA-ignoredIp`

- Launch the application:
`./run-unifiAdopter.sh` or `unifiA-run`

- Launch the application without questioning:
`./runNoAsk-unifiAdopter.sh` or `unifiA-runNoAsk`

- Update the application:
`sudo ./update-unifiAdopter.sh` or `unifiA-update`

- Restore the configuration files:
`./restore-unifiAdopter.sh` or `unifiA-restore`

- Remove the application:
`sudo ./remove-unifiAdopter.sh` or `unifiA-remove`

###Start wizard
Here is the tree structure of the launch Wizard:
- Would you like to modify the informations ? (y/n) [n]:
  - `y`: Shows all entries and asks if they need to be changed
  - Would you like to overwrite config files ? (y/n) [n]:
    - Overwrite the config file
- Would you like to see the ignored ip ? (y/n) [n]:
  - `y`: Shows all ignored Ip
  - Would you like to modify the ignored ip list? (y/n) [n]:
    - `y`: Shows all ignored Ip and asks if they need to be changed
        - `10.0.0.0`: replace the current Ip by '10.0.0.0'
        - `-`: delete the current Ip
        - `-all`: delete all Ip
      - Writes new range (None = no):
        - `10.0.0.10-10.0.0.15`: add all addresses between '10.0.0.10' and '10.0.0.15'
        - ' ': Go to the next question
      - Writes new address (None = no):
        - `10.0.0.10`: add addresses '10.0.0.10'
        - ' ': Go to the next question
      - Would you like to overwrite the ignored ip files ? (y/n) [n]:
        - `y`: Overwrite the ignored ip file
- Would you like to run the scan ? (y/n) [y]:
  - `n`: Stops the program
- Would you like to add automatically the non-valid ip to the files ? (y/n) [n]:
  - `y`: Add all non-valid ip to the ignored ip file. Useful when you need to run the application 2 times on the same network.
  
#Easter egg
Write kebab83 to the first question