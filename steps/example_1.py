
__author__ = 'Bene'

from behave   import *
from hamcrest import *
from mininet.net import *
from mininet.topo import *
from mininet.node import *
from mininet.link import *
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

# @when('the link between {node1} and {node2} is going down')
# def step_linkDown(context, node1, node2):
#     for node in [node1, node2]:
#         assert node is not None
#         assert_that((node in context.testTopo.hosts()) or (node in context.testTopo.switches()),equal_to(True), 'node %s exists' %node)

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
        assert_that(context.mini.__contains__(switch), equal_to(True), "Switch %s exists" % switch)
    s1 = context.mini.getNodeByName(sw1)
    s2 = context.mini.getNodeByName(sw2)
    connectionList = s1.connectionsTo(s2)
    assert_that(len(connectionList), greater_than(0), "Link %s <-> %s found" % (sw1,sw2))

    #assert_that(s1 in context.mini.switches and s2 in context.mini.switches, equal_to(True))
    #linkToFind = (str(sw1) + "-", str(sw2) + "-")
    # matcher1 = str(sw1) + "-"
    # matcher2 = str(sw2) + "-"
    # for link in context.mini.links:
    #     linkString = str(link.__str__())
    #     if(matcher1 in linkString and matcher2 in linkString):
    #         assert_that(matcher1 in linkString and matcher2 in linkString, equal_to(True), "Link %s <-> %s found" % (sw1,sw2))
    #
    # #in case there is no link this will make the test fail
    # for link in context.mini.links:
    #     linkString = link.__str__()
    #     assert_that(matcher1 in linkString and matcher2 in linkString, equal_to(True), "Link %s <-> %s found" % (sw1,sw2))
    # linkToFind = (sw1, sw2)
    # assert_that(linkToFind in context.testTopo.links(), equal_to(True), "Link %s exists" % str(linkToFind))

@then('switch {sw1} and switch {sw2} will not share a link')
def step_test_connection(context, sw1, sw2):
    for switch in [sw1, sw2]:
        assert switch is not None
        assert_that(context.mini.__contains__(switch), equal_to(True),"Switch %s exists" % switch)
    s1 = context.mini.getNodeByName(sw1)
    s2 = context.mini.getNodeByName(sw2)
    connectionList = s1.connectionsTo(s2)
    assert_that(len(connectionList), equal_to(0), "Link %s <-> %s found" % (sw1,sw2))

@then('host {hst1} is able to ping host {hst2}')
def step_test_ping(context, hst1, hst2):
    context.mini.start()
    for host in [hst1, hst2]:
        assert host is not None
        assert_that(context.mini.__contains__(host), equal_to(True),"host %s exists" % host)
    #context.mininet.buildFromTopo(topo=context.testTopo)
    #add new remote Controller to mininet object
    #onosController = RemoteController('c1', ip='192.168.59.103', port=6633)
    #context.mini.addController( onosController )
    # context.mini.build()
    # context.mini.start()
    # context.mini.waitConnected()
    # context.mini.waitConnected()
    h1 = context.mini.getNodeByName(hst1)
    h2 = context.mini.getNodeByName(hst2)
    print(h1.IP())
    print(h2.IP())
    timeout = "5"
    packetLoss = context.mini.ping((h1,h2), timeout)
    assert_that(packetLoss, close_to(0,5))

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
    assert_that(context.response, equal_to(0),"ExitCode is %s " % response)
    #solution with http request pattern matching
    #context.response = h1.cmd(cmdString)
    #assert_that(context.response, contains_string("HTTP request sent, awaiting response... 200 OK"), "%s" % context.response)