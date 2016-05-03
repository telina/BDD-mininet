__author__ = 'Bene'

from mininet.topo import *
from mininet.net import *
from mininet.node import OVSController, RemoteController
from mininet.log import MininetLogger
from mininet.clean import Cleanup
from controllerHelper import ControllerSetup, OnosRestAPI
from openStackHelper import TerraformHelper, NeutronHelper
from time import sleep
import os
from pexpect import pxssh
import json
import subprocess

def before_scenario(context,scenario):
    context.onosFlag=False
    context.openStackTest=False
    ######################################
    #OpenStack Part
    #IF BH_VAR_OPENSTACK=True
    ######################################
    try:
        os.environ['BH_VAR_OPENSTACK'] == True or "true"
        context.openStackTest = True;
    except KeyError:
        context.openStackTest = False;

    if(context.openStackTest):
        # init openstack environment
        # deploy infrastructure with terraform
        context.terraform = TerraformHelper()
        context.terraform.tf_apply()

        # init switch ports with neutronclient
        context.neutron = NeutronHelper()
        # init port_left
        ipServerVM = context.terraform.tf_get("serverVM_ip")
        macServerVM = context.terraform.tf_get("serverVM_mac")
        context.neutron.nt_setIpMacPair("port_left", ipServerVM, macServerVM)
        # init port_right
        ipClientVM = context.terraform.tf_get("clientVM_ip")
        macClientVM = context.terraform.tf_get("clientVM_mac")
        context.neutron.nt_setIpMacPair("port_right", ipClientVM, macClientVM)

        # run ssh command on client
        fipClientVM = context.terraform.tf_get("clientVM_fip")
        fipServerVM = context.terraform.tf_get("serverVM_fip")


        try:
            s = pxssh.pxssh()
            ip = fipClientVM
            username = "ubuntu"
            password = ""
            s.login(ip, username, password)
            s.sendline("ping -c 10 " + ipServerVM)
            s.prompt()
            print(s.before)
            s.sendline("echo $?")
            s.prompt()
            print(s.before)
            tmp = s.before
            s.logout()
            s.close()
        except pxssh.ExceptionPxssh,e:
            print("pxssh failed on login.")
            print(str(e))

        if(tmp.splitlines()[1] == "0"):
            print("ping succeeded")
        else:
            print("ping failed")


        raise Exception("Done")

    else:
    ######################################
    #Mininet & Controller Part
    #IF OPENSTACK=False
    ######################################
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
            context.onosRest = OnosRestAPI(onosIP)
            #prevents flapping behavior of tests. It's not the best solution, but for now it works.
            payload = {"flowTimeout":"5"}
            context.onosRest.setOnosConfig(payload)
            context.onosRest.setOnosIntent("00:00:00:00:00:01", "00:00:00:00:00:02")
            context.onosFlag=True
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
    ######################################
    #OpenStack Part
    #IF OPENSTACK=True
    ######################################
     if(context.openStackTest):
         pass
         #TODO, possibly some code here
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
         pass
         #TODO, possibly some code here
     else:
    ######################################
    #Mininet & Controller Part
    #IF OPENSTACK=False
    ######################################
        if context.onosFlag:
            context.onosRest.removeOnosIntents()
            context.onosFlag=False
        Cleanup.cleanup()

def buildAndStart(context):
    if not context.mininetStarted:
        context.mini.build()
        context.mini.start()
        context.mininetStarted = True
