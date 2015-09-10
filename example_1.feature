Feature: set up and test a small topology

#  Scenario: connection of switches
#    Given a single switch
#      And a single switch
#      And we connect switch s1 to switch s2
#     Then switch s1 and switch s2 will share a link
#
#  Scenario: connection of switches
#     Given a set of two switches
#       And we connect switch s1 to switch s2
#      Then switch s1 and switch s3 will not share a link
#
#  Scenario: connection of switches
#    Given a set of 3 switches
#      And we connect all switches with each other
#     Then switch s1 and switch s3 will share a link
#
#  Scenario: connection of switches
#    Given a set of four switches
#      And we connect all switches with each other
#     Then switch s1 and switch s4 will share a link
#
#  Scenario: connection of switches
#    Given a set of 4 switches
#      And we connect switch s1 to switch s2
#      And we connect switch s1 to switch s3
#      And we connect switch s1 to switch s4
#     Then switch s1 and switch s2 will share a link
#      And switch s3 and switch s4 will not share a link

              #works
  Scenario: connection of a single switch and 2 hosts
    Given a set of 2 switches
      And a set of two hosts
      And we connect switch s1 to switch s2
      And we connect host h1 to switch s1
      And we connect host h2 to switch s2
     When host h1 pings host h2
     Then the ping succeeds
###
#  Scenario: mesh net with 4 switches and 2 hosts
#    Given a set of 4 switches
#      And a set of two hosts
#      And we connect all switches with each other
#      And we connect host h1 to switch s1
#      And we connect host h2 to switch s1
#     When host h1 pings host h2
#     Then the ping succeeds
#
##
#  Scenario: tree topo with depth 1, 4 switches and 2 hosts
#    Given a set of 4 switches
#      And a set of two hosts
#      And we connect switch s1 to switch s2
#      And we connect switch s1 to switch s3
#      And we connect switch s1 to switch s4
#      And we connect host h1 to switch s2
#      And we connect host h2 to switch s4
#     When host h1 pings host h2
#     Then the ping succeeds
##
#    Scenario: tree topo with depth 1, 4 switches and 2 hosts
#    Given a set of 4 switches
#      And a set of two hosts
#      And we connect switch s1 to switch s2
#      And we connect switch s1 to switch s3
#      And we connect switch s1 to switch s4
#      And we connect host h1 to switch s1
#      And we connect host h2 to switch s4
#      When host h1 pings host h2
#      Then the ping succeeds
##
#  Scenario: bus topo with 3 switches and 2 hosts
#    Given a set of 4 switches
#      And a set of two hosts
#      And we connect switch s1 to switch s2
#      And we connect switch s2 to switch s3
#      And we connect switch s3 to switch s4
#      And we connect host h1 to switch s1
#      And we connect host h2 to switch s3
#     When host h1 pings host h2
#     Then the ping succeeds
#

#  Scenario: connection of switches
#    Given a set of two switches
#      And a set of 2 hosts
#      And we connect switch s1 to switch s2
#      And we connect host h1 to switch s1
#      And we connect host h2 to switch s2
#     When we start a webserver on host h1
#      And we send a HTTP request from host h2 to host h1
##     Then host h2 is able to send a HTTP request to host h1
#     Then the request succeeds
#
#  Scenario: two connected switches, with link going down
#    Given a set of two switches
#      And we connect switch s1 to switch s2
#     When the link between s1 and s2 is going down
#     Then switch s1 and switch s2 will not share a link

#
#  Scenario: two connected switches, with link going down
#    Given a set of two switches
#      And a set of 2 hosts
#      And we connect switch s1 to switch s2
#      And we connect host h1 to switch s1
#      And we connect host h2 to switch s2
#     When the link between s1 and s2 is going down
#      And host h1 pings host h2
#     Then the ping fails
##
#  Scenario: mesh net, with link going down
#    Given a set of 4 switches
#      And a set of two hosts
#      And we connect all switches with each other
#      And we connect host h1 to switch s1
#      And we connect host h2 to switch s4
#     When the link between s1 and s4 is going down
#      And host h1 pings host h2
#     Then the ping succeeds

##  Scenario: net with static vlans
##    Given a set of 1 switches
##      And a set of 2 hosts
##     #When we connect switch s1 to switch s2
##      And we connect host h1 to switch s1
##      And we connect host h2 to switch s1
##      #And we connect host h3 to switch s2
##      And we assign host h1 on switch s1 to VLAN 11
##      #And we assign host h2 on switch s2 to VLAN 12
##      #And we assign host h3 on switch s2 to VLAN 20
##     Then host h1 is not able to ping host h2
##      #And host h1 is not able to ping host h3

  Scenario: simple net with route identification
    Given a set of 5 switches
      And a set of 2 hosts
      And we connect switch s1 to switch s2
      And we connect switch s1 to switch s4
      And we connect switch s2 to switch s3
      And we connect switch s3 to switch s5
      And we connect switch s4 to switch s5
      And we connect host h1 to switch s1
      And we connect host h2 to switch s5
 #    Then host h1 is able to ping host h2
     When host h1 pings host h2
     Then the ping traffic from host h1 to host h2 takes the route across switch s3
 #     And switch s4 is next hop from switch s1 for ping

#  Scenario: simple net with route identification
#    Given a set of 5 switches
#      And a set of 2 hosts
#     When we connect switch s1 to switch s2
#      And we connect switch s1 to switch s4
#      And we connect switch s2 to switch s3
#      And we connect switch s3 to switch s5
#      And we connect switch s4 to switch s5
#      And we connect host h1 to switch s1
#      And we connect host h2 to switch s5
#      And we start a webserver on host h2
#     Then the http traffic from host h1 to host h2 takes the route across switch s2