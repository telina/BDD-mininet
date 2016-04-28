
# Configure the OpenStack Provider
# before terraform apply set TF_VAR_os_user and TF_VAR_os_password

#VARIABLES
variable os_user {
  description = "LDAP username"
}
variable os_password {
  description = "LDAP password (shown in plain-text!)"
}
variable os_project {
  #default = "user-benedikt.pfaff"
  description = "OpenStack Project"
}
variable os_domain_name {
  description = "Domain Name"
}
variable os_auth_url {
  description = "Auth URL"
}



#PROVIDER
provider "openstack" {
    user_name  = "${var.os_user}"
    tenant_name = "${var.os_project}"
    password  = "${var.os_password}"
    domain_name = "${var.os_domain_name}"
    auth_url = "${var.os_auth_url}"
#    api_key = "..."
#    domain_name = "lsinfo3"
#    auth_url  = "https://172.17.0.3:5000/v3"
    insecure = "true"
}



#KEYPAIRS (VM, Mac, Steffen)
resource "openstack_compute_keypair_v2" "bpf" {
    name = "bpf_tf"
    public_key = "${file("~/.ssh/id_rsa_tf.pub")}"
}
resource "openstack_compute_keypair_v2" "mac" {
    name = "mac"
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCUuJ0t4q2vtgYhL+Pevycd6ptnFCCGgFAePIEKq6dmYG8HNrR+VHprfHfn9/8keFuVU2dn0bKR3epV5wEL77O9H5GxNXnVn8JrRNjrIOcwWsua1uMOKumjVsH8IVW0LH+5qUd6zrZ3LP0N52wO8lJpnz4Dk8eTV8lD2Dp+bEIQmvZ1wO+eiWZrhCm59OSiAm2okcpW1NzBBFIwbAK2yhE83F+vZ3ROR9cjIXtvWaYq6EPaSZK1j/7z1Pzuc56by1+uhOlsX6mmXCEcTwhtB6YsMQJ8/s1tLxpNlOLn/C93Lq3AylEifRF/NmHiR/qiQKApks+C5OBq1bDPPFFln3pja6RTGPPt6sAyYv6S4DRspejJilxgKvu3D9XB4T/8Fq6ATTM41zKhn/bwK71F19pCHqtujo71s0F8WNlWE+3/JO+oHtVflMuqhVPI4Jyw/rUH7Rj4pprI7MkOEHIu2R6Xh68ILWhF364M3uXE96cBpBJy/5KZOkCyg2ARls4cjdDrpzjbYmhggY4Qy1LJr/2Yi7bggUpJkq4PVmfGlAVQFGH7qh98Q96bK+utwbZgE8KuRHsFAYPhhWKlLzKcYBh7irtRA8kBAqZ9RV3GOqS2/pl84BaOiu8kPWIeIgLx9LBAoe8E4mLfKLgFhkUbhxGXLzzKyW9SMlcgmHudmsmXCQ== Bene@Bene-MBPs-MacBook-Pro.local"
}
resource "openstack_compute_keypair_v2" "stg" {
    name = "stg_terraform"
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAyRKAea5teRt2KWvkIOnJZ2BPekTSKb0f5mzV87vEap6qcxtVdh1EyHLUhDzkzpgsWiLho6nXTh1iIJnr9D5GFg47Fl70KE9nnjdEuMC7y+RqTxxw1Npi9QuIpIuI/efoWgGEiMQVfooJ/gRDyDwDG/iGXMMlU8s2dDiZ5W/pMKC1ElJzHiws4sorJFcdjLyjPANoCn5YVmZzH9SQTI8Xmsar+opSf311JgDwLRtyuGR3MTFTj3g22MZNNHYj/2pqvYK5n/e9ZlCt2g/Db2jKrTwgjIjwRZfANeYjCY5IHhJsKjGWyLNc+Uuej5GAjDL3DLh0dZzQ1zyQ+ARDB1AYlw== steffen"
}


