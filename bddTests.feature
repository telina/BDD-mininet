
  Feature: Run topology tests

#    Scenario: one Switch and two hosts
#        Given two hosts connected to one switch
#         When host h1 pings host h2
#         Then the ping succeeds
#
#    Scenario: one switch and four hosts
#        Given four hosts connected to one switch
#         When host h1 pings host h4
#         Then the ping succeeds
#
#    Scenario: two switches and two hosts
#        Given two hosts, each connected to a switch which are connected
#         When host h1 pings host h2
#         Then the ping succeeds
#
    Scenario: tree topo with three switches and four hosts
        Given a tree topo with depth one and fanout two
         When host h2 pings host h3
         Then the ping succeeds






#Feature: set up and test a small topology
#
#  Scenario: Nr.1 connection of switches
#    Given a single switch
#      And a single switch
#      And we connect switch s1 to switch s2
#     Then switch s1 and switch s2 will share a link
#
#  Scenario: Nr.2 connection of switches
#    Given a set of three switches
#      And we connect switch s1 to switch s2
#     Then switch s1 and switch s3 will not share a link
#
#  Scenario: Nr.3 connection of switches
#    Given a set of 3 switches
#      And we connect all switches with each other
#     Then switch s1 and switch s3 will share a link
#
#  Scenario: Nr.4 connection of switches
#    Given a set of four switches
#      And we connect all switches with each other
#     Then switch s1 and switch s4 will share a link
#
#  Scenario: Nr.5 connection of switches
#    Given a set of 4 switches
#      And we connect switch s1 to switch s2
#      And we connect switch s1 to switch s3
#      And we connect switch s1 to switch s4
#     Then switch s1 and switch s2 will share a link
#      And switch s3 and switch s4 will not share a link
#
#  Scenario: Nr.6 two connected switches, with link going down
#    Given a set of two switches
#      And we connect switch s1 to switch s2
#     When the link between s1 and s2 is going down
#     Then switch s1 and switch s2 will not share a link
#
#  Scenario: Nr.7 connection of 2 switches and 2 hosts
#    Given a set of 2 switches
#      And a set of two hosts
#      And we connect switch s1 to switch s2
#      And we connect host h1 to switch s1
#      And we connect host h2 to switch s2
#     When host h1 pings host h2
#     Then the ping succeeds
#
#  Scenario: Nr.8 mesh net with 4 switches and 2 hosts
#    Given a set of 4 switches
#      And a set of two hosts
#      And we connect all switches with each other
#      And we connect host h1 to switch s1
#      And we connect host h2 to switch s1
#     When host h1 pings host h2
#     Then the ping succeeds
#
#  Scenario: Nr.9 tree topo with depth 1, 4 switches and 2 hosts
#    Given a set of 4 switches
#      And a set of two hosts
#      And we connect switch s1 to switch s2
#      And we connect switch s1 to switch s3
#      And we connect switch s1 to switch s4
#      And we connect host h1 to switch s2
#      And we connect host h2 to switch s4
#     When host h1 pings host h2
#     Then the ping succeeds
#
#  Scenario: Nr.10 tree topo with depth 2, 7 switches and 2 hosts
#    Given a set of 7 switches
#      And a set of two hosts
#      And we connect switch s1 to switch s2
#      And we connect switch s1 to switch s3
#      And we connect switch s2 to switch s4
#      And we connect switch s2 to switch s5
#      And we connect switch s3 to switch s6
#      And we connect switch s3 to switch s7
#      And we connect host h1 to switch s5
#      And we connect host h2 to switch s7
#      When host h1 pings host h2
#      Then the ping succeeds
#
#  Scenario: No.11 bus topo with 3 switches and 2 hosts
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
#  Scenario: Nr.12 connection of switches
#    Given a set of two switches
#      And a set of 2 hosts
#      And we connect switch s1 to switch s2
#      And we connect host h1 to switch s1
#      And we connect host h2 to switch s2
#      And we start a webserver on host h1
#     When we send a http request from host h2 to host h1
#     Then the request succeeds
#
#  Scenario: Nr.13 two connected switches, with link going down
#    Given a set of two switches
#      And a set of 2 hosts
#      And we connect switch s1 to switch s2
#      And we connect host h1 to switch s1
#      And we connect host h2 to switch s2
#     When the link between s1 and s2 is going down
#      And host h1 pings host h2
#     Then the ping fails
#
#  Scenario: Nr.14 mesh net, with single link going down
#    Given a set of 4 switches
#      And a set of two hosts
#      And we connect all switches with each other
#      And we connect host h1 to switch s1
#      And we connect host h2 to switch s4
#     When the link between s1 and s4 is going down
#      And host h1 pings host h2
#     Then the ping succeeds
#
#  Scenario: Nr.15 simple net with route identification
#    Given a set of 5 switches
#      And a set of 2 hosts
#      And we connect switch s1 to switch s2
#      And we connect switch s1 to switch s4
#      And we connect switch s2 to switch s3
#      And we connect switch s3 to switch s5
#      And we connect switch s4 to switch s5
#      And we connect host h1 to switch s1
#      And we connect host h2 to switch s5
#     When host h1 pings host h2
#     Then the ping traffic from host h1 to host h2 takes the route across switch s4
#
#  Scenario: Nr.16 simple net with 3 routes between hosts
#    Given a set of 10 switches
#      And a set of 2 hosts
#      And we connect switch s1 to switch s2
#      And we connect switch s1 to switch s5
#      And we connect switch s1 to switch s8
#      And we connect switch s2 to switch s3
#      And we connect switch s3 to switch s4
#      And we connect switch s5 to switch s6
#      And we connect switch s6 to switch s7
#      And we connect switch s4 to switch s9
#      And we connect switch s7 to switch s9
#      And we connect switch s8 to switch s9
#      And we connect switch s9 to switch s10
#      And we connect host h1 to switch s1
#      And we connect host h2 to switch s10
#     When host h1 pings host h2
#     Then the ping traffic from host h1 to host h2 takes the route across switch s8
#
#  Scenario: Nr.17 simple net with route identification
#    Given a set of 5 switches
#      And a set of 2 hosts
#      And we connect switch s1 to switch s2
#      And we connect switch s1 to switch s4
#      And we connect switch s2 to switch s3
#      And we connect switch s3 to switch s5
#      And we connect switch s4 to switch s5
#      And we connect host h1 to switch s1
#      And we connect host h2 to switch s5
#      And we start a webserver on host h2
#     When we send a http request from host h1 to host h2
#     Then the http traffic from host h1 to host h2 takes the route across switch s4


# IPv6 Tests
#
#  Scenario: Directed IPv6 Ping
#    Given four hosts connected to one switch
#      And we enable IPv6 addressing
#      When host h1 pings host h2 2 times via IPv6
#    Then the ping succeeds
#
#  Scenario: IPv6 Pingall with less than 20% packetloss
#    Given a tree topo with depth one and fanout two
#      And we enable IPv6 addressing
#      When we ping all hosts via IPv6
#    Then the packetloss is below 20 percent