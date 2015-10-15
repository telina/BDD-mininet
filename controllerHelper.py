__author__ = 'Bene'

from mininet.net import *
from mininet.node import OVSController, RemoteController
import requests

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

    def setOnosConfig(self, payload):
        onosConfig = 'configuration/'
        onosAppConfig = 'org.onosproject.fwd.ReactiveForwarding/'
        response = requests.post(self.onosRestEndpoint + onosConfig + onosAppConfig ,json=payload)
        return response

    #not jet tested
    def setOnosIntent(self, ethSrc, ethDst):
        payload = {"add-host-intent":{ethSrc:ethDst}}
        onosIntents = 'intents/'
        reponse = requests.post(self.onosRestEndpoint + onosIntents, json=payload)