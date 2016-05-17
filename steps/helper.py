__author__ = 'Bene'

from FlowEntrys import FlowTable
from behave import *
from hamcrest import *
from mininet.topo import *
from mininet.net import *
from mininet.node import OVSController, RemoteController
import requests
import subprocess
from pexpect import pxssh

class MininetHelper(object):

    def __init__(cls, mininet):
        cls.mininetInstanz = mininet

    @classmethod
    def validateNodes(cls, mininet, nodeList):
        for node in nodeList:
            assert node is not None
            assert_that(mininet.__contains__(node), "node %s exists" % node)
        return True

    @classmethod
    def getNodeFromName(cls, mininet, nodeName):
        assert nodeName is not None
        assert_that(mininet.__contains__(nodeName), "node %s exists" % nodeName)
        return mininet.getNodeByName(nodeName)

    @classmethod
    def addSwitches(cls, mininet, numberOfSwitches):
        for i in range (1, numberOfSwitches+1):
            switchName = "s" + str(i)
            #context.testTopo.addSwitch(switchName)
            mininet.addSwitch(switchName)

    @classmethod
    def addHosts(cls, mininet, numberOfHosts):
        for i in range (1, numberOfHosts+1):
            hostName = "h" + str(i)
            mininet.addHost(hostName)

    @classmethod
    def createFullMeshedNet(cls, mininet):
        listOfSwitches = mininet.switches
        listLength = len(listOfSwitches)
        assert_that(listLength, greater_than(1), "More than one switch existing")
        for i in range(0, listLength-1):
            switch1 = str(listOfSwitches[i])
            for j in range(i+1, listLength):
                switch2 = str(listOfSwitches[j])
                mininet.addLink(switch1, switch2)

    @classmethod
    def createFlowTable(cls, switch):
        flows = switch.dpctl("dump-flows")
        return FlowTable(switch, flows)




class NumberConverter(object):
    """Map named numbers into numbers."""
    MAP = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four":  4,
        "five":  5,
        "six":   6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }

    @classmethod
    def convertNumber(cls, number):
        assert number is not None
        if number.isdigit():
            convNumber = int(number)
            assert_that(convNumber, greater_than(0), "number greater than 0")
            return convNumber
        else:
            name = number.strip().lower()
            convNumber = cls.MAP[name]
            assert_that(convNumber, greater_than(0), "number greater than 0")
            return convNumber


