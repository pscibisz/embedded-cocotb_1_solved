# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0
# Simple tests for an adder module
import random

from adder_model import adder_model

import cocotb
from cocotb.triggers import Timer, FallingEdge
from cocotb.clock import Clock


@cocotb.test()
async def adder_basic_test(dut):
    """Test for 5 + 10"""

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock
    await FallingEdge(dut.clk)              # Synchronize with the clock

    A = 5
    B = 10

    dut.A.value = A
    dut.B.value = B
    await Timer(100, 'us')

    assert dut.X.value == adder_model(
        A, B
    ), f"Adder result is incorrect: {dut.X.value} != 15"


@cocotb.test()
async def adder_randomised_test(dut):
    """Test for adding 2 random numbers multiple times"""

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock
    await FallingEdge(dut.clk)              # Synchronize with the clock

    for i in range(10):

        A = random.randint(0, 15)
        B = random.randint(0, 15)

        dut.A.value = A
        dut.B.value = B

        await Timer(100, 'us')

        assert dut.X.value == adder_model(
            A, B
        ), "Randomised adder test failed: {A} + {B} = {X}".format(
            A=dut.A.value, B=dut.B.value, X=dut.X.value
        )
