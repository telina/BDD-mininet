
__author__ = 'Bene'

from behave   import *
from hamcrest import *
from mininet.net import *
from mininet.topo import *
from mininet.node import *
from mininet.link import *
from mininet.cli import *
from helper import NumberConverter, MininetHelper
from FlowEntrys import FlowTable
from environment import *


@given('a single switch')
def step_impl(context):
    #add switches to topology
    nextSwitch = len(context.mini.switches)+1
    switch  = "s" + str(nextSwitch)
    context.mini.addSwitch(switch)

@given("a set of {number} switches")
def step_addSwitches(context, number):
    numberOfSwitches = NumberConverter.convertNumber(number)
    MininetHelper.addSwitches(context.mini, numberOfSwitches)

@given("a set of {number} hosts")
def step_addHost(context, number):
    numberOfHosts = NumberConverter.convertNumber(number)
    MininetHelper.addHosts(context.mini, numberOfHosts)


@given('we connect all switches with each other')
def step_fullMeshedNet(context):
    MininetHelper.createFullMeshedNet(context.mini)


@given('we connect switch {sw1} to switch {sw2}')
def step_connect(context, sw1, sw2):
    #validation (switches existing?)
    if MininetHelper.validateNodes(context.mini, (sw1,sw2)):
        context.mini.addLink(sw1,sw2)

@given('we connect host {hst} to switch {sw}')
def step_connectHosts(context, hst, sw):
    if MininetHelper.validateNodes(context.mini, (hst,sw)):
        context.mini.addLink(hst,sw)

#########################################################
#               WHEN Part

@when('host {hst1} pings host {hst2}')
def step_ping(context, hst1, hst2):
    h1 = MininetHelper.getNodeFromName(context.mini, hst1)
    h2 = MininetHelper.getNodeFromName(context.mini, hst2)
    #build and start mininet
    buildAndStart(context)
    timeout = "5"
    packetLoss = context.mini.ping((h1,h2), timeout)
    context.pingResult = packetLoss


@when('we start a webserver on host {hst}')
def step_startWebserver(context, hst):
    serverNode = MininetHelper.getNodeFromName(context.mini, hst)
    #start Webserver
    cmdString = "python -m SimpleHTTPServer 80 >& /tmp/http.log &"
    serverNode.cmd(cmdString)
    #build and start mininet
    buildAndStart(context)

@when('the link between {nd1} and {nd2} is going down')
def step_linkDown(context, nd1, nd2):
    node1 = MininetHelper.getNodeFromName(context.mini, nd1)
    node2 = MininetHelper.getNodeFromName(context.mini, nd2)
    #build an start mininet
    buildAndStart(context)
    #check if link between nodes is existing
    connectionList = node1.connectionsTo(node2)
    assert_that(len(connectionList), greater_than(0), "Link between %s and %s found" % (nd1,nd2))
    #find the correct link and stop it => link status will be set to "MISSING"
    for link in context.mini.links:
        if((str(node1.name + "-") in str(link.intf1) and str(node2.name + "-") in str(link.intf2)) or
               (str(node1.name + "-") in str(link.intf2) and str(node2.name + "-") in str(link.intf1))):
            link.stop()

@when('we send a HTTP request from host {hst1} to host {hst2}')
def step_httpRequest(context, hst1, hst2):
    h1 = MininetHelper.getNodeFromName(context.mini, hst1)
    h2 = MininetHelper.getNodeFromName(context.mini, hst2)
    #build an start mininet
    buildAndStart(context)
    #send request
    cmdString = "wget -O - %s" % h2.IP()
    responseArray = h1.pexec(cmdString)
    #write response (Exitcode) in context variable
    response = responseArray[2]
    context.httpRequestExitcode = response


#######################################################
#                   THEN Part

@then('switch {sw1} and switch {sw2} will share a link')
def step_test_connection(context, sw1, sw2):
    s1 = MininetHelper.getNodeFromName(context.mini, sw1)
    s2 = MininetHelper.getNodeFromName(context.mini, sw2)
    #build an start mininet
    buildAndStart(context)
    connectionList = s1.connectionsTo(s2)
    assert_that(len(connectionList), greater_than(0), "Link %s <-> %s found" % (sw1,sw2))

