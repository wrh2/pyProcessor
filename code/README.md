
# Example Usage

## Instantiation

This works:


    import pyProcessor
    myProcessor = pyProcessor.pyProcessor()

but you can also do this:


    from pyProcessor import *
    myProcessor = pyProcessor()

## Simulation

To run the default amount of timesteps do:


    myProcessor.simulate()

    <class 'myhdl._SuspendSimulation'>: Simulated 1000 timesteps


You can also specify the amount of timestamps


    myProcessor.simulate(5000)

    <class 'myhdl._SuspendSimulation'>: Simulated 5000 timesteps


## Running a different program

You can run something other than the default program by specifying a different
file at instantiation as such


    myProcessor = pyProcessor(instructions='anotherProgram.hex')

Note that this file must contain the instruction in the hex format specified in
the documentation in the report folder...this is obviously not ideal and will
change at a later time. See the included program.hex file for an example.

## Memory initialization

You can initialize the memory image with your own as such


    myProcessor = pyProcessor(mem_image='myImage.hex')

For an example memory image, see memory_image.hex. For more details on the
memory, see the project documentation in the report folder.
