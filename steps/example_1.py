
__author__ = 'Bene'

from behave   import *
from hamcrest import *
from mininet.net import *
from mininet.topo import *
from mininet.node import *
from mininet.link import *
from mininet.cli import *
from helper import NamedNumber

# This version of the code is working with Topo objects

@given('a single switch {sw1}')
def step_impl(context, sw1):
    assert sw1 is not None
    #add switches to topology
    #context.testTopo.addSwitch(sw1)
    context.mini.addSwitch(sw1)

@given('switch {sw1} and switch {sw2}')
def step_impl(context, sw1, sw2):
    #context.testTopo = Topo()
    assert sw1 is not None
    assert sw2 is not None
    #add switches to topology
    #context.testTopo.addSwitch(sw1)
    #context.testTopo.addSwitch(sw2)
    context.mini.addSwitch(sw1)
    context.mini.addSwitch(sw2)

@given('switches {sw1} and {sw2} and {sw3}')
def step_impl(context, sw1, sw2, sw3):
    assert sw1 is not None
    assert sw2 is not None
    assert sw3 is not None
    #add switches to topology
    for switch in [sw1,sw2,sw3]:
        #context.testTopo.addSwitch(switch)
        context.mini.addSwitch(switch)

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
        #context.testTopo.addSwitch(switchName)
        context.mini.addSwitch(switchName)

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
        #context.testTopo.addHost(hostName)
        context.mini.addHost(hostName)


#########################################################
#               WHEN Part

@when('we connect all switches with each other')
def step_connect_all(context):
    assert context is not None
    #get list of switches
    listOfSwitches = context.mini.switches
    listLength = len(listOfSwitches)
    assert_that(less_than(listLength), 1, "More than one host existing")
    for i in range(0, listLength-1):
        switch1 = str(listOfSwitches[i])
        for j in range(i+1, listLength):
            switch2 = str(listOfSwitches[j])
            context.mini.addLink(switch1, switch2)

@when('we connect switch {sw1} to switch {sw2}')
def step_connect(context, sw1, sw2):
    #validation (switches existing?
    for switch in [sw1, sw2]:
        assert switch is not None
        assert_that(context.mini.__contains__(switch), equal_to(True), "switch %s exists" % switch)
    #s1 = context.mini.getNodeByName(sw1)
    #s2 = context.mini.getNodeByName(sw2)
    #assert_that(s1 in context.mini.switches and s2 in context.mini.switches, equal_to(True))
    #connect the switches
    #context.testTopo.addLink(sw1, sw2)
    context.mini.addLink(sw1, sw2)

@when('we connect host {host} to switch {switch}')
def step_connectHosts(context, host, switch):
    assert host is not None
    assert switch is not None
    assert_that(context.mini.__contains__(switch), equal_to(True),"switch %s exists" % switch)
    assert_that(context.mini.__contains__(host), equal_to(True),"host %s exists" % host)
    #assert_that(host in context.mini.hosts, equal_to(True), "Host %s exists" % host)
    #assert_that(switch in context.mini.switches, equal_to(True), "Switch %s exists" % switch)
    #connect host to switch
    #context.testTopo.addLink(str(host), str(switch))
    context.mini.addLink(host, switch)


@when('we start a webserver on host {host}')
def step_startWebserver(context, host):
    assert host is not None
    assert_that(context.mini.__contains__(host), equal_to(True),"host %s exists" % host)
    cmdString = "python -m SimpleHTTPServer 80 >& /tmp/http.log &"
    context.mini.getNodeByName(host).cmd(cmdString)

@when('the link between {nd1} and {nd2} is going down')
def step_linkDown(context, nd1, nd2):
    for node in [nd1, nd2]:
        assert node is not None
        assert_that(context.mini.__contains__(node), equal_to(True),"node %s exists" % node)
    node1 = context.mini.getNodeByName(nd1)
    node2 = context.mini.getNodeByName(nd2)
    #check if link between nodes is existing
    connectionList = node1.connectionsTo(node2)
    assert_that(len(connectionList), greater_than(0), "Link between %s and %s found" % (nd1,nd2))
    #find the correct link and stop it => link status will be set to "MISSING"
    for link in context.mini.links:
        if((str(node1.name + "-") in str(link.intf1) and str(node2.name + "-") in str(link.intf2)) or
               (str(node1.name + "-") in str(link.intf2) and str(node2.name + "-") in str(link.intf1))):
            link.stop()

