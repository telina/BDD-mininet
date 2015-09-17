__author__ = 'Bene'

from mininet.topo import *
from mininet.net import *
from mininet.node import OVSController, RemoteController
from mininet.log import MininetLogger
from mininet.link import *
from mininet.clean import *
from mininet import net
from functools import partial
from mininet.clean import Cleanup
#from mininet.examples.vlanhost import *
import logging

#logging.basicConfig(filename='example.log',level=logging.DEBUG)

def before_scenario(context,scenario):
    context.mininetStarted = False
    #create testTopo
    context.testTopo = Topo()
    #create remoteController
    onosController = RemoteController('c0', ip='192.168.59.103', port=6633)
    onosController2 = RemoteController('c0', ip = '192.168.0.100', port=6633)
    #create mininet instance with testTopo and a remoteController (alternative: controller=OVSController)
    context.mini = Mininet(topo=context.testTopo, controller=onosController2, cleanup=True, ipBase='10.0.0.0/8', autoSetMacs=True,
                           waitConnected=True)
    #set LogLevel (default is "output")
    logLevel = 'warning'
    MininetLogger(context.mini).setLogLevel(logLevel)

def before_step(context, step):
    #start mininet when first "when" step is executed
    if(step.step_type == 'when'):
        if not context.mininetStarted:
             context.mini.build()
             context.mini.start()
             context.mininetStarted = True


def after_scenario(context,scenario):
    Cleanup.cleanup()


def buildAndStart(context):
    if not context.mininetStarted:
        context.mini.build()
        context.mini.start()
        context.mininetStarted = True