#NETWORKING
resource "openstack_networking_network_v2" "network_1" {
  name = "access"
  admin_state_up = "true"
}
resource "openstack_networking_network_v2" "network_2" {
  name = "network_left"
  admin_state_up = "true"
}
resource "openstack_networking_network_v2" "network_3" {
  name = "network_right"
  admin_state_up = "true"
}

#NETWORKING  Subnets for Networks
resource "openstack_networking_subnet_v2" "subnet_1" {
  name = "subnet_access"
  network_id = "${openstack_networking_network_v2.network_1.id}"
  cidr = "10.0.0.0/24"
  ip_version = 4
  dns_nameservers = ["132.187.0.13"]
}
resource "openstack_networking_subnet_v2" "subnet_2" {
  name = "subnet_left"
  network_id = "${openstack_networking_network_v2.network_2.id}"
  cidr = "192.168.100.0/24"
  ip_version = 4
  dns_nameservers = ["132.187.0.13"]
}
resource "openstack_networking_subnet_v2" "subnet_3" {
  name = "subnet_right"
  network_id = "${openstack_networking_network_v2.network_3.id}"
  cidr = "192.168.200.0/24"
  ip_version = 4
  dns_nameservers = ["132.187.0.13"]
}

#NETWORKING ports
# definition of ports for the switch
resource "openstack_networking_port_v2" "port_1" {
  name = "port_left"
  security_group_ids = ["cb8b4b7a-714a-4182-927b-71e50c94f053"]
  network_id = "${openstack_networking_network_v2.network_2.id}"
  fixed_ip = {
    subnet_id = "${openstack_networking_subnet_v2.subnet_2.id}"
    ip_address = "192.168.100.10"
  }
  admin_state_up = "true"
}
# definition of ports for the switch
resource "openstack_networking_port_v2" "port_2" {
  name = "port_right"
  security_group_ids = ["cb8b4b7a-714a-4182-927b-71e50c94f053"]
  network_id = "${openstack_networking_network_v2.network_3.id}"
  fixed_ip = {
    subnet_id = "${openstack_networking_subnet_v2.subnet_3.id}"
    ip_address = "192.168.200.10"
  }
  admin_state_up = "true"
}



#ROUTER
#Router for external access
resource "openstack_networking_router_v2" "router" {
  region = "RegionOne"
  name = "Router"
  external_gateway = "753af3b7-49ff-4522-b3a8-0cf85d66b0ff"

}
#ROUTER Interface (access -> Router)
resource "openstack_networking_router_interface_v2" "router_interface" {
  region = ""
  router_id = "${openstack_networking_router_v2.router.id}"
  subnet_id = "${openstack_networking_subnet_v2.subnet_1.id}"
}




#FLOATING IP
resource "openstack_compute_floatingip_v2" "floatip_1" {
  pool = "net04_ext"
}
resource "openstack_compute_floatingip_v2" "floatip_2" {
  pool = "net04_ext"
}
resource "openstack_compute_floatingip_v2" "floatip_3" {
  pool = "net04_ext"
}


#RESOURCES