@then('switch {sw1} and switch {sw2} will not share a link')
def step_test_connection(context, sw1, sw2):
    s1 = MininetHelper.getNodeFromName(context.mini, sw1)
    s2 = MininetHelper.getNodeFromName(context.mini, sw2)
    #build an start mininet
    buildAndStart(context)
    connectionList = s1.connectionsTo(s2)
    # at least one link is existing -> check all links
    if(len(context.mini.links) > 0):
        for link in context.mini.links:
            #check if link between nodes is existing, if so check status
            if(str(sw1 + "-") in link.__str__() and str(sw2 + "-") in link.__str__()):
                #link is existing and status must be (MISSING MISSING)
                #print(link)
                assert_that(link.status(), equal_to("(MISSING MISSING)"), "Link %s <-> %s found with status %s" % (sw1,sw2,link.status()))
            else:
                #link between nodes is not existing
                assert_that(str(sw1 + "-") in link.__str__() and str(sw2 + "-") in link.__str__(), equal_to(False))
    else:
        #no links at all
        assert_that(len(connectionList), equal_to(0))


@then('the ping succeeds')
def step_pingSucceed(context):
    if context.pingResult == 0.0 :
        ping = True
    else:
        ping = False
    assert_that(ping, equal_to(True), "Ping succeeds")

@then('the ping fails')
def step_pingFailure(context):
    if context.pingResult > 0.0 :
        ping = False
    else:
        ping = True
    assert_that(ping, equal_to(False), "Ping fails")

@then('the request succeeds')
def step_httpRequestSucceed(context):
    if context.httpRequestExitcode == 0 :
        request = True
    else:
        request = False
    assert_that(request, equal_to(True), "HTTP Request was successful")

@then('the ping traffic from host {hst1} to host {hst2} takes the route across switch {sw}')
def step_routeIdentification(context, hst1, hst2, sw):
    s1 = MininetHelper.getNodeFromName(context.mini, sw)
    h1 = MininetHelper.getNodeFromName(context.mini, hst1)
    h2 = MininetHelper.getNodeFromName(context.mini, hst2)
    #build an start mininet
    buildAndStart(context)
    #build flow table
    s1FlowTable = MininetHelper.createFlowTable(s1)
    #check if forwarding entry exists
    hasEntry = s1FlowTable.hasForwardingEntry(h1.MAC(), h2.MAC())
    assert_that(hasEntry, equal_to(True), "switch %s has forwarding entry for ping traffic" % sw)


@then('the http traffic from host {hst1} to host {hst2} takes the route across switch {sw}')
def step_routeIdentification(context, hst1, hst2, sw):
    s1 = MininetHelper.getNodeFromName(context.mini, sw)
    h1 = MininetHelper.getNodeFromName(context.mini, hst1)
    h2 = MininetHelper.getNodeFromName(context.mini, hst2)
    #build an start mininet
    buildAndStart(context)
    #buil FlowTable
    s1FlowTable = MininetHelper.createFlowTable(s1)
    hasEntry = s1FlowTable.hasForwardingEntry(h1.MAC(), h2.MAC())
    assert_that(hasEntry, equal_to(True), "switch %s has dl_dst entry for traffic" % sw)







