__author__ = 'Bene'

from mininet.topo import *
from mininet.net import *
from mininet.node import OVSController, RemoteController
from mininet.link import *
from mininet.clean import *
from mininet import net
from mininet.clean import Cleanup
import logging

#logging.basicConfig(filename='example.log',level=logging.DEBUG)

def before_scenario(context,scenario):
    context.mininetStarted = False
    #create testTopo
    context.testTopo = Topo()
    #create mininet instance with testTopo
    #context.mini = Mininet(topo=context.testTopo, controller=OVSController, cleanup=True)
    onosController= RemoteController('c0', ip='192.168.59.103', port=6633)
    context.mini = Mininet(topo=context.testTopo, controller=onosController, cleanup=True, ipBase='10.0.0.0/8', waitConnected=True)
    #context.mini.addController(name='c0', ip='192.168.59.103', port=6634)

# def before_step(context, step):
#     #start mininet when first "then" step is executed
#     if(step.step_type == "then"):
#         if not context.mininetStarted:
#             context.mini.start()
#             context.mininetStarted = True
#     #logging.warning("before_step ///" + step.name + "\\\\, type ///" + step.step_type)

def after_scenario(context,scenario):
    # print("ExitCode:")
    # print(context.response)
    print("Output for debugging purposes:")
    print("List of Controllers: ")
    print(context.mini.controllers)
    print("List of Switches: ")
    # print(context.testTopo.switches(sort=True))
    print(context.mini.switches)
    print("List of Hosts: ")
    # print(context.testTopo.hosts(sort=True))
    print(context.mini.hosts)
    print("List of Links: ")
    # print(context.testTopo.links(sort=True))
    # print(context.mini.topo.links(sort=True))
    print(context.mini.links)

    Cleanup.cleanup()