#VM one
resource "openstack_compute_instance_v2" "default_Instance_1" {
  name = "clientVM"
  image_name = "ubuntu14.04-x64"
  flavor_name = "i3.xmall"
  security_groups = ["default"]
  region = "RegionOne"
  key_pair = "bpf_tf"
#  key_pair = "${openstack_compute_keypair_v2.bpf.name}"
  floating_ip = "${openstack_compute_floatingip_v2.floatip_1.address}"
  network { uuid = "${openstack_networking_network_v2.network_1.id}" }
  network { uuid = "${openstack_networking_network_v2.network_2.id}" }
  provisioner "remote-exec" {
      inline = [
         "sudo sed -i 's/ localhost/ localhost clientVM/' /etc/hosts",
         "sudo ifconfig eth1 ${openstack_compute_instance_v2.default_Instance_1.network.1.fixed_ip_v4} netmask 255.255.0.0",
         "sudo echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCUuJ0t4q2vtgYhL+Pevycd6ptnFCCGgFAePIEKq6dmYG8HNrR+VHprfHfn9/8keFuVU2dn0bKR3epV5wEL77O9H5GxNXnVn8JrRNjrIOcwWsua1uMOKumjVsH8IVW0LH+5qUd6zrZ3LP0N52wO8lJpnz4Dk8eTV8lD2Dp+bEIQmvZ1wO+eiWZrhCm59OSiAm2okcpW1NzBBFIwbAK2yhE83F+vZ3ROR9cjIXtvWaYq6EPaSZK1j/7z1Pzuc56by1+uhOlsX6mmXCEcTwhtB6YsMQJ8/s1tLxpNlOLn/C93Lq3AylEifRF/NmHiR/qiQKApks+C5OBq1bDPPFFln3pja6RTGPPt6sAyYv6S4DRspejJilxgKvu3D9XB4T/8Fq6ATTM41zKhn/bwK71F19pCHqtujo71s0F8WNlWE+3/JO+oHtVflMuqhVPI4Jyw/rUH7Rj4pprI7MkOEHIu2R6Xh68ILWhF364M3uXE96cBpBJy/5KZOkCyg2ARls4cjdDrpzjbYmhggY4Qy1LJr/2Yi7bggUpJkq4PVmfGlAVQFGH7qh98Q96bK+utwbZgE8KuRHsFAYPhhWKlLzKcYBh7irtRA8kBAqZ9RV3GOqS2/pl84BaOiu8kPWIeIgLx9LBAoe8E4mLfKLgFhkUbhxGXLzzKyW9SMlcgmHudmsmXCQ== Bene@Bene-MBPs-MacBook-Pro.local' >> ~/.ssh/authorized_keys",
         "sudo echo 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAyRKAea5teRt2KWvkIOnJZ2BPekTSKb0f5mzV87vEap6qcxtVdh1EyHLUhDzkzpgsWiLho6nXTh1iIJnr9D5GFg47Fl70KE9nnjdEuMC7y+RqTxxw1Npi9QuIpIuI/efoWgGEiMQVfooJ/gRDyDwDG/iGXMMlU8s2dDiZ5W/pMKC1ElJzHiws4sorJFcdjLyjPANoCn5YVmZzH9SQTI8Xmsar+opSf311JgDwLRtyuGR3MTFTj3g22MZNNHYj/2pqvYK5n/e9ZlCt2g/Db2jKrTwgjIjwRZfANeYjCY5IHhJsKjGWyLNc+Uuej5GAjDL3DLh0dZzQ1zyQ+ARDB1AYlw== steffen' >> ~/.ssh/authorized_keys"
      ]
      connection {
          user = "ubuntu"
          type = "ssh"
          private_key = "${file("~/.ssh/id_rsa_tf")}"
          timeout = "2m"
          agent = false
      }
  }
}


