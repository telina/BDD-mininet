__author__ = 'Bene'

from mininet.topo import *
from mininet.net import *
from mininet.node import OVSController, RemoteController
from mininet.log import MininetLogger
from mininet.clean import Cleanup
from controllerHelper import ControllerSetup, OnosRestAPI
from time import sleep
import os
from pexpect import pxssh
import json
import subprocess


def before_all(context):
    #global variables
    context.onosFlag=False
    context.openStackTest=False
    # set LogLevel from environment variable
    # BH_LOG=output is default
    try:
        context.behaveLogLevel = os.environ['BH_LOG']
        if(context.behaveLogLevel == 'WARNING'):
            context.behaveLogLevel = 'warning'
        else:
            context.behaveLogLevel = 'output'
    except KeyError:
        context.behaveLogLevel = "output"
    '''
    test settings
    testing with mininet or openstack
    controller settings
    '''
    #check if test is openStack test
    try:
        openStackTest = os.environ['BH_OPENSTACK'] # == "true"
        #openStack test
        if(openStackTest == "true" or openStackTest == "True" ):
            context.openStackTest = True
        else:
            context.openStackTest = False
    except KeyError:
        #default, mininet test
        context.openStackTest = False
    ######################################
    #OpenStack Part
    #IF BH_VAR_OPENSTACK=True
    ######################################
    if(context.openStackTest == True):
        #any openstack specific code here
        pass
    else:
    ######################################
    #Mininet & Controller Part
    #IF OPENSTACK=False
    ######################################
        # check for controller type
        try:
            onosFlag = os.environ['BH_CONTROLLER_TYPE'] # == "ONOS" or "onos" or "Onos"
            if(onosFlag == "ONOS" or onosFlag == "onos" ):
                context.onosFlag = True
            else:
                context.onosFlag = False
        except KeyError:
            context.onosFlag = False

        # get controller settings (default ip=127.0.0.1, port=6633)
        try:
            controllerIpPort = os.environ['BH_CONTROLLER_IP_PORT']
            if ':' in controllerIpPort:
                context.controllerIp, context.controllerPort = controllerIpPort.split( ':' )
            else:
                context.controllerIp = controllerIpPort
                context.controllerPort = '6633'
        except KeyError:
            # in case no controller IP/port is provided the default 127.0.0.1:6633 is taken
            context.controllerIp = '127.0.0.1'
            context.controllerPort = '6633'
            pass


