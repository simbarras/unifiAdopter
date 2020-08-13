import paramiko
import socket


class Ssh:
    ip = ''
    port = 22
    username = ''
    password = ''
    url = ''
    urlPort = 0

    def __init__(self, controllerAntenna):
        self.username = controllerAntenna.user
        self.password = controllerAntenna.mdp
        self.url = controllerAntenna.url
        self.urlPort = controllerAntenna.port

    def addtocontroller(self, ip):
        self.ip = ip
        # self.ip = '10.11.100.53'

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip, self.port, self.username, self.password, timeout=3)

            stdin, stdout, stderr = ssh.exec_command(
                "/usr/bin/mca-cli-op set-inform http://unifi." + self.url + ":" + str(self.urlPort) + "/inform")

            outlines = stdout.readlines()
            outErrors = stderr.readlines()
            if not outlines == []:
                resp = ''.join(outlines)
                return 'Ok'
            elif not outErrors == []:
                errors = ''.join(outErrors)
                return 'Errors: ' + errors
            else:
                return 'No response'
        except socket.timeout:
            return 'Empty'
        except TimeoutError:
            return 'Empty'
        except paramiko.ssh_exception.NoValidConnectionsError:
            return 'Ignored'
        except paramiko.ssh_exception.BadAuthenticationType:
            return 'Ignored'
        except paramiko.ssh_exception.AuthenticationException:
            return 'Ignored'
