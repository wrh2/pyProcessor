
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


## Instruction memory

The instruction memory can be accessed as follows. These contents are set at
instantiation and are specified by the file 'program.hex'. The values are of
type [modbv](http://docs.myhdl.org/en/stable/manual/reference.html?highlight=mod
bv#myhdl.modbv).


    # there's lots of them so we will only do a small portion
    # myProcessor.instruction_memory will yield all the contents
    myProcessor.instruction_memory[0:10]




    [modbv(259602432L),
     modbv(8009985L),
     modbv(8075778L),
     modbv(259799811L),
     modbv(92109689L),
     modbv(92175482L),
     modbv(260013316L),
     modbv(8421246L),
     modbv(260145157L),
     modbv(8552831L)]



### Running a different program

There are currently no methods for changing instruction memory outside of
instantiation. You can run something other than the default program by
specifying a different file at instantiation as follows.


    myProcessor = pyProcessor(instructions='anotherProgram.hex')

Note that this file must contain the instruction in the hex format specified in
the documentation in the report folder...this is obviously not ideal and will
change at a later time. See the included 'program.hex' file for an example.

## Main memory

The contents of main memory can be accessed as follows. These contents are set
at instantiation and are specified by the file 'memory_image.hex'. The values
are of type [modbv](http://docs.myhdl.org/en/stable/manual/reference.html?highli
ght=modbv#myhdl.modbv).


    # there's lots of them so we will only do a small portion
    # myProcessor.main_memory will yield all the contents
    myProcessor.main_memory[0:10]




    [modbv(30722L),
     modbv(50257L),
     modbv(17507L),
     modbv(19011L),
     modbv(64016L),
     modbv(41308L),
     modbv(16474L),
     modbv(19010L),
     modbv(41608L),
     modbv(50836L)]



### Memory initialization

There are currently no methods for changing main memory outside of
instantiation. You can initialize the main memory with something other than the
default memory image as follows.


    myProcessor = pyProcessor(mem_image='myImage.hex')

For an example memory image, see memory_image.hex. For more details on the
memory, see the project documentation in the report folder.