''' Deprecated or not in use

# @given('a single switch {sw1}')
# def step_impl(context, sw1):
#     assert sw1 is not None
#     #add switches to topology
#     #context.testTopo.addSwitch(sw1)
#     context.mini.addSwitch(sw1)

# @given('switch {sw1} and switch {sw2}')
# def step_impl(context, sw1, sw2):
#     #context.testTopo = Topo()
#     assert sw1 is not None
#     assert sw2 is not None
#     #add switches to topology
#     #context.testTopo.addSwitch(sw1)
#     #context.testTopo.addSwitch(sw2)
#     context.mini.addSwitch(sw1)
#     context.mini.addSwitch(sw2)
#
# @given('switches {sw1} and {sw2} and {sw3}')
# def step_impl(context, sw1, sw2, sw3):
#     assert sw1 is not None
#     assert sw2 is not None
#     assert sw3 is not None
#     #add switches to topology
#     for switch in [sw1,sw2,sw3]:
#         #context.testTopo.addSwitch(switch)
#         context.mini.addSwitch(switch)

# @given('we connect switch {sw1} to switch {sw2}')
# def step_connect(context, sw1, sw2):
#     #validation (switches existing?)
#     for switch in [sw1, sw2]:
#         assert switch is not None
#         assert_that(context.mini.__contains__(switch), equal_to(True), "switch %s exists" % switch)
#     #s1 = context.mini.getNodeByName(sw1)
#     #s2 = context.mini.getNodeByName(sw2)
#     #assert_that(s1 in context.mini.switches and s2 in context.mini.switches, equal_to(True))
#     #connect the switches
#     #context.testTopo.addLink(sw1, sw2)
#     context.mini.addLink(sw1, sw2)

# @given('we connect host {host} to switch {switch}')
# def step_connectHosts(context, host, switch):
#     assert host is not None
#     assert switch is not None
#     assert_that(context.mini.__contains__(switch), equal_to(True),"switch %s exists" % switch)
#     assert_that(context.mini.__contains__(host), equal_to(True),"host %s exists" % host)
#     #assert_that(host in context.mini.hosts, equal_to(True), "Host %s exists" % host)
#     #assert_that(switch in context.mini.switches, equal_to(True), "Switch %s exists" % switch)
#     #connect host to switch
#     #context.testTopo.addLink(str(host), str(switch))
#     context.mini.addLink(host, switch)

# @given("a set of {number} switches")
# def step_addSwitches(context, number):
#     numberOfSwitches = NumberConverter.convertNumber(number)
#     for i in range (1,numberOfSwitches+1):
#         switchName = "s" + str(i)
#         #context.testTopo.addSwitch(switchName)
#         context.mini.addSwitch(switchName)

# @given("a set of {number} hosts")
# def step_addHost(context, number):
#     numberOfHosts = NumberConverter.convertNumber(number)
#     for i in range (1, numberOfHosts+1):
#         hostName = "h" + str(i)
#         context.mini.addHost(hostName)

# @given('we connect all switches with each other')
# def step_fullMeshedNet(context):
#     #get list of switches
#     listOfSwitches = context.mini.switches
#     listLength = len(listOfSwitches)
#     assert_that(less_than(listLength), 1, "More than one host existing")
#     for i in range(0, listLength-1):
#         switch1 = str(listOfSwitches[i])
#         for j in range(i+1, listLength):
#             switch2 = str(listOfSwitches[j])
#             context.mini.addLink(switch1, switch2)

# @when('we start a webserver on host {host}')
# def step_startWebserver(context, host):
#     assert host is not None
#     assert_that(context.mini.__contains__(host), equal_to(True),"host %s exists" % host)
#     cmdString = "python -m SimpleHTTPServer 80 >& /tmp/http.log &"
#     context.mini.getNodeByName(host).cmd(cmdString)
#     #call function to build and start mininet
#     #buildAndStart(context)

# @when('the link between {nd1} and {nd2} is going down')
# def step_linkDown(context, nd1, nd2):
#     for node in [nd1, nd2]:
#         assert node is not None
#         assert_that(context.mini.__contains__(node), equal_to(True),"node %s exists" % node)
#     #buildAndStart(context)
#     node1 = context.mini.getNodeByName(nd1)
#     node2 = context.mini.getNodeByName(nd2)
#     #check if link between nodes is existing
#     connectionList = node1.connectionsTo(node2)
#     assert_that(len(connectionList), greater_than(0), "Link between %s and %s found" % (nd1,nd2))
#     #find the correct link and stop it => link status will be set to "MISSING"
#     for link in context.mini.links:
#         if((str(node1.name + "-") in str(link.intf1) and str(node2.name + "-") in str(link.intf2)) or
#                (str(node1.name + "-") in str(link.intf2) and str(node2.name + "-") in str(link.intf1))):
#             link.stop()

# @when('we send a HTTP request from host {hst1} to host {hst2}')
# def step_httpRequest(context, hst1, hst2):
#     for host in [hst1, hst2]:
#         assert host is not None
#         assert_that(context.mini.__contains__(host), equal_to(True),"host %s exists" % host)
#     h1 = context.mini.getNodeByName(hst1)
#     h2 = context.mini.getNodeByName(hst2)
#     cmdString = "wget -O - %s" % h2.IP()
#     responseArray = h1.pexec(cmdString)
#     response = responseArray[2]
#     context.httpRequestExitcode = response
#     print(responseArray)
#     #assert_that(response, equal_to(0),"ExitCode is %s " % response)
#     #solution with http request pattern matching
#     #context.response = h1.cmd(cmdString)
#     #assert_that(context.response, contains_string("HTTP request sent, awaiting response... 200 OK"), "%s" % context.response)


# @then('host {hst1} is able to ping host {hst2}')
# def step_test_ping(context, hst1, hst2):
#     for host in [hst1, hst2]:
#         assert host is not None
#         assert_that(context.mini.__contains__(host), equal_to(True),"host %s exists" % host)
#     h1 = context.mini.getNodeByName(hst1)
#     h2 = context.mini.getNodeByName(hst2)
#     timeout = "5"
#     packetLoss = context.mini.ping((h1,h2), timeout)
#     assert_that(packetLoss, close_to(0,5),"Packet loss in percent is %s " % packetLoss)

# @then('host {hst1} is not able to ping host {hst2}')
# def step_test_ping(context, hst1, hst2):
#     #context.mini.start()
#     for host in [hst1, hst2]:
#         assert host is not None
#         assert_that(context.mini.__contains__(host), equal_to(True),"host %s exists" % host)
#     h1 = context.mini.getNodeByName(hst1)
#     h2 = context.mini.getNodeByName(hst2)
#     timeout = "5"
#     packetLoss = context.mini.ping((h1,h2), timeout)
#     assert_that(packetLoss, equal_to(100), "Packet loss in percent is %s " % packetLoss)

@then('switch {sw1} and switch {sw2} will share a link')
# def step_test_connection(context, sw1, sw2):
#     for switch in [sw1, sw1]:
#         assert switch is not None
#         assert_that(context.mini.__contains__(switch), equal_to(True), "Switch %s exists" % switch)
#     s1 = context.mini.getNodeByName(sw1)
#     s2 = context.mini.getNodeByName(sw2)
#     connectionList = s1.connectionsTo(s2)
#     assert_that(len(connectionList), greater_than(0), "Link %s <-> %s found" % (sw1,sw2))

@then('switch {sw1} and switch {sw2} will not share a link')
# def step_test_connection(context, sw1, sw2):
#     for switch in [sw1, sw2]:
#         assert switch is not None
#         assert_that(context.mini.__contains__(switch), equal_to(True),"Switch %s exists" % switch)
#     s1 = context.mini.getNodeByName(sw1)
#     s2 = context.mini.getNodeByName(sw2)
#     connectionList = s1.connectionsTo(s2)
#     # at least one link is existing -> check all links
#     if(len(context.mini.links) > 0):
#         for link in context.mini.links:
#             #check if link between nodes is existing, if so check status
#             if(str(sw1 + "-") in link.__str__() and str(sw2 + "-") in link.__str__()):
#                 #link is existing and status must be (MISSING MISSING)
#                 print(link)
#                 assert_that(link.status(), equal_to("(MISSING MISSING)"), "Link %s <-> %s found with status %s" % (sw1,sw2,link.status()))
#             else:
#                 #link between nodes is not existing
#                 assert_that(str(sw1 + "-") in link.__str__() and str(sw2 + "-") in link.__str__(), equal_to(False))
#     else:
#         #no links at all
#         assert_that(len(connectionList), equal_to(0))

# @then('host {host1} is able to send a HTTP request to host {host2}')
# def step_httpRequest(context, host1, host2):
#     for host in [host1, host2]:
#         assert host is not None
#         assert_that(context.mini.__contains__(host), equal_to(True),"host %s exists" % host)
#     h1 = context.mini.getNodeByName(host1)
#     h2 = context.mini.getNodeByName(host2)
#     cmdString = "wget -O - %s" % h2.IP()
#     responseArray = h1.pexec(cmdString)
#     response = responseArray[2]
#     assert_that(response, equal_to(0),"ExitCode is %s " % response)
#     #solution with http request pattern matching
#     #context.response = h1.cmd(cmdString)
#     #assert_that(context.response, contains_string("HTTP request sent, awaiting response... 200 OK"), "%s" % context.response)

# @then('the ping traffic from host {host1} to host {host2} takes the route across switch {switch1}')
# def step_routeIdentification(context, switch1, host1, host2):
#     for node in [switch1, host1, host2]:
#         assert node is not None
#         assert_that(context.mini.__contains__(node), equal_to(True),"node %s exists" % node)
#     buildAndStart(context)
#     s1 = context.mini.getNodeByName(switch1)
#     h1 = context.mini.getNodeByName(host1)
#     h2 = context.mini.getNodeByName(host2)
#     #print(s1.dpctl("add-flow priority=40000,in_port=1,dl_dst=00:00:00:00:00:02,actions=drop"))
#     context.mini.ping((h1,h2), 5)
#     response = s1.dpctl("dump-flows")
#     #create Flowtable for switch
#     s1FlowTable = FlowTable(switch1, response)
#     #check if switch has forwarding entry for MAC of host1
#     hasEntry = s1FlowTable.hasForwardingEntry(h2.MAC())
#     assert_that(hasEntry, equal_to(True), "switch %s has dl_dst entry for traffic" % switch1)
#     #s1FlowTable.printTable()
#     flowEntrySrcDst = "dl_src=%s,dl_dst=%s" %(h1.MAC(), h2.MAC())
#     #assert_that(response, equal_to("TEST"), "Response: %s" % response)

# @then('the http traffic from host {host1} to host {host2} takes the route across switch {switch1}')
# def step_routeIdentification(context, switch1, host1, host2):
#     for node in [switch1, host1, host2]:
#         assert node is not None
#         assert_that(context.mini.__contains__(node), equal_to(True),"node %s exists" % node)
#     s1 = context.mini.getNodeByName(switch1)
#     h1 = context.mini.getNodeByName(host1)
#     h2 = context.mini.getNodeByName(host2)
#     #send http request
#     cmdString = "wget -O - %s:8080" % h2.IP()
#     h1.pexec(cmdString)
#     print(cmdString)
#     response = s1.dpctl("dump-flows")
#     #create Flowtable for switch
#     s1FlowTable = FlowTable(switch1, response)
#     #check if switch has forwarding entry for hosts MAC
#     hasEntry = s1FlowTable.hasForwardingEntry(h2.MAC())
#     assert_that(hasEntry, equal_to(True), "switch %s has dl_dst entry for traffic" % switch1)
#     #assert_that(response, equal_to("TEST"), "Response: %s" % response)



# @when('we assign host {host} on switch {switch} to VLAN {vlan}')
# def step_assignVlan(context, host, switch, vlan):
#     assert host is not None
#     assert_that(context.mini.__contains__(host), equal_to(True), "host %s exists" % host)
#     assert_that(context.mini.__contains__("h2"), equal_to(True), "host %s exists" % host)
#     assert switch is not None
#     assert_that(context.mini.__contains__(switch), equal_to(True), "switch %s exists" % switch)
#     assert vlan is not None
#     assert_that(vlan.isdigit(),equal_to(True), "VLAN-Number is number")
#     vlanNumber = int(vlan)
#     switch1 = context.mini.getNodeByName(switch)
#     host1 = context.mini.getNodeByName(host)
#     if not context.mininetStarted:
#         context.mini.build()
#         context.mini.start()
#         context.mininetStarted = True
#     list = switch1.connectionsTo(host1)
#     for intf in list:
#         if(switch1.name in str(intf)):
#             for index in range(0, len(intf)):
#                 if(str(switch1.name + "-") in str(intf[index])):
#                     port = intf[index]
#     #set port s1-eth1 tag=20 vlan_mode=access
#     # command = "set port %s tag=%s vlan_mode=access" % (port, vlanNumber)
#     # print(command)
#     # bridge = "br%s" % vlanNumber
#     # switch1.vsctl("add-br %s" % bridge)
#     # switch1.vsctl("add-port %s eth2" % bridge)
#     # switch1.vsctl("add-br brFake%s %s %s" % (vlanNumber, bridge, vlanNumber))
#     # #switch1.vsctl("add-port br0 eth2 tag=666")
#     # print(switch1.vsctl("list-ports br0"))
#     #print(switch1.vsctl("show"))
#     #print(switch1.dpctl("add-flow in_port=4,actions=drop"))
#     #print(switch1.dpctl(""))
#     #switch1.dpctl(command)
#     response = switch1.dpctl("dump-flows")
#     print(response)

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
#             link.makeIntfPair(nd1, nd2)v

'''










