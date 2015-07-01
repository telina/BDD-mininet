Feature: set up a small topology

  Scenario: connection of switches
    Given switch s1 and switch s2
     When we connect the switches
     Then switch s1 and switch s2 will share a link

  Scenario: connection of switches
     Given switch s4 and switch s5
      When we connect the switches
      Then switch s4 and switch s6 will share a link