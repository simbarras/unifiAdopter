# unifiAdopter
Python project who add automaticly all antenna from a subnet to a distant controller

This application tests all the addresses of a subnet and if it is a Unifi antenna, it automatically adds it to the controller.
It starts by reading the file `files/config.xml` and takes the following parameters: User, password, controller URL, maximum timeout and subnet. Then, it reads a list of banned addresses from `files/ignoredIp.xml` to save time. Finally, it tests all the addresses and ends up rendering a time statistic and the number of ok, ignored and empty addresses.
Before scanning the network, it is possible to change the settings and stop the application.
The `-noAsk` argument allows you to not require an answer to the question.
