__author__ = 'Bene'

from behave   import *
from hamcrest import assert_that, equal_to
from switchDummy import *

@given('switch {sX} and switch {sY}')
def step_impl(context, sX, sY):
    assert sX is not None
    context.sX = sX
    context.switch1 = switch(sX)
    assert sY is not None
    context.sY = sY
    context.switch2 = switch(sY)

@when('we connect the switches')
def step_connect(context):
    context.switch1.addLink(context.sX,context.sY)
    context.switch2.addLink(context.sY,context.sX)

@then('switch {swX} and switch {swY} will share a link')
def step_test_connection(context, swX, swY):
    assert swX is not None
    assert swY is not None
    assert_that(True, equal_to(context.switch1.testLink(swY) and context.switch2.testLink(swX)))

    #if context.switch1.name == swX and context.switch2.name == swY:
     #   assert_that(True, equal_to(context.switch1.testLink(swY)))

    #if context.switch1 == switch.returnSwitch(sX) and context.switch2 == switch.returnSwitch(sY):
     #   assert_that(True, equal_to(context.switch1.testLink(sY)))



