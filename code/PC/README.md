# Program Counter

A simple program counter modelled with MyHDL.

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

Tests functionality described above over 2000 timesteps

### Example usage

    python testbench.py