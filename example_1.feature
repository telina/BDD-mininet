Feature: set up a small topology

  Scenario: connection of switches
    Given switch s1 and switch s2
     When we connect switch s1 to switch s2
     Then switch s1 and switch s2 will share a link

  Scenario: connection of switches
     Given switch s4 and switch s5
      When we connect switch s4 to switch s5
      Then switch s4 and switch s6 will not share a link

  Scenario: connection of switches
    Given switches s1 and s2 and s3
     When we connect all switches with each other
     Then switch s1 and switch s3 will share a link

  Scenario: connection of switches
    Given a set of four switches
     When we connect all switches with each other
     Then switch s1 and switch s4 will share a link

  Scenario: connection of switches
    Given a set of 4 switches
     When we connect switch s1 to switch s2
      And we connect switch s1 to switch s3
      And we connect switch s1 to switch s4
     Then switch s2 and switch s3 will not share a link
      And switch s3 and switch s4 will not share a link

  Scenario: connection of a single switch and 2 hosts
    Given a single switch s1
      And a set of two hosts
     When we connect host h1 to switch s1
      And we connect host h2 to switch s1
     Then host h1 is able to ping host h2

  Scenario: mesh net with 4 switches and 2 hosts
    Given a set of 4 switches
      And a set of two hosts
     When we connect all switches with each other
      And we connect host h1 to switch s1
      And we connect host h2 to switch s4
     Then host h1 is able to ping host h2

  Scenario: tree topo with depth 1, 4 switches and 2 hosts
    Given a set of 4 switches
      And a set of two hosts
     When we connect switch s1 to switch s2
      And we connect switch s1 to switch s3
      And we connect switch s1 to switch s4
      And we connect host h1 to switch s2
      And we connect host h2 to switch s4
     Then host h1 is able to ping host h2

  Scenario: bus topo with 3 switches and 2 hosts
    Given a set of 4 switches
      And a set of two hosts
     When we connect switch s1 to switch s2
      And we connect switch s2 to switch s3
      And we connect switch s3 to switch s4
      And we connect host h1 to switch s1
      And we connect host h2 to switch s4
     Then host h1 is able to ping host h2

#  Scenario: mesh net, with link going down
#    Given a set of 4 switches
#      And a set of two hosts
#     When we connect all switches with each other
#      And we connect host h1 to switch s1
#      And we connect host h2 to switch s4
#      And the link between s1 and s4 is going down
#     Then host h1 is able to ping host h2

#  Scenario: two connected switches, with link going down
#    Given switch s1 and switch s2
#     When we connect switch s1 to switch s2
#      And the link between s1 and s2 is going down
#     Then switch s1 and switch s2 will not share a link