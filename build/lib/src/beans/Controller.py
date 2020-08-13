class Controller:
    user = ''
    mdp = ''
    url = ''
    port = 0
    timeout = 0

    def __init__(self, user, mdp, url, port, timeout):
        self.user = user
        self.mdp = mdp
        self.url = url
        self.port = int(port)
        self.timeout = int(timeout)