# @when('the link between {nd1} and {nd2} is going up')
# def step_linkUp(context, nd1, nd2):
#     for node in [nd1, nd2]:
#         assert node is not None
#         assert_that(context.mini.__contains__(node), equal_to(True), "node %s exists" % node)
#     node1 = context.mini.getNodeByName(nd1)
#     node2 = context.mini.getNodeByName(nd2)
#     for link in context.mini.links:
#         if((str(node1.name + "-") in str(link.intf1) and str(node2.name + "-") in str(link.intf2)) or
#                (str(node1.name + "-") in str(link.intf2) and str(node2.name + "-") in str(link.intf1))):
#             link.makeIntfPair(nd1, nd2)


#######################################################
#                   THEN Part

@then('switch {sw1} and switch {sw2} will share a link')
def step_test_connection(context, sw1, sw2):
    for switch in [sw1, sw1]:
        assert switch is not None
        assert_that(context.mini.__contains__(switch), equal_to(True), "Switch %s exists" % switch)
    s1 = context.mini.getNodeByName(sw1)
    s2 = context.mini.getNodeByName(sw2)
    connectionList = s1.connectionsTo(s2)
    assert_that(len(connectionList), greater_than(0), "Link %s <-> %s found" % (sw1,sw2))

@then('switch {sw1} and switch {sw2} will not share a link')
def step_test_connection(context, sw1, sw2):
    for switch in [sw1, sw2]:
        assert switch is not None
        assert_that(context.mini.__contains__(switch), equal_to(True),"Switch %s exists" % switch)
    s1 = context.mini.getNodeByName(sw1)
    s2 = context.mini.getNodeByName(sw2)

    connectionList = s1.connectionsTo(s2)
    # at least one link is existing -> check all links
    if(len(context.mini.links) > 0):
        for link in context.mini.links:
            #check if link between nodes is existing, if so check status
            if(str(sw1 + "-") in link.__str__() and str(sw2 + "-") in link.__str__()):
                #link is existing and status must be (MISSING MISSING)
                print(link)
                assert_that(link.status(), equal_to("(MISSING MISSING)"), "Link %s <-> %s found with status %s" % (sw1,sw2,link.status()))
            else:
                #link between nodes is not existing
                assert_that(str(sw1 + "-") in link.__str__() and str(sw2 + "-") in link.__str__(), equal_to(False))
    else:
        #no links at all
        assert_that(len(connectionList), equal_to(0))

@then('host {hst1} is able to ping host {hst2}')
def step_test_ping(context, hst1, hst2):
    #context.mini.start()
    for host in [hst1, hst2]:
        assert host is not None
        assert_that(context.mini.__contains__(host), equal_to(True),"host %s exists" % host)
    h1 = context.mini.getNodeByName(hst1)
    h2 = context.mini.getNodeByName(hst2)
    timeout = "5"
    packetLoss = context.mini.ping((h1,h2), timeout)
    assert_that(packetLoss, close_to(0,5),"Packet loss in percent is %s " % packetLoss)

@then('host {hst1} is not able to ping host {hst2}')
def step_test_ping(context, hst1, hst2):
    #context.mini.start()
    for host in [hst1, hst2]:
        assert host is not None
        assert_that(context.mini.__contains__(host), equal_to(True),"host %s exists" % host)
    h1 = context.mini.getNodeByName(hst1)
    h2 = context.mini.getNodeByName(hst2)
    timeout = "5"
    packetLoss = context.mini.ping((h1,h2), timeout)
    assert_that(packetLoss, equal_to(100), "Packet loss in percent is %s " % packetLoss)

@then('host {host1} is able to send a HTTP request to host {host2}')
def step_httpRequest(context, host1, host2):
    for host in [host1, host2]:
        assert host is not None
        assert_that(context.mini.__contains__(host), equal_to(True),"host %s exists" % host)
    h1 = context.mini.getNodeByName(host1)
    h2 = context.mini.getNodeByName(host2)
    cmdString = "wget -O - %s" % h2.IP()
    responseArray = h1.pexec(cmdString)
    response = responseArray[2]
    assert_that(response, equal_to(0),"ExitCode is %s " % response)
    #solution with http request pattern matching
    #context.response = h1.cmd(cmdString)
    #assert_that(context.response, contains_string("HTTP request sent, awaiting response... 200 OK"), "%s" % context.response)