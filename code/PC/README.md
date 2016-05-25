# Program Counter

A simple program counter modelled with MyHDL.

## Contents

This folder contains the program counter module (PC.py) and a testbench for it (testbench.py). The Test folder contains testing documentation for the program counter along with vcd files from the testbench.

## Functional description

Incremenets by 4 when EN signal is asserted. Load signal causes Value to be next output of progam counter.

### Signals

#### Inputs

* EN - Enable, control signal for incrementing counter
* Load - Control signal for loading value into program counter
* Value - Value to load into program counter, loaded when load signal asserted

#### Outputs

* Output - Counter value 

## Testbench

Tests functionality described above over 1000 timesteps

### Example usage

    python testbench.py