#VM switch
resource "openstack_compute_instance_v2" "default_Instance_2" {
  name = "switchVM"
  image_name = "ubuntu14.04-x64"
  flavor_name = "i3.xmall"
  #security_groups = ["bpf_tf_secgroup_1"]
  security_groups = ["default"]
  region = "RegionOne"
  key_pair = "bpf_tf"
#  key_pair = "${openstack_compute_keypair_v2.bpf.name}"
  floating_ip = "${openstack_compute_floatingip_v2.floatip_2.address}"
  #this creates a default port to network_1 (access)
  network { uuid = "${openstack_networking_network_v2.network_1.id}" }
  #this assigns port_1 (network_left) to the switch
  network {
      port = "${openstack_networking_port_v2.port_1.id}"
      #uuid = "${openstack_networking_network_v2.network_2.id}"
  }
  #this assigns port_2 (network_right) to the switch
  network {
      port = "${openstack_networking_port_v2.port_2.id}"
      #uuid = "${openstack_networking_network_v2.network_3.id}"
  }

  provisioner "remote-exec" {
      # edit /etc/hosts to prevent error "unable to resolve host switch"
      inline = [
          "sudo sed -i 's/ localhost/ localhost switchVM/' /etc/hosts",
          "sudo ifconfig eth1 promisc ${openstack_networking_port_v2.port_1.fixed_ip.0.ip_address} netmask 255.255.0.0 up",
          "sudo ifconfig eth2 promisc ${openstack_networking_port_v2.port_2.fixed_ip.0.ip_address} netmask 255.255.0.0 up",
          "sudo apt-get update",
          "sudo apt-get -y upgrade",
          "sudo apt-get update",
          "sudo apt-get install -y openvswitch-switch",
          "sudo apt-get install -y openvswitch-common",
          "sudo ovs-vsctl add-br myBridge",
          "sudo ovs-vsctl add-port myBridge eth1",
          "sudo ovs-vsctl add-port myBridge eth2",
          "sudo ovs-vsctl set-controller myBridge tcp:10.0.0.66:6633",
          "sudo ovs-vsctl set-fail-mode myBridge secure",
          "sudo ovs-ofctl add-flow myBridge 'in_port=1,priority=10,actions=output:2'",
          "sudo ovs-ofctl add-flow myBridge 'in_port=2,priority=10,actions=output:1'",
          "sudo echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCUuJ0t4q2vtgYhL+Pevycd6ptnFCCGgFAePIEKq6dmYG8HNrR+VHprfHfn9/8keFuVU2dn0bKR3epV5wEL77O9H5GxNXnVn8JrRNjrIOcwWsua1uMOKumjVsH8IVW0LH+5qUd6zrZ3LP0N52wO8lJpnz4Dk8eTV8lD2Dp+bEIQmvZ1wO+eiWZrhCm59OSiAm2okcpW1NzBBFIwbAK2yhE83F+vZ3ROR9cjIXtvWaYq6EPaSZK1j/7z1Pzuc56by1+uhOlsX6mmXCEcTwhtB6YsMQJ8/s1tLxpNlOLn/C93Lq3AylEifRF/NmHiR/qiQKApks+C5OBq1bDPPFFln3pja6RTGPPt6sAyYv6S4DRspejJilxgKvu3D9XB4T/8Fq6ATTM41zKhn/bwK71F19pCHqtujo71s0F8WNlWE+3/JO+oHtVflMuqhVPI4Jyw/rUH7Rj4pprI7MkOEHIu2R6Xh68ILWhF364M3uXE96cBpBJy/5KZOkCyg2ARls4cjdDrpzjbYmhggY4Qy1LJr/2Yi7bggUpJkq4PVmfGlAVQFGH7qh98Q96bK+utwbZgE8KuRHsFAYPhhWKlLzKcYBh7irtRA8kBAqZ9RV3GOqS2/pl84BaOiu8kPWIeIgLx9LBAoe8E4mLfKLgFhkUbhxGXLzzKyW9SMlcgmHudmsmXCQ== Bene@Bene-MBPs-MacBook-Pro.local' >> ~/.ssh/authorized_keys",
          "sudo echo 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAyRKAea5teRt2KWvkIOnJZ2BPekTSKb0f5mzV87vEap6qcxtVdh1EyHLUhDzkzpgsWiLho6nXTh1iIJnr9D5GFg47Fl70KE9nnjdEuMC7y+RqTxxw1Npi9QuIpIuI/efoWgGEiMQVfooJ/gRDyDwDG/iGXMMlU8s2dDiZ5W/pMKC1ElJzHiws4sorJFcdjLyjPANoCn5YVmZzH9SQTI8Xmsar+opSf311JgDwLRtyuGR3MTFTj3g22MZNNHYj/2pqvYK5n/e9ZlCt2g/Db2jKrTwgjIjwRZfANeYjCY5IHhJsKjGWyLNc+Uuej5GAjDL3DLh0dZzQ1zyQ+ARDB1AYlw== steffen' >> ~/.ssh/authorized_keys"
      ]
      connection {
          user = "ubuntu"
          type = "ssh"
          private_key = "${file("~/.ssh/id_rsa_tf")}"
          timeout = "2m"
          agent = false
      }
  }
}

