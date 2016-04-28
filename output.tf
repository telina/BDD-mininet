#switch outputs
output "switch_Id" {
    value = "${openstack_compute_instance_v2.default_Instance_2.id}"
}
output "switch_fip" {
    value = "${openstack_compute_floatingip_v2.floatip_2.address}"
}
#output "switch_ip_left" {
#   value = "${openstack_compute_instance_v2.default_Instance_2.network.1.fixed_ip_v4}"
#}
#output "switch_mac_left" {
#   value = "${openstack_compute_instance_v2.default_Instance_2.network.1.mac}"
#}
#output "switch_ip_right" {
#   value = "${openstack_compute_instance_v2.default_Instance_2.network.2.fixed_ip_v4}"
#}
#output "switch_mac_right" {
#   value = "${openstack_compute_instance_v2.default_Instance_2.network.2.mac}"
#}
output "portId_left" {
    value = "${openstack_compute_instance_v2.default_Instance_2.network.1.port}"
}
output "portId_right" {
    value = "${openstack_compute_instance_v2.default_Instance_2.network.2.port}"
}


#Port outputs
output "port_ip_left" {
    value = "${openstack_networking_port_v2.port_1.fixed_ip.0.ip_address}"
}
output "port_ip_right" {
    value = "${openstack_networking_port_v2.port_2.fixed_ip.0.ip_address}"
}
output "port_mac_left" {
    value = "${openstack_networking_port_v2.port_1.mac_address}"
}
output "port_mac_right" {
    value = "${openstack_networking_port_v2.port_2.mac_address}"
}

#VM client outputs
output "clientVM_Id" {
    value = "${openstack_compute_instance_v2.default_Instance_1.id}"
}
output "clientVM_fip" {
    value = "${openstack_compute_floatingip_v2.floatip_1.address}"
}
output "clientVM_ip" {
   value = "${openstack_compute_instance_v2.default_Instance_1.network.1.fixed_ip_v4}"
}
output "clientVM_mac" {
   value = "${openstack_compute_instance_v2.default_Instance_1.network.1.mac}"
}

#VM server outputs
output "serverVM_Id" {
    value = "${openstack_compute_instance_v2.default_Instance_3.id}"
}
output "serverVM_fip" {
    value = "${openstack_compute_floatingip_v2.floatip_3.address}"
}
output "serverVM_ip" {
   value = "${openstack_compute_instance_v2.default_Instance_3.network.1.fixed_ip_v4}"
}
output "serverVM_mac" {
   value = "${openstack_compute_instance_v2.default_Instance_3.network.1.mac}"
}

