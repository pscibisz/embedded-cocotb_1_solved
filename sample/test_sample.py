import random

import cocotb
from cocotb.triggers import Timer, FallingEdge
from cocotb.clock import Clock
from cocotb.handle import Force, Release, Deposit

# Without time trigger values will be encrypted after 2500us
@cocotb.test()
async def sample_randomised_test(dut):
    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock
    await FallingEdge(dut.clk)              # Synchronize with the clock

    dut.disable_seq.value = Force(0)
    dut.disable_time.value = Force(0)

    for i in range(30):
        dut.cnt.value = Force(0)
        dut.input_.value = current = random.randint(0, 255)
        await Timer(100, 'us')
        assert dut.output_.value == (~current & 0xff)

        dut._log.info("out is %s", dut.output_.value)

# Values after 2500us shouldn't be encrypted
@cocotb.test()
async def sample_randomised_time_trigger_test(dut):
    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock
    await FallingEdge(dut.clk)              # Synchronize with the clock

    dut.cnt.value = Release()
    dut.cnt.value = Deposit(0)
    dut.disable_time.value = Release()
    dut.disable_time.value = Deposit(0)
    dut.disable_seq.value = Force(0)
    

    for i in range(25):
        dut.input_.value = current = random.randint(0, 255)
        await Timer(100, 'us')
        assert dut.output_.value == (~current & 0xff)
        dut._log.info("out is %s", dut.output_.value)

    for i in range(24):
        dut.input_.value = current = random.randint(0, 255)
        await Timer(100, 'us')
        assert dut.output_.value == (current & 0xff)
        dut._log.info("out is %s", dut.output_.value)

# Input trojan sequence
@cocotb.test()
async def sample_sequence_injection_test(dut):
    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock
    await FallingEdge(dut.clk)              # Synchronize with the clock

    dut.cnt.value = Force(0)
    dut.disable_time.value = Force(0)
    dut.disable_seq.value = Release()
    dut.disable_seq.value = Deposit(0)

    # Encryption should work at this stage
    dut.input_.value = current = random.randint(0, 255)
    await Timer(100, 'us')
    assert dut.output_.value == (~current & 0xff)
    
    # Enter the sequence that launches the trojan
    dut.input_.value = current = 0x21
    await Timer(100, 'us')
    assert dut.output_.value == (~current & 0xff)

    dut.input_.value = current = 0xF1
    await Timer(100, 'us')
    assert dut.output_.value == (~current & 0xff)

    # The last value of the sequence should still be encrypted
    dut.input_.value = current = 0x37
    await Timer(100, 'us')
    assert dut.output_.value == (~current & 0xff)

    # Next value shouldn't be encrypted
    dut.input_.value = current = random.randint(0, 255)
    await Timer(100, 'us')
    assert dut.output_.value == (current & 0xff)

# Encryption should be disabled when both time and sequence triggers are enabled
@cocotb.test()
async def sample_time_sequence_reg_enabled_test(dut):
    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock
    await FallingEdge(dut.clk)              # Synchronize with the clock

    dut.disable_time.value = Force(1)
    dut.disable_seq.value = Force(1)

    dut.input_.value = current = random.randint(0, 255)
    await Timer(100, 'us')
    assert dut.output_.value == (current & 0xff)

# When both are disabled value should be encrypted
@cocotb.test()
async def sample_time_sequence_reg_disabled_test(dut):
    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock
    await FallingEdge(dut.clk)              # Synchronize with the clock

    dut.disable_time.value = Force(0)
    dut.disable_seq.value = Force(0)

    dut.input_.value = current = random.randint(0, 255)
    await Timer(100, 'us')
    assert dut.output_.value == (~current & 0xff)

# Time trigger should remove encryption alone
@cocotb.test()
async def sample_time_reg_enabled_test(dut):
    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock
    await FallingEdge(dut.clk)              # Synchronize with the clock

    dut.disable_time.value = Force(1)
    dut.disable_seq.value = Force(0)

    dut.input_.value = current = random.randint(0, 255)
    await Timer(100, 'us')
    assert dut.output_.value == (current & 0xff)

# Sequence trigger should remove encryption alone
@cocotb.test()
async def sample_sequence_reg_enabled_test(dut):
    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock
    await FallingEdge(dut.clk)              # Synchronize with the clock

    dut.disable_time.value = Force(0)
    dut.disable_seq.value = Force(1)

    dut.input_.value = current = random.randint(0, 255)
    await Timer(100, 'us')
    assert dut.output_.value == (current & 0xff)