class Addresse:
    ip1 = 0
    ip2 = 0
    ip3 = 0
    ip4 = 0
    mask = 0
    rangeStart1 = 0
    rangeStart2 = 0
    rangeStart3 = 0
    rangeStart4 = 0
    rangeEnd1 = 0
    rangeEnd2 = 0
    rangeEnd3 = 0
    rangeEnd4 = 0

    def __init__(self, ip1, ip2, ip3, ip4, mask, rangeStart, rangeEnd):
        self.ip1 = int(ip1)
        self.ip2 = int(ip2)
        self.ip3 = int(ip3)
        self.ip4 = int(ip4)
        self.mask = int(mask)
        rsip1, rsip2, rsip3, rsip4 = rangeStart.split('.', 4)
        self.rangeStart1 = int(rsip1)
        self.rangeStart2 = int(rsip2)
        self.rangeStart3 = int(rsip3)
        self.rangeStart4 = int(rsip4)
        reip1, reip2, reip3, reip4 = rangeEnd.split('.', 4)
        self.rangeEnd1 = int(reip1)
        self.rangeEnd2 = int(reip2)
        self.rangeEnd3 = int(reip3)
        self.rangeEnd4 = int(reip4)
