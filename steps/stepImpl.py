
__author__ = 'Bene'

from behave   import *
from hamcrest import *
from mininet.net import *
from mininet.topo import *
from mininet.node import *
from mininet.link import *
from helper import NumberConverter, MininetHelper, TerraformHelper
from environment import *
import itertools



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

@given('we start a webserver on host {hst}')
def step_startWebserver(context, hst):
    serverNode = MininetHelper.getNodeFromName(context.mini, hst)
    #start Webserver
    cmdString = "python -m SimpleHTTPServer 80 &"
    serverNode.cmd(cmdString)

@given('we enable IPv6 addressing')
def step_addIPv6Address(context):
    hosts = context.mini.hosts
    cnt = 1
    for host in hosts:
        host.cmd('ifconfig h{0}-eth0 inet6 add fc00:0000:0000:0000::{0}/16 '.format(str(cnt))) 
        cnt += 1

#########################################################
#               WHEN Part

@when('host {hst1} pings host {hst2}')
def step_ping(context, hst1, hst2):
    # OpenStack part
    if(context.openStackTest == True):
        '''
        validate nodes
        send ping
        return packetLoss (pingResult)
        '''
        context.tf.validateNodes((hst1,hst2))
        # set host to host intents (get names of hst1/hst2, add "_mac" to get terraform output)
        #ping once for ONOS host detection
        pingOnce = True
        context.tf.ping(hst1, hst2, pingOnce)
        hst1_mac =  context.tf.tf_get(context.tf.translateHostName(hst1) + "_mac")
        hst2_mac =  context.tf.tf_get(context.tf.translateHostName(hst2) + "_mac")
        context.onosRest.setOnosIntent(hst1_mac, hst2_mac)
        packetLoss = context.tf.ping(hst1, hst2, False)
    else:
        # Mininet part
        h1 = MininetHelper.getNodeFromName(context.mini, hst1)
        h2 = MininetHelper.getNodeFromName(context.mini, hst2)
        # if controller = ONOS set host intents
        if(context.onosFlag):
            context.onosRest.setOnosIntent(h1.MAC(h1.name + "-eth0"), h2.MAC(h2.name + "-eth0"))
        timeout = "5"
        packetLoss = 100
        pingCounter = 0
        pingMaxCount = 5
        while packetLoss > 0 and pingCounter < pingMaxCount:
            if(pingCounter > 0):
                #wait some time between two pings
                sleep(1)
            packetLoss = context.mini.ping((h1,h2), timeout)
            pingCounter += 1
    context.pingResult = packetLoss

# According to the error message, the same description is already used above
# @when('host {hst1} pings host {hst2} {x} times')
# def step_pingTimes(context, hst1, hst2, x):
#     h1 = MininetHelper.getNodeFromName(context.mini, hst1)
#     h2 = MininetHelper.getNodeFromName(context.mini, hst2)
#     timeout = "5"
#     packetloss = 0
#     times = int(x)
#     for _ in itertools.repeat(None, times):
#         packetloss += context.mini.ping((h1, h2), timeout)
#         sleep(0.50)
#         context.pingResult = (packetloss / times)

when('host {hst1} pings host {hst2} {x} times via IPv6')
def step_pingTimesIPv6(context, hst1, hst2, x):
    h1 = MininetHelper.getNodeFromName(context.mini, hst1)
    h2 = MininetHelper.getNodeFromName(context.mini, hst2)
    h2_address = h2.cmd("/sbin/ip -6 addr | grep inet6 | awk -F '[ \t]+|/' '{print $3}' | grep -E -v '^fe80*|^::1*'")
    times = int(x)
    packetloss = h1.cmd("ping6 -c {0} {1} | grep -oP '\d+(?=% packet loss)'".format(times, h2_address.rstrip()))
    try:
        context.pingResult = int(packetloss) / times
    except(ValueError):
        context.pingResult = 100 

@when('we ping all hosts via IPv6')
def step_pingAllHostsIPv6(context):
    hosts = context.mini.hosts
    if (hosts): # A trial with no hosts would result in dividing by zero
        addresses = []
        packetloss = 0            
        for host in hosts:
            # gets the ipv6 address. Excludes linklocal and host address
            addresses.append(host.cmd("/sbin/ip -6 addr | grep inet6 | awk -F '[ \t]+|/' '{print $3}' | grep -E -v '^fe80*|^::1*'"))
        for host in hosts:
            for address in addresses:
                result = host.cmd("ping6 -c 1 {0} | grep -oP '\d+(?=% packet loss)'".format(address.rstrip()))
                try:
                    packetloss += int(result)
                except(ValueError): # result was string => 'ping failed'
                    packetloss += 100
                    break
        context.pingResult = int(packetloss / len(hosts))
    else:
        context.pingResult = 100 # error case => no host was found



