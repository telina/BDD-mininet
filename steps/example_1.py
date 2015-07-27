
__author__ = 'Bene'

from behave   import *
from hamcrest import assert_that, equal_to, less_than, close_to
from mininet.net import *
from mininet.topo import *
from mininet.node import RemoteController
from mininet.link import *
from helper import NamedNumber

# This version of the code is working with Topo objects

@given('a single switch {sw1}')
def step_impl(context, sw1):
    assert sw1 is not None
    #add switches to topology with addSwitch(name)
    context.testTopo.addSwitch(sw1)

@given('switch {sw1} and switch {sw2}')
def step_impl(context, sw1, sw2):
    #context.testTopo = Topo()
    assert sw1 is not None
    assert sw2 is not None
    #add switches to topology with addSwitch(name)
    context.testTopo.addSwitch(sw1)
    context.testTopo.addSwitch(sw2)

@given('switches {sw1} and {sw2} and {sw3}')
def step_impl(context, sw1, sw2, sw3):
    assert sw1 is not None
    assert sw2 is not None
    assert sw3 is not None
    #add switches to topology with addSwitch(name)
    for switch in [sw1,sw2,sw3]:
        context.testTopo.addSwitch(switch)

@given("a set of {number} switches")
def step_numberSwitches(context, number):
    assert number is not None
    #cast number to int
    if number.isdigit():
        numberOfSwitches = int(number)
    else:
        numberOfSwitches = NamedNumber.from_string(number)
    assert_that(numberOfSwitches, less_than(10), "Less than 10 switches existing")
    #add switches to topology
    for i in range (1,numberOfSwitches+1):
        switchName = "s" + str(i)
        context.testTopo.addSwitch(switchName)

@given("a set of {number} hosts")
def step_addHost(context, number):
    assert number is not None
    if number.isdigit():
        numberOfHosts = int(number)
    else:
        numberOfHosts = NamedNumber.from_string(number)
    assert_that(numberOfHosts, less_than(10), "Less than 10 hosts existing")
    for i in range (1, numberOfHosts+1):
        hostName = "h" + str(i)
        context.testTopo.addHost(hostName)


#########################################################
#               WHEN Part

@when('we connect all switches with each other')
def step_connect_all(context):
    assert context is not None
    #get list of switches
    listOfSwitches = context.testTopo.switches()
    listLength = len(listOfSwitches)
    assert_that(less_than(listLength), 1, "More than one host existing")
    for i in range(0, listLength-1):
        switch1 = str(listOfSwitches[i])
        for j in range(i+1, listLength):
            switch2 = str(listOfSwitches[j])
            context.testTopo.addLink(switch1, switch2)
            #context.mini.addLink(switch1,switch2)

@when('we connect switch {sw1} to switch {sw2}')
def step_connect(context, sw1, sw2):
        #validation (switches existing?)
    for switch in [sw1, sw2]:
        assert switch is not None
        assert_that(switch in context.testTopo.switches(), equal_to(True), "Host %s exists" % switch)
    #connect the switches
    #context.testTopo.addLink(sw1, sw2)
    #s1 = context.mini.__getitem__(sw1)
    #s2 = context.mini.__getitem__(sw2)
    context.testTopo.addLink(sw1, sw2)
    #context.mini.addLink(s1, s2)

@when('we connect host {host} to switch {switch}')
def step_connectHosts(context, host, switch):
    assert host is not None
    assert switch is not None
    assert_that(host in context.testTopo.hosts(), equal_to(True), "Host %s exists" % host)
    assert_that(switch in context.testTopo.switches(), equal_to(True), "Switch %s exists" % switch)
    #connect host to switch
    context.testTopo.addLink(str(host), str(switch))

# @when('the link between {node1} and {node2} is going down')
# def step_linkDown(context, node1, node2):
#     for node in [node1, node2]:
#         assert node is not None
#         assert_that((node in context.testTopo.hosts()) or (node in context.testTopo.switches()),equal_to(True), 'node %s exists' %node)
#     #TODO

    #listOfLinks = context.testTopo.links()
    #linkToDelete = Link(node1, node2)
    #linkToDelete = (node1, node2)
    #assert_that(linkToDelete in context.testTopo.links(), equal_to(True))
    #listOfLinks.remove(linkToDelete)
    #context.testTopo.links = listOfLinks
    #context.mini.configLinkStatus(node1, node2, "down")

#######################################################
#                   THEN Part

@then('switch {sw1} and switch {sw2} will share a link')
def step_test_connection(context, sw1, sw2):
    for switch in [sw1, sw1]:
        assert switch is not None
        assert_that(switch in context.testTopo.switches(), equal_to(True), "Switch %s exists" % switch)
    linkToFind = (sw1, sw2)
    assert_that(linkToFind in context.testTopo.links(), equal_to(True), "Link %s exists" % str(linkToFind))

@then('switch {sw1} and switch {sw2} will not share a link')
def step_test_connection(context, sw1, sw2):
    for switch in [sw1, sw2]:
        assert switch is not None
        assert_that(switch in context.testTopo.switches(), equal_to(True), "Switch %s exists" % switch)
    linkToFind = (sw1, sw2)
    #assert_that(linkToFind in context.testTopo.links(), equal_to(False), "Link %s does not exist" % str(linkToFind))

@then('host {hst1} is able to ping host {hst2}')
def step_test_ping(context, hst1, hst2):
    for host in [hst1, hst2]:
        assert host is not None
        assert_that(host in context.testTopo.hosts(), equal_to(True), "Host %s exists" % host)
    #context.mininet.buildFromTopo(topo=context.testTopo)
    #add new remote Controller to mininet object
    #onosController = RemoteController('c1', ip='192.168.59.103', port=6633)
    #context.mini.addController( onosController )
    context.mini.build()
    context.mini.start()
    context.mini.waitConnected()
    context.mini.waitConnected()

    timeout = "5"
    packetLoss = context.mini.ping((context.mini.getNodeByName(hst1), context.mini.getNodeByName(hst2)), timeout)
    assert_that(packetLoss, close_to(0,5))

    #check if hosts are existing
    # if(context.hstA in context.testTopo.hosts() and context.hstB in context.testTopo.hosts()):
    #     #test ping
    #     timeout = "1"
    #     packetLoss = context.mini.ping((context.mini.getNodeByName(hstA), context.mini.getNodeByName(hstB)), timeout)
    #     print(packetLoss)
    #     assert_that(0, equal_to(packetLoss))




    #Garbage
    #if context.switch1.name == swX and context.switch2.name == swY:
     #   assert_that(True, equal_to(context.switch1.testLink(swY)))

    #if context.switch1 == switch.returnSwitch(sX) and context.switch2 == switch.returnSwitch(sY):
     #   assert_that(True, equal_to(context.switch1.testLink(sY)))