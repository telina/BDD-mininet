__author__ = 'Bene'

import string

# class to hold flow entrys

class FlowTable(object):

    def __init__(self, switch=None, tableString=None):
        self.switch = switch
        self.tableString = tableString
        #holds alls entrys of a given switch
        self.table = []
        #fill table
        #split tablestring by row
        __rows = string.split(tableString, '\n')  # --> ['Entry 1', 'Line 2', 'Line 3']
        #iterate each row and fill table with entrys
        attributes = []
        for rowIndex in range(1, len(__rows)):
            attributes = __rows[rowIndex].replace(' actions', ',actions').split(',')
            #create entrys with attributs
            #attributes for each entry
            cookie=None
            duration=None
            table=None
            n_packets=None
            n_bytes=None
            idle_age=None
            priority=None
            in_port = None
            dl_vlan = None
            dl_src = None
            dl_dst = None
            dl_type = None
            nw_src = None
            nw_dst = None
            nw_prot = None
            nw_tos = None
            tp_src = None
            tp_dst = None
            icmp_type = None
            icmp_code = None
            actions = None
            for index in range(0, len(attributes)):
                attributeToCheck = attributes[index]
                #if else if cascade to match keys
                if("cookie" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    cookie = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("duration" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    duration = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("table" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    table = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("n_packets" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    n_packets = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("n_bytes" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    n_bytes = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("idle_age" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    idle_age = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("priority" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    priority = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("in_port" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    in_port = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("dl_vlan" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    dl_vlan = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("dl_src" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    dl_src = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("dl_dst" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    dl_dst = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("dl_type" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    dl_type = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("nw_src" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    nw_src = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("nw_dst" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    nw_dst = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("nw_prot" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    nw_prot = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("nw_tos" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    nw_tos = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("tp_src" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    tp_src = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("icmp_type" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    icmp_type = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("icmp_code" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    icmp_code = attributeToCheck[splitIndex : len(attributeToCheck)]
                elif("actions" in attributeToCheck):
                    splitIndex = attributeToCheck.find('=') + 1
                    actions = attributeToCheck[splitIndex : len(attributeToCheck)]
            if(actions is not None):
                entry = FlowEntry(cookie, duration, table,n_packets, n_bytes, idle_age, priority, in_port,
                              dl_vlan, dl_src, dl_dst, dl_type, nw_src, nw_dst, nw_prot, nw_tos, tp_src,
                              tp_dst, icmp_type, icmp_code, actions)
                self.table.append(entry)




    # def printTable(self):
    #     print("table len = %s" % len(self.table))
    #     for index in range(0, len(self.table)):
    #         self.table[index].printEntry()

    def hasEntryWithMacDest(self, mac):
        for index in range(0, len(self.table)):
            if(self.table[index].dl_dst == mac):
                return True
            else:
                return False

    def hasForwardingEntry(self, mac):
        #check all entrys in table
        for index in range(0, len(self.table)):
            entry = self.table[index]
            #check if entry has MAC as dest and action is output (rather than drop)
            if(entry.dl_dst == mac and "output" in entry.actions):
                return True
        return False

    def printTable(self):
        #check all entrys in table
        for index in range(0, len(self.table)):
            entry = self.table[index]
            entry.printEntry()

    # def splitFirstLine(self):
    #     line = self.table[1]
    #     #line.replace(' actions', ',actions')
    #     #print(string.split(line, ','))
    #     #myLine = string.split(line, ',')
    #     myLine = line.replace(' actions', ',actions').split(',')
    #     for index in range(0, len(myLine)):
    #         print(myLine[index])





class FlowEntry(object):

    def __init__(self, cookie=None, duration=None, table=None, n_packets=None, n_bytes=None,
                 idle_age=None, priority=None, in_port=None, dl_vlan=None, dl_src=None, dl_dst=None,
                 dl_type=None, nw_src=None, nw_dst=None, nw_prot=None, nw_tos=None,
                 tp_src=None, tp_dst=None, icmp_type=None, icmp_code=None,
                 actions=None):
        '''
        in_port=port_no
            Matches physical port port_no. Switch ports are numbered as displayed by dpctl show.
        dl_vlan=vlan
            Matches IEEE 802.1q virtual LAN tag vlan. Specify 0xffff as vlan to match packets that
            are not tagged with a virtual LAN; otherwise, specify a number between 0 and 4095, inclusive,
            as the 12-bit VLAN ID to match.
        dl_src=mac
            Matches Ethernet source address mac, which should be specified as 6 pairs of hexadecimal digits
            delimited by colons, e.g. 00:0A:E4:25:6B:B0.
        dl_dst=mac
            Matches Ethernet destination address mac.
        dl_type=ethertype
            Matches Ethernet protocol type ethertype, which should be specified as a integer between 0 and 65535,
            inclusive, either in decimal or as a hexadecimal number prefixed by 0x, e.g. 0x0806 to match ARP packets.
        nw_src=ip[/netmask]
            Matches IPv4 source address ip, which should be specified as an IP address or host name,
            e.g. 192.168.1.1 or www.example.com. The optional netmask allows matching only on an
            IPv4 address prefix. It may be specified as a dotted quad (e.g. 192.168.1.0/255.255.255.0) or
            as a count of bits (e.g. 192.168.1.0/24).
        nw_dst=ip[/netmask]
            Matches IPv4 destination address ip.
        nw_proto=proto
            Matches IP protocol type proto, which should be specified as a decimal number between 0 and 255,
            inclusive, e.g. 6 to match TCP packets.
        nw_tos=tos/dscp
            Matches ToS/DSCP (only 6-bits, not modify reserved 2-bits for future use) field of IPv4 header tos/dscp,
            which should be specified as a decimal number between 0 and 255, inclusive.
        tp_src=port
            Matches UDP or TCP source port port, which should be specified as a decimal number between 0 and 65535,
            inclusive, e.g. 80 to match packets originating from a HTTP server.
        tp_dst=port
            Matches UDP or TCP destination port port.
        icmp_type=type
            Matches ICMP message with type, which should be specified as a decimal number between 0 and 255, inclusive.
        icmp_code=code
            Matches ICMP messages with code.
        '''
        self.cookie=cookie
        self.duration=duration
        self.table=table
        self.n_packets=n_packets
        self.n_bytes=n_bytes
        self.idle_age=idle_age
        self.priority=priority
        self.in_port = in_port
        self.dl_vlan = dl_vlan
        self.dl_src = dl_src
        self.dl_dst = dl_dst
        self.dl_type = dl_type
        self.nw_src = nw_src
        self.nw_dst = nw_dst
        self.nw_prot = nw_prot
        self.nw_tos = nw_tos
        self.tp_src = tp_src
        self.tp_dst = tp_dst
        self.icmp_type = icmp_type
        self.icmp_code = icmp_code
        self.actions = actions

    def printEntry(self):
         print("cookie="+str(self.cookie)),
         print("duration="+str(self.duration)),
         print("table="+str(self.table)),
         print("n_packets="+str(self.n_packets)),
         print("n_bytes="+str(self.n_bytes)),
         print("idle_age="+str(self.idle_age)),
         print("priority="+str(self.priority)),
         print("in_port="+str(self.in_port)),
         print("dl_vlan="+str(self.dl_vlan)),
         print("dl_src="+str(self.dl_src)),
         print("dl_dst="+str(self.dl_dst)),
         print("dl_type="+str(self.dl_type)),
         print("nw_src="+str(self.nw_src)),
         print("nw_dst="+str(self.nw_dst)),
         print("nw_prot="+str(self.nw_prot)),
         print("nw_tos="+str(self.nw_tos)),
         print("tp_src="+str(self.tp_src)),
         print("tp_dst="+str(self.tp_dst)),
         print("icmp_type="+str(self.icmp_type)),
         print("icmp_code="+str(self.icmp_code)),
         print("actions="+str(self.actions))
