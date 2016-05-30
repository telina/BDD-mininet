#switch outputs
output "switch1_Id" {
    value = "${openstack_compute_instance_v2.default_Instance_0.id}"
}
output "switch1_fip" {
    value = "${openstack_compute_floatingip_v2.floatip_0.address}"
}
output "switch1_portId_one" {
    value = "${openstack_compute_instance_v2.default_Instance_0.network.1.port}"
}
output "switch1_portId_two" {
    value = "${openstack_compute_instance_v2.default_Instance_0.network.2.port}"
}
output "switch1_portId_three" {
    value = "${openstack_compute_instance_v2.default_Instance_0.network.3.port}"
}
output "switch1_portId_four" {
    value = "${openstack_compute_instance_v2.default_Instance_0.network.4.port}"
}


#Port outputs
output "port_ip_one" {
    value = "${openstack_networking_port_v2.port_1.fixed_ip.0.ip_address}"
}
output "port_ip_two" {
    value = "${openstack_networking_port_v2.port_2.fixed_ip.0.ip_address}"
}
output "port_ip_three" {
    value = "${openstack_networking_port_v2.port_3.fixed_ip.0.ip_address}"
}
output "port_ip_four" {
    value = "${openstack_networking_port_v2.port_4.fixed_ip.0.ip_address}"
}
output "port_mac_one" {
    value = "${openstack_networking_port_v2.port_1.mac_address}"
}
output "port_mac_two" {
    value = "${openstack_networking_port_v2.port_2.mac_address}"
}
output "port_mac_three" {
    value = "${openstack_networking_port_v2.port_3.mac_address}"
}
output "port_mac_four" {
    value = "${openstack_networking_port_v2.port_4.mac_address}"
}

#VM client outputs
output "one_Id" {
    value = "${openstack_compute_instance_v2.default_Instance_1.id}"
}
output "one_fip" {
    value = "${openstack_compute_floatingip_v2.floatip_1.address}"
}
output "one_ip" {
   value = "${openstack_compute_instance_v2.default_Instance_1.network.1.fixed_ip_v4}"
}
output "one_mac" {
   value = "${openstack_compute_instance_v2.default_Instance_1.network.1.mac}"
}

output "two_Id" {
    value = "${openstack_compute_instance_v2.default_Instance_2.id}"
}
output "two_fip" {
    value = "${openstack_compute_floatingip_v2.floatip_2.address}"
}
output "two_ip" {
   value = "${openstack_compute_instance_v2.default_Instance_2.network.1.fixed_ip_v4}"
}
output "two_mac" {
   value = "${openstack_compute_instance_v2.default_Instance_2.network.1.mac}"
}

output "three_Id" {
    value = "${openstack_compute_instance_v2.default_Instance_3.id}"
}
output "three_fip" {
    value = "${openstack_compute_floatingip_v2.floatip_3.address}"
}
output "three_ip" {
   value = "${openstack_compute_instance_v2.default_Instance_3.network.1.fixed_ip_v4}"
}
output "three_mac" {
   value = "${openstack_compute_instance_v2.default_Instance_3.network.1.mac}"
}

output "four_Id" {
    value = "${openstack_compute_instance_v2.default_Instance_4.id}"
}
output "four_fip" {
    value = "${openstack_compute_floatingip_v2.floatip_4.address}"
}
output "four_ip" {
   value = "${openstack_compute_instance_v2.default_Instance_4.network.1.fixed_ip_v4}"
}
output "four_mac" {
   value = "${openstack_compute_instance_v2.default_Instance_4.network.1.mac}"
}

