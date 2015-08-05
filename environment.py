__author__ = 'Bene'

from mininet.topo import *
from mininet.net import *
from mininet.node import OVSController, RemoteController
from mininet.link import *
from mininet.clean import *
from mininet import net
from mininet.clean import Cleanup

def before_scenario(context,scenario):
    #create testTopo
    context.testTopo = Topo()
    #create mininet instance with testTopo
    #context.mini = Mininet(topo=context.testTopo, controller=OVSController, cleanup=True)
    onosController= RemoteController('c0', ip='192.168.59.103', port=6633)
    context.mini = Mininet(topo=context.testTopo, controller=onosController, cleanup=True)
    #context.mini.addController(name='c0', ip='192.168.59.103', port=6634)

def after_scenario(context,scenario):
    # print("ExitCode:")
    # print(context.response)
    # print("Output for debugging purposes:")
    # print("List of Controllers: ")
    # print(context.mini.controllers)
    # print("List of Switches: ")
    # print(context.testTopo.switches(sort=True))
    # print(context.mini.switches)
    # print("List of Hosts: ")
    # print(context.testTopo.hosts(sort=True))
    # print(context.mini.hosts)
    # print("List of Links: ")
    # print(context.testTopo.links(sort=True))
    #print(context.mini.topo.links(sort=True))
    #print(context.mini.links)

    Cleanup.cleanup()