class TerraformHelper(object):

    def __init__(cls, wd):
        cls.workingDir = wd
        cls.validNodeNames = ("one", "two", "three", "four", "h1", "h2", "h3", "h4")

    def validateNodes(cls, nodeList):
        for node in nodeList:
            assert node is not None
            assert_that(cls.validNodeNames, has_item(node), "%s in valid nodeNames" % node)

    def ping(cls, host1, host2, timeout):
        #translate hostnames (h1, h2, etc)
        src = cls.translateHostName(host1)
        dst = cls.translateHostName(host2)
        #get Fip and Ip (Fip(floatingIp) for SSH connection)
        srcFip = cls.tf_get(src+"_fip")
        dstIp = cls.tf_get(dst+"_ip")
        try:
            s = pxssh.pxssh()
            ip = srcFip
            username = "ubuntu"
            password = ""
            s.login(ip, username, password)
            s.sendline("ping -c 10 " + dstIp)
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
        #get exitCode and return packetLoss
        if(tmp.splitlines()[1] == "0"):
            packetLoss = 0.0
            return packetLoss
        else:
            packetLoss = -1
            return packetLoss

    def translateHostName(self, host):
        if(host == "h1"):
            return "one"
        elif(host == "h2"):
            return "two"
        elif(host == "h3"):
            return "three"
        elif(host == "h4"):
            return "four"


    def tf_get(cls, arg):
        outputCMD = 'terraform output ' + arg
        output = subprocess.Popen(outputCMD, stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]
        return str(output).rstrip()

    def build_topo_1(cls):
        return_code = subprocess.call("terraform apply", cwd=cls.workingDir, shell=True)
        assert_that(return_code, equal_to(0), "Something went wrong while deploying the Openstack infrastructure with terraform. Please run the test again. If this doesn't solve the problem, check terraform *.tf files for errors." )
        #if(return_code != 0):
        #     raise Exception("Something went wrong while deploying the Openstack infrastructure with terraform. Please run the test again. If this doesn't solve the problem, check terraform *.tf files for errors.")
        cls.config_topo_1()
        raise Exception("Done")

    def build_topo_2(cls):
        return_code = subprocess.call("terraform apply", cwd=cls.workingDir, shell=True)
        assert_that(return_code, equal_to(0), "Something went wrong while deploying the Openstack infrastructure with terraform. Please run the test again. If this doesn't solve the problem, check terraform *.tf files for errors." )
        cls.config_topo_2()
        raise Exception("Done")

    def build_topo_3(cls):
        return_code = subprocess.call("terraform apply", cwd=cls.workingDir, shell=True)
        assert_that(return_code, equal_to(0), "Something went wrong while deploying the Openstack infrastructure with terraform. Please run the test again. If this doesn't solve the problem, check terraform *.tf files for errors." )
        cls.config_topo_3()
        raise Exception("Done")

    def build_topo_4(cls):
        return_code = subprocess.call("terraform apply", cwd=cls.workingDir, shell=True)
        assert_that(return_code, equal_to(0), "Something went wrong while deploying the Openstack infrastructure with terraform. Please run the test again. If this doesn't solve the problem, check terraform *.tf files for errors." )
        cls.config_topo_4()

    def config_topo_1(cls):
        #set "--allowed-address-pair" for topo_1 = "one switch with two hosts"
        port_1 = cls.tf_get('switch1_portId_one')
        port_2 = cls.tf_get('switch1_portId_two')
        ip_cidr = '192.168.0.0/16'
        mac_1 = cls.tf_get('one_mac')
        mac_2 = cls.tf_get('two_mac')
        setAddressPairs_1 = 'neutron port-update ' + port_1 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_2
        subprocess.Popen(setAddressPairs_1, stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]
        setAddressPairs_2 = 'neutron port-update ' + port_2 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_1
        subprocess.Popen(setAddressPairs_2, stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]

    def config_topo_2(cls):
        #set "--allowed-address-pair" for topo_2 = "one switch with four hosts"
        port_1 = cls.tf_get('switch1_portId_one')
        port_2 = cls.tf_get('switch1_portId_two')
        port_3 = cls.tf_get('switch1_portId_three')
        port_4 = cls.tf_get('switch1_portId_four')
        ip_cidr = '192.168.0.0/16'
        mac_1 = cls.tf_get('one_mac')
        mac_2 = cls.tf_get('two_mac')
        mac_3 = cls.tf_get('three_mac')
        mac_4 = cls.tf_get('four_mac')
        #configure port_1 (where vm one is connected to)
        setAddressPairs_1 = 'neutron port-update ' + port_1 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_2 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_3 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_4
        subprocess.Popen(setAddressPairs_1 , stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]
        #configure port_2 (where vm two is connected to)
        setAddressPairs_2 = 'neutron port-update ' + port_2 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_1 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_3 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_4
        subprocess.Popen(setAddressPairs_2 , stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]
        #configure port_3 (where vm three is connected to)
        setAddressPairs_3 = 'neutron port-update ' + port_3 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_1 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_2 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_4
        subprocess.Popen(setAddressPairs_3 , stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]
        #configure port_4 (where vm four is connected to)
        setAddressPairs_4 = 'neutron port-update ' + port_4 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_1 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_2 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_3
        subprocess.Popen(setAddressPairs_4 , stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]

    def config_topo_3(cls):
        #set "--allowed-address-pair" for topo_3 = "two switches with two hosts"
        sw1_port_1 = cls.tf_get('switch1_portId_one')
        sw1_port_2 = cls.tf_get('switch1_portId_two')
        sw2_port_1 = cls.tf_get('switch2_portId_one')
        sw2_port_2 = cls.tf_get('switch2_portId_two')
        ip_cidr = '192.168.0.0/16'
        mac_1 = cls.tf_get('one_mac')
        mac_2 = cls.tf_get('two_mac')
        #configure sw1_port_1 (where vm one is connected to)
        setAddressPairs_1 = 'neutron port-update ' + sw1_port_1 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_2
        subprocess.Popen(setAddressPairs_1 , stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]
        #configure sw1_port_2 (where the other switch is connected to)
        setAddressPairs_2 = 'neutron port-update ' + sw1_port_2 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_1
        subprocess.Popen(setAddressPairs_2 , stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]
        #configure sw2_port_1 (where vm two is connected to)
        setAddressPairs_3 = 'neutron port-update ' + sw2_port_1 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_1
        subprocess.Popen(setAddressPairs_3 , stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]
        #configure sw2_port_2 (where the other switch is connected to)
        setAddressPairs_4 = 'neutron port-update ' + sw2_port_2 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_2
        subprocess.Popen(setAddressPairs_4 , stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]


    def config_topo_4(cls):
        #set "--allowed-address-pair" for topo_4 = "tree topo with three switches and four hosts"
        sw1_port_1 = cls.tf_get('switch1_portId_one')
        sw1_port_2 = cls.tf_get('switch1_portId_two')
        sw1_port_3 = cls.tf_get('switch1_portId_three')
        sw2_port_1 = cls.tf_get('switch2_portId_one')
        sw2_port_2 = cls.tf_get('switch2_portId_two')
        sw2_port_3 = cls.tf_get('switch2_portId_three')
        sw3_port_1 = cls.tf_get('switch3_portId_one')
        sw3_port_2 = cls.tf_get('switch3_portId_two')
        ip_cidr = '192.168.0.0/16'
        mac_1 = cls.tf_get('one_mac')
        mac_2 = cls.tf_get('two_mac')
        mac_3 = cls.tf_get('three_mac')
        mac_4 = cls.tf_get('four_mac')
        #configure sw1_port_1 (where vm one is connected to)
        setAddressPairs_1 = 'neutron port-update ' + sw1_port_1 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_2 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_3 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_4
        subprocess.Popen(setAddressPairs_1 , stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]
        #configure sw1_port_2 (where vm two is connected to)
        setAddressPairs_2 = 'neutron port-update ' + sw1_port_2 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_1 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_3 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_4
        subprocess.Popen(setAddressPairs_2 , stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]
        #configure sw1_port_3 (where the other switch is connected to)
        setAddressPairs_3 = 'neutron port-update ' + sw1_port_3 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_1 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_2
        subprocess.Popen(setAddressPairs_3 , stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]
        #Switch 2
        #configure sw2_port_1 (where vm three is connected to)
        setAddressPairs_4 = 'neutron port-update ' + sw2_port_1 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_1 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_2 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_4
        subprocess.Popen(setAddressPairs_4 , stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]
        #configure sw2_port_2 (where vm four is connected to)
        setAddressPairs_5 = 'neutron port-update ' + sw2_port_2 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_1 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_2 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_3
        subprocess.Popen(setAddressPairs_5 , stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]
        #configure sw2_port_3 (where the other switch is connected to)
        setAddressPairs_6 = 'neutron port-update ' + sw2_port_3 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_3 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_4
        subprocess.Popen(setAddressPairs_6 , stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]
        #Switch 3
        #configure sw3_port_1 (where the other switch is connected to)
        setAddressPairs_7 = 'neutron port-update ' + sw3_port_1 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_3 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_4
        subprocess.Popen(setAddressPairs_7 , stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]
        #configure sw3_port_2 (where the other switch is connected to)
        setAddressPairs_8 = 'neutron port-update ' + sw3_port_2 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_1 + \
                          ' --allowed-address-pair ip_address=' + ip_cidr + ',mac_address=' + mac_2
        subprocess.Popen(setAddressPairs_8 , stdout=subprocess.PIPE, cwd=cls.workingDir, shell=True).communicate()[0]



class openStackEnv(object):
    vmList = []

    def validateVM(cls, vm):
        assert vm is not None
        assert_that(vm not in cls.vmList, "virtual machine %s exists" % vm)
        cls.vmList.append(vm)


