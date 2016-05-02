__author__ = 'Bene'

import subprocess
import json

'''
this class provides basic terraform commands
before use, make sure config_os file got sourced
'''
class terraformHelper (object):

    '''
    deploy openstack environment (defined in "main.tf") with "terraform apply"
    check exitcode to be 0
    '''
    def tf_apply(self):
        return_code = subprocess.call("terraform apply", shell=True)
        if(return_code != 0):
            raise Exception("Deploying Openstack with terraform went wrong. Please check terraform *.tf files for errors.")

    # destroys deployed openstack infrastructure
    def tf_destroy(self):
        return_code = subprocess.call("terraform destroy", shell=True)
        subprocess.call("yes", shell=True)
        if(return_code != 0):
            raise Exception("Something went wrong during destruction of your openstack infrastructure.")

    # reads output from "output.tf" file and makes IPs, MACs and OS-IDs accessible for behave tests
    def tf_get(self, arg):
        outputCMD = 'terraform output ' + arg
        output = subprocess.Popen(outputCMD , stdout=subprocess.PIPE, shell=True).communicate()[0]
        return str(output).rstrip()



class neutronHelper (object):

    '''
    set additional IP/MAC pair for port
    if not set, openstack drops packets with IP/MAC different from the ports IP/MAC
    '''
    def nt_setIpMacPair(self, portName, ip, mac):
        #output = subprocess.Popen('neutron port-show port_left -f json' , stdout=subprocess.PIPE, shell=True).communicate()[0]
        #parsed_json = json.loads(output)
        #print(parsed_json["name"])

        #NOTE: this port-update deletes all other IP/MAC pairs
        command = 'neutron port-update ' + portName + ' --allowed-address-pair ip_address=' + ip + ',mac_address=' + mac
        subprocess.Popen(command , stdout=subprocess.PIPE, shell=True).communicate()[0]