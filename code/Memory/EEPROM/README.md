# EEPROM

Electronically Erasable Programmable Read-Only Memory that serves as the instruction memory of the processor

## Functional description

This memory module holds the instructions to be executed by the processor.
The instructions are generated in the insert_program function.
This function generates hex with gtv.py (generate test vectors) then formats it
into an array that is read in at the initialization of the EEPROM.

### Signals

#### Inputs

* Addr - Address of memory location
* Clk - Clock signal
* Content - Array of hex encoded instructions, initializes memory
* Width - bit width of output

#### Outputs

* Dout - Data in memory location

## Testbench

Tests functionality by iterating through memory locations with Program Counter module over 2000 timesteps

### Example usage

    python testbench.py