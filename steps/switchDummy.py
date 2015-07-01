__author__ = 'Bene'

# Test class switch,
# later changed to mininet API


class switch(object):
    def __init__(self, switchName=None):
        self.name = switchName
        self.connectionTo = None

    def addLink(self, nameLink1, nameLink2):
        assert nameLink1 is not None
        assert nameLink2 is not None
        if self.name == nameLink1:
            self.connectionTo = nameLink2
            return True
        elif self.name == nameLink2:
            self.connectionTo = nameLink1
            return True
        else:
            return False

    def testLink(self, linkedSwitch):
        assert linkedSwitch is not None
        assert self.connectionTo is not None
        if self.connectionTo == linkedSwitch:
            return True
        else:
            return False
        #assert self.opponent is not None


if __name__ == "__main__":
    s1 = "s1"
    s2 = "s2"
    switch1 = switch(s1)
    switch2 = switch(s2)


    print("Name von Switch1 = " + switch1.name)
    print("Name von Switch2 = " + switch2.name)


    switch1.addLink(s1,s2)

    #print("Switch1 ist verbunden mit " + switch1.connectionTo)
    sX = "s3"
    if switch1.testLink(sX):
     print("Switch1 ist verbunden mit (Methodenaufruf) " + switch1.connectionTo)
    else:
     print("Switch1 ist nicht verbunden mit " + sX)