def before_scenario(context,scenario):
    ######################################
    #OpenStack Part
    #IF BH_VAR_OPENSTACK=True
    ######################################
    if(context.openStackTest == True):
        #any openstack specific code here
        pass
    else:
    ######################################
    #Mininet & Controller Part
    #IF OPENSTACK=False
    ######################################
        #controller is onos
        if(context.onosFlag == True):
            controller = ControllerSetup.returnController(context.controllerIp, context.controllerPort)
            #default port for RestAPI is 8181
            context.onosRest = OnosRestAPI(context.controllerIp)
            #prevents flapping behavior of tests. It's not the best solution, but for now it works.
            payload = {"flowTimeout":"5"}
            context.onosRest.setOnosConfig(payload)
            #context.onosRest.setOnosIntent("00:00:00:00:00:01", "00:00:00:00:00:02")
        # controller is not onos
        else:
            controller = ControllerSetup.returnController(context.controllerIp, context.controllerPort)

        context.mininetStarted = False
        #create testTopo
        context.testTopo = Topo()
        #create mininet instance with testTopo and controller
        context.mini = Mininet(topo=context.testTopo, controller=controller, cleanup=True,
                               ipBase='10.0.0.0/8', autoSetMacs=True, waitConnected=True)
        #set mininet loglevel to global loglevel
        MininetLogger(context.mini).setLogLevel(context.behaveLogLevel)


    # #context.onosFlag=False
    # #context.openStackTest=False
    # ######################################
    # #OpenStack Part
    # #IF BH_VAR_OPENSTACK=True
    # ######################################
    # try:
    #     os.environ['BH_VAR_OPENSTACK'] == True or "true"
    #     context.openStackTest = True
    # except KeyError:
    #     context.openStackTest = False
    #
    # if(context.openStackTest):
    #     pass
    #     #some openstack specific code here
    # else:
    # ######################################
    # #Mininet & Controller Part
    # #IF OPENSTACK=False
    # ######################################
    #     context.mininetStarted = False
    #     #create testTopo
    #     context.testTopo = Topo()
    #     #create controller
    #     try:
    #         onosIpPort = os.environ['ONOS_CONTROLLER']
    #         if ':' in onosIpPort:
    #             onosIP, onosPort = onosIpPort.split( ':' )
    #         onosChosen = True
    #     except KeyError:
    #         onosChosen = False
    #     try:
    #         controllerIpPort = os.environ['REMOTE_CONTROLLER']
    #         if ':' in controllerIpPort:
    #             remoteIP, remotePort = controllerIpPort.split( ':' )
    #         remoteChosen = True
    #     except KeyError:
    #         remoteChosen = False
    #     try:
    #         os.environ['DEFAULT_CONTROLLER'] == True or "true"
    #         defaultChosen = True
    #     except KeyError:
    #         defaultChosen = False
    #     #set controllerspecific
    #     if(onosChosen):
    #         controller = ControllerSetup.returnController(onosIP, onosPort)
    #         #default port for RestAPI is 8181
    #         context.onosRest = OnosRestAPI(onosIP)
    #         #prevents flapping behavior of tests. It's not the best solution, but for now it works.
    #         payload = {"flowTimeout":"5"}
    #         context.onosRest.setOnosConfig(payload)
    #         context.onosRest.setOnosIntent("00:00:00:00:00:01", "00:00:00:00:00:02")
    #         context.onosFlag=True
    #     elif(remoteChosen):
    #         controller = ControllerSetup.returnController(remoteIP, remotePort)
    #     elif(defaultChosen):
    #         controller = ControllerSetup.returnDefaultController()
    #     else:
    #         controller = ControllerSetup.returnController()
    #         #Controller('c0', ip='127.0.0.1', port=6633)
    #
    #     #create mininet instance with testTopo and a controller
    #     context.mini = Mininet(topo=context.testTopo, controller=controller, cleanup=True,
    #                            ipBase='10.0.0.0/8', autoSetMacs=True, waitConnected=True)
    #     #set LogLevel (default is "output")
    #     #logLevel ='warning'
    #     try:
    #         logLevel = os.environ['MININET_LOGLEVEL']
    #         if(not logLevel == 'output'):
    #             logLevel='warning'
    #     except KeyError:
    #         #logLevel standard is 'output'
    #         logLevel = 'warning'
    #     MininetLogger(context.mini).setLogLevel(logLevel)

def before_step(context, step):
    ######################################
    #OpenStack Part
    #IF OPENSTACK=True
    ######################################
     if(context.openStackTest == True):
         #any openstack specific code here
         pass
     else:
    ######################################
    #Mininet & Controller Part
    #IF OPENSTACK=False
    ######################################
        #start mininet when first "when" step is executed
        if(step.step_type == 'when'):
            if not context.mininetStarted:
                 context.mini.build()
                 context.mini.start()
                 context.mininetStarted = True
            #small delay for controller init
            sleep(0.50)

def after_scenario(context,scenario):
    ######################################
    #OpenStack Part
    #IF OPENSTACK=True
    ######################################
     if(context.openStackTest):
        if(context.tf.readyToDestroy == True):
            context.tf.destroy()
            pass
        else:
            print("Please destroy infrastructure manually.")
     else:
    ######################################
    #Mininet & Controller Part
    #IF OPENSTACK=False
    ######################################
        if(context.onosFlag):
            context.onosRest.removeOnosIntents()
            context.onosFlag = False
        Cleanup.cleanup()

# def buildAndStart(context):
#     if not context.mininetStarted:
#         context.mini.build()
#         context.mini.start()
#         context.mininetStarted = True