@when('the link between {nd1} and {nd2} is going down')
def step_linkDown(context, nd1, nd2):
    node1 = MininetHelper.getNodeFromName(context.mini, nd1)
    node2 = MininetHelper.getNodeFromName(context.mini, nd2)
    #check if link between nodes is existing
    connectionList = node1.connectionsTo(node2)
    assert_that(len(connectionList), greater_than(0), "Link between %s and %s found" % (nd1,nd2))
    #find the correct link and stop it => link status will be set to "MISSING"
    for link in context.mini.links:
        if((str(node1.name + "-") in str(link.intf1) and str(node2.name + "-") in str(link.intf2)) or
               (str(node1.name + "-") in str(link.intf2) and str(node2.name + "-") in str(link.intf1))):
            link.stop()

@when('we send a http request from host {hst1} to host {hst2}')
def step_httpRequest(context, hst1, hst2):
    h1 = MininetHelper.getNodeFromName(context.mini, hst1)
    h2 = MininetHelper.getNodeFromName(context.mini, hst2)
    #send request
    cmdString = "wget -O - --tries=2  -T30 %s" % h2.IP()
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
    connectionList = s1.connectionsTo(s2)
    assert_that(len(connectionList), greater_than(0), "Link %s <-> %s found" % (sw1,sw2))

@then('switch {sw1} and switch {sw2} will not share a link')
def step_test_connection(context, sw1, sw2):
    s1 = MininetHelper.getNodeFromName(context.mini, sw1)
    s2 = MininetHelper.getNodeFromName(context.mini, sw2)
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

@then('the packetloss is below {ptls} percent')
def step_comparePacketloss(context, ptls):
    result = False
    ptls = int(ptls)
    if 0 <= ptls <= 100:
        if context.pingResult < ptls:
            result = True
    assert_that(result, equal_to(True), ("Packetloss was below %s" % str(ptls)))

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
    #build flow table
    s1FlowTable = MininetHelper.createFlowTable(s1)
    hasEntry = s1FlowTable.hasForwardingEntry(h1.MAC(), h2.MAC())
    assert_that(hasEntry, equal_to(True), "switch %s has forwarding entry for ping traffic" % sw)


@then('the http traffic from host {hst1} to host {hst2} takes the route across switch {sw}')
def step_routeIdentification(context, hst1, hst2, sw):
    s1 = MininetHelper.getNodeFromName(context.mini, sw)
    h1 = MininetHelper.getNodeFromName(context.mini, hst1)
    h2 = MininetHelper.getNodeFromName(context.mini, hst2)
    #buil FlowTable
    s1FlowTable = MininetHelper.createFlowTable(s1)
    hasEntry = s1FlowTable.hasForwardingEntry(h1.MAC(), h2.MAC())
    assert_that(hasEntry, equal_to(True), "switch %s has dl_dst entry for traffic" % sw)




'''
#####################################################################################################

                                    complete topologies

#####################################################################################################
'''


@given('two hosts connected to one switch')
def step_build_topo_1(context):
    # OpenStack part
    if(context.openStackTest == True):
        #deploy infrastructure and configure ports
        workingDir = "terraformFiles/flat_1sw_2h"
        context.tf = TerraformHelper(workingDir, context.behaveLogLevel)
        context.tf.build_topo_1()
        #provide controllers IP
        context.controllerIp = context.tf.tf_get("controller_fip")
        #provide ONOS-Rest access
        context.onosRest = OnosRestAPI(context.controllerIp)
    else:
        # Mininet part
        mnHelper = MininetHelper()
        mnHelper.build_topo_1(context.mini)

@given('four hosts connected to one switch')
def step_build_topo_1(context):
    # OpenStack part
    if(context.openStackTest == True):
        workingDir = "terraformFiles/flat_1sw_4h"
        context.tf = TerraformHelper(workingDir, context.behaveLogLevel)
        context.tf.build_topo_2()
        #provide controllers IP
        context.controllerIp = context.tf.tf_get("controller_fip")
        #provide ONOS-Rest access
        context.onosRest = OnosRestAPI(context.controllerIp)
    else:
        # Mininet part
        mnHelper = MininetHelper()
        mnHelper.build_topo_2(context.mini)

@given('two hosts, each connected to a switch which are connected')
def step_build_topo_1(context):
    # OpenStack part
    if(context.openStackTest == True):
        workingDir = "terraformFiles/flat_2sw_2h"
        context.tf = TerraformHelper(workingDir, context.behaveLogLevel)
        context.tf.build_topo_3()
        #provide controllers IP
        context.controllerIp = context.tf.tf_get("controller_fip")
        #provide ONOS-Rest access
        context.onosRest = OnosRestAPI(context.controllerIp)
    else:
        # Mininet part
        mnHelper = MininetHelper()
        mnHelper.build_topo_3(context.mini)

@given('a tree topo with depth one and fanout two')
def step_build_topo_1(context):
    # OpenStack part
    if(context.openStackTest == True):
        workingDir = "terraformFiles/tree_3sw_4h"
        context.tf = TerraformHelper(workingDir, context.behaveLogLevel)
        context.tf.build_topo_4()
        #provide controllers IP
        context.controllerIp = context.tf.tf_get("controller_fip")
        #provide ONOS-Rest access
        context.onosRest = OnosRestAPI(context.controllerIp)
    else:
        # Mininet part
        mnHelper = MininetHelper()
        mnHelper.build_topo_4(context.mini)








