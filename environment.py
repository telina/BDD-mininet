__author__ = 'Bene'

from mininet.topo import *
from mininet.net import *
from mininet.node import OVSController, RemoteController
from mininet.log import MininetLogger
#from mininet.link import *
from mininet.clean import Cleanup
from time import sleep
import os



def before_scenario(context,scenario):
    context.mininetStarted = False
    #create testTopo
    context.testTopo = Topo()
    #check environment variables
    try:
        os.environ['DefaultController'] == True
        chooseDefault = True
    except KeyError:
        chooseDefault = False
    #create remoteController
    port = 6633
    try:
        controllerIP = os.environ['RemoteController']
        if ':' in controllerIP:
            controllerIP, port = controllerIP.split( ':' )
            port = int(port)
        controller = RemoteController('c0', ip=controllerIP, port=port)
    except KeyError:
        if(chooseDefault):
            controller = DefaultController('c0', controller=OVSController)
        else:
            controller = Controller('c0', ip='127.0.0.1', port=6633)
    #create mininet instance with testTopo and a remoteController (alternative: controller=OVSController)
    context.mini = Mininet(topo=context.testTopo, controller=controller, cleanup=True, ipBase='10.0.0.0/8', autoSetMacs=True,
                           waitConnected=True)
    #set LogLevel (default is "output")
    logLevel = 'warning'
    logLevel = 'output'
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
