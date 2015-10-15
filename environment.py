__author__ = 'Bene'

from mininet.topo import *
from mininet.net import *
from mininet.node import OVSController, RemoteController
from mininet.log import MininetLogger
from mininet.clean import Cleanup
from controllerHelper import ControllerSetup, OnosRestAPI
from time import sleep
import os

def before_scenario(context,scenario):
    context.mininetStarted = False
    #create testTopo
    context.testTopo = Topo()
    #create controller
    try:
        onosIpPort = os.environ['ONOS_CONTROLLER']
        if ':' in onosIpPort:
            onosIP, onosPort = onosIpPort.split( ':' )
        onosChosen = True
    except KeyError:
        onosChosen = False
    try:
        controllerIpPort = os.environ['REMOTE_CONTROLLER']
        if ':' in controllerIpPort:
            remoteIP, remotePort = controllerIpPort.split( ':' )
        remoteChosen = True
    except KeyError:
        remoteChosen = False
    try:
        os.environ['DEFAULT_CONTROLLER'] == True or "true"
        defaultChosen = True
    except KeyError:
        defaultChosen = False
    #set controllerspecific
    if(onosChosen):
        controller = ControllerSetup.returnController(onosIP, onosPort)
        #default port for RestAPI is 8181
        onosRest = OnosRestAPI(onosIP)
        #prevents flapping behavior of tests. It's not the best solution, but for now it works.
        payload = {"flowTimeout":"5"}
        onosRest.setOnosConfig(payload)
    elif(remoteChosen):
        controller = ControllerSetup.returnController(remoteIP, remotePort)
    elif(defaultChosen):
        controller = ControllerSetup.returnDefaultController()
    else:
        controller = ControllerSetup.returnController()
        #Controller('c0', ip='127.0.0.1', port=6633)

    #create mininet instance with testTopo and a controller
    context.mini = Mininet(topo=context.testTopo, controller=controller, cleanup=True,
                           ipBase='10.0.0.0/8', autoSetMacs=True, waitConnected=True)
    #set LogLevel (default is "output")
    #logLevel ='warning'
    try:
        logLevel = os.environ['MININET_LOGLEVEL']
        if(not logLevel == 'output'):
            logLevel='warning'
    except KeyError:
        #logLevel standard is 'output'
        logLevel = 'warning'
    MininetLogger(context.mini).setLogLevel(logLevel)

def before_step(context, step):
    #start mininet when first "when" step is executed
    if(step.step_type == 'when'):
        if not context.mininetStarted:
             context.mini.build()
             context.mini.start()
             context.mininetStarted = True
        #small delay for controller init
        sleep(0.50)

def after_scenario(context,scenario):
    Cleanup.cleanup()

def buildAndStart(context):
    if not context.mininetStarted:
        context.mini.build()
        context.mini.start()
        context.mininetStarted = True
