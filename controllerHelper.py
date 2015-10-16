__author__ = 'Bene'

from mininet.net import *
from mininet.node import OVSController, RemoteController
import requests
import json
from requests.auth import *

class ControllerSetup(object):

    @classmethod
    def returnController(cls, ip='127.0.0.1', port=6633):
        return RemoteController('c0', ip, int(port))

    @classmethod
    def returnDefaultController(cls):
        return DefaultController('c0', controller=OVSController)


class OnosRestAPI(object):

    def __init__(self, ip, port="8181"):
        self.onosRestEndpoint = 'http://' + ip + ':' + port + '/onos/v1/'
        self.credentials = ('karaf','karaf')
        self.intentIdList = []
        response = requests.delete(self.onosRestEndpoint + 'applications/org.onosproject.fwd/active', auth=(self.credentials))

    def setOnosConfig(self, payload):
        onosConfig = 'configuration/'
        onosAppConfig = 'org.onosproject.fwd.ReactiveForwarding/'
        response = requests.post(self.onosRestEndpoint + onosConfig + onosAppConfig ,json=payload, auth=(self.credentials))

    def setOnosIntent(self, ethSrc, ethDst):
        ethSrc = ethSrc + '/-1'
        ethDst = ethDst + '/-1'
        payload = {
          "type": "HostToHostIntent",
          "appId":"org.onosproject.openflow",
          "priority": "7",
          "one": ethSrc,
          "two": ethDst
        }
        onosIntents = 'intents/'
        postResponse = requests.post(self.onosRestEndpoint + onosIntents, json=payload, auth=(self.credentials))
        sleep(0.5)
        #read all intents, get Id's, convert Id's to decimal, store Id's
        getResponse = requests.get(self.onosRestEndpoint + onosIntents, auth=(self.credentials))
        intentDict = getResponse.json()
        for intent in intentDict.get("intents"):
            self.intentIdList.append(int(intent.get("id"),16))

    def removeOnosIntens(self):
        onosIntents = 'intents/'
        onosApp = 'org.onosproject.openflow/'
        for intentId in self.intentIdList:
            response = requests.delete(self.onosRestEndpoint + onosIntents + onosApp + str(intentId), auth=(self.credentials))