class Addresse:
    ip1 = 0
    ip2 = 0
    ip3 = 0
    ip4 = 0
    mask = 0

    def __init__(self, ip1, ip2, ip3, ip4, mask):
        self.ip1 = int(ip1)
        self.ip2 = int(ip2)
        self.ip3 = int(ip3)
        self.ip4 = int(ip4)
        self.mask = int(mask)
