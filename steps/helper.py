__author__ = 'Bene'

from flowEntrys import FlowTable
from behave import *
from hamcrest import *
from mininet.topo import *
from mininet.net import *
from mininet.node import OVSController, RemoteController
import requests

class MininetHelper(object):

    def __init__(self, mininet):
        self.mininetInstanz = mininet

    @classmethod
    def validateNodes(cls, mininet, nodeList):
        for node in nodeList:
            assert node is not None
            assert_that(mininet.__contains__(node), "node %s exists" % node)
        return True

    @classmethod
    def getNodeFromName(cls, mininet, nodeName):
        assert nodeName is not None
        assert_that(mininet.__contains__(nodeName), "node %s exists" % nodeName)
        return mininet.getNodeByName(nodeName)

    @classmethod
    def addSwitches(cls, mininet, numberOfSwitches):
        for i in range (1, numberOfSwitches+1):
            switchName = "s" + str(i)
            #context.testTopo.addSwitch(switchName)
            mininet.addSwitch(switchName)

    @classmethod
    def addHosts(cls, mininet, numberOfHosts):
        for i in range (1, numberOfHosts+1):
            hostName = "h" + str(i)
            mininet.addHost(hostName)

    @classmethod
    def createFullMeshedNet(cls, mininet):
        listOfSwitches = mininet.switches
        listLength = len(listOfSwitches)
        assert_that(listLength, greater_than(1), "More than one switch existing")
        for i in range(0, listLength-1):
            switch1 = str(listOfSwitches[i])
            for j in range(i+1, listLength):
                switch2 = str(listOfSwitches[j])
                mininet.addLink(switch1, switch2)

    @classmethod
    def createFlowTable(cls, switch):
        flows = switch.dpctl("dump-flows")
        return FlowTable(switch, flows)




class NumberConverter(object):
    """Map named numbers into numbers."""
    MAP = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four":  4,
        "five":  5,
        "six":   6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }

    @classmethod
    def convertNumber(cls, number):
        assert number is not None
        if number.isdigit():
            convNumber = int(number)
            assert_that(convNumber, greater_than(0), "number greater than 0")
            return convNumber
        else:
            name = number.strip().lower()
            convNumber = cls.MAP[name]
            assert_that(convNumber, greater_than(0), "number greater than 0")
            return convNumber




