#switch outputs
output "switch1_Id" {
    value = "${openstack_compute_instance_v2.default_Instance_sw1.id}"
}
output "switch1_fip" {
    value = "${openstack_compute_floatingip_v2.floatip_sw1.address}"
}
output "switch1_portId_one" {
    value = "${openstack_compute_instance_v2.default_Instance_sw1.network.1.port}"
}
output "switch1_portId_two" {
    value = "${openstack_compute_instance_v2.default_Instance_sw1.network.2.port}"
}
#switch outputs
output "switch2_Id" {
    value = "${openstack_compute_instance_v2.default_Instance_sw2.id}"
}
output "switch2_fip" {
    value = "${openstack_compute_floatingip_v2.floatip_sw2.address}"
}
output "switch2_portId_one" {
    value = "${openstack_compute_instance_v2.default_Instance_sw2.network.1.port}"
}
output "switch2_portId_two" {
    value = "${openstack_compute_instance_v2.default_Instance_sw2.network.2.port}"
}


#Port outputs
output "sw1_port_ip_one" {
    value = "${openstack_networking_port_v2.sw1_port_1.fixed_ip.0.ip_address}"
}
output "sw1_port_ip_two" {
    value = "${openstack_networking_port_v2.sw1_port_2.fixed_ip.0.ip_address}"
}
output "sw2_port_ip_one" {
    value = "${openstack_networking_port_v2.sw2_port_1.fixed_ip.0.ip_address}"
}
output "sw2_port_ip_two" {
    value = "${openstack_networking_port_v2.sw2_port_2.fixed_ip.0.ip_address}"
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

