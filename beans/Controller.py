class Controller:
    user = ''
    mdp = ''
    url = ''
    port = 0

    def __init__(self, user, mdp, url, port):
        self.user = user
        self.mdp = mdp
        self.url = url
        self.port = int(port)
