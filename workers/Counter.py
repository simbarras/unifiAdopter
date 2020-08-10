class Counter:
    ip1 = 0
    ip2 = 0
    ip3 = 0
    ip4 = 0
    mask = 0
    host = '0.0.0.0'

    def __init__(self, adresseSubnet):
        self.ip1 = adresseSubnet.ip1
        self.ip2 = adresseSubnet.ip2
        self.ip3 = adresseSubnet.ip3
        self.ip4 = adresseSubnet.ip4
        self.mask = adresseSubnet.mask

    def counter(self):
        if self.ip4 == 255:
            self.ip4 = 0
            if self.ip3 == 255:
                self.ip3 = 0
                if self.ip2 == 255:
                    self.ip2 = 0
                    if self.ip1 == 255:
                        self.ip1 = 0
                    else:
                        self.ip1 = self.ip1 + 1
                else:
                    self.ip2 = self.ip2 + 1
            else:
                self.ip3 = self.ip3 + 1
        else:
            self.ip4 = self.ip4 + 1

        self.host = str(self.ip1) + "." + str(self.ip2) + "." + str(self.ip3) + "." + str(self.ip4)
        return self.host