#VM server
resource "openstack_compute_instance_v2" "default_Instance_3" {
  name = "serverVM"
  image_name = "ubuntu14.04-x64"
  flavor_name = "i3.xmall"
  #security_groups = ["bpf_tf_secgroup_1"]
  security_groups = ["default"]
  region = "RegionOne"
  key_pair = "bpf_tf"
#  key_pair = "${openstack_compute_keypair_v2.bpf.name}"
  floating_ip = "${openstack_compute_floatingip_v2.floatip_3.address}"
  network { uuid = "${openstack_networking_network_v2.network_1.id}" }
  network { uuid = "${openstack_networking_network_v2.network_3.id}" }


  provisioner "remote-exec" {
      inline = [
          "sudo sed -i 's/ localhost/ localhost serverVM/' /etc/hosts",
          "sudo ifconfig eth1 ${openstack_compute_instance_v2.default_Instance_3.network.1.fixed_ip_v4} netmask 255.255.0.0",
          "sudo apt-get update",
          "sudo apt-get install apache2 -y",
          "sudo echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCUuJ0t4q2vtgYhL+Pevycd6ptnFCCGgFAePIEKq6dmYG8HNrR+VHprfHfn9/8keFuVU2dn0bKR3epV5wEL77O9H5GxNXnVn8JrRNjrIOcwWsua1uMOKumjVsH8IVW0LH+5qUd6zrZ3LP0N52wO8lJpnz4Dk8eTV8lD2Dp+bEIQmvZ1wO+eiWZrhCm59OSiAm2okcpW1NzBBFIwbAK2yhE83F+vZ3ROR9cjIXtvWaYq6EPaSZK1j/7z1Pzuc56by1+uhOlsX6mmXCEcTwhtB6YsMQJ8/s1tLxpNlOLn/C93Lq3AylEifRF/NmHiR/qiQKApks+C5OBq1bDPPFFln3pja6RTGPPt6sAyYv6S4DRspejJilxgKvu3D9XB4T/8Fq6ATTM41zKhn/bwK71F19pCHqtujo71s0F8WNlWE+3/JO+oHtVflMuqhVPI4Jyw/rUH7Rj4pprI7MkOEHIu2R6Xh68ILWhF364M3uXE96cBpBJy/5KZOkCyg2ARls4cjdDrpzjbYmhggY4Qy1LJr/2Yi7bggUpJkq4PVmfGlAVQFGH7qh98Q96bK+utwbZgE8KuRHsFAYPhhWKlLzKcYBh7irtRA8kBAqZ9RV3GOqS2/pl84BaOiu8kPWIeIgLx9LBAoe8E4mLfKLgFhkUbhxGXLzzKyW9SMlcgmHudmsmXCQ== Bene@Bene-MBPs-MacBook-Pro.local' >> ~/.ssh/authorized_keys",
          "sudo echo 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAyRKAea5teRt2KWvkIOnJZ2BPekTSKb0f5mzV87vEap6qcxtVdh1EyHLUhDzkzpgsWiLho6nXTh1iIJnr9D5GFg47Fl70KE9nnjdEuMC7y+RqTxxw1Npi9QuIpIuI/efoWgGEiMQVfooJ/gRDyDwDG/iGXMMlU8s2dDiZ5W/pMKC1ElJzHiws4sorJFcdjLyjPANoCn5YVmZzH9SQTI8Xmsar+opSf311JgDwLRtyuGR3MTFTj3g22MZNNHYj/2pqvYK5n/e9ZlCt2g/Db2jKrTwgjIjwRZfANeYjCY5IHhJsKjGWyLNc+Uuej5GAjDL3DLh0dZzQ1zyQ+ARDB1AYlw== steffen' >> ~/.ssh/authorized_keys"
      ]
      connection {
          user = "ubuntu"
          type = "ssh"
          private_key = "${file("~/.ssh/id_rsa_tf")}"
          timeout = "2m"
          agent = false
      }
  }
}

