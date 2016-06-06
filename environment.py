__author__ = 'Bene'

from mininet.topo import *
from mininet.net import *
from mininet.node import OVSController, RemoteController
from mininet.log import MininetLogger
from mininet.clean import Cleanup
from controllerHelper import ControllerSetup, OnosRestAPI
from time import sleep
from steps.helper import TerraformHelper
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
