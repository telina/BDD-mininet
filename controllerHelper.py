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

    # @classmethod
    # def returnDefaultController(cls):
    #     return DefaultController('c0', controller=OVSController)


class OnosRestAPI(object):

    def __init__(cls, ip, port="8181"):
        cls.onosRestEndpoint = 'http://' + ip + ':' + port + '/onos/v1/'
        cls.credentials = ('karaf','karaf')
        cls.intentIdList = []
        response = requests.delete(cls.onosRestEndpoint + 'applications/org.onosproject.fwd/active', auth=(cls.credentials))

    def setOnosConfig(cls, payload):
        onosConfig = 'configuration/'
        onosAppConfig = 'org.onosproject.fwd.ReactiveForwarding/'
        response = requests.post(cls.onosRestEndpoint + onosConfig + onosAppConfig ,json=payload, auth=(cls.credentials))

    def setOnosIntent(cls, ethSrc, ethDst):
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
        postResponse = requests.post(cls.onosRestEndpoint + onosIntents, json=payload, auth=(cls.credentials))
        sleep(0.5)
        #read all intents, get Id's, convert Id's to decimal, store Id's
        getResponse = requests.get(cls.onosRestEndpoint + onosIntents, auth=(cls.credentials))
        intentDict = getResponse.json()
        for intent in intentDict.get("intents"):
            cls.intentIdList.append(int(intent.get("id"),16))

    def removeOnosIntents(cls):
        onosIntents = 'intents/'
        onosApp = 'org.onosproject.openflow/'
        for intentId in cls.intentIdList:
            response = requests.delete(cls.onosRestEndpoint + onosIntents + onosApp + str(intentId), auth=(cls.credentials))