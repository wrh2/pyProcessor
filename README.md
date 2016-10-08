# pyProcessor

An application specific processor modelled with the python MyHDL package.

Please be aware that this project is not finished.
It is a "pet project" of mine and something that I plan to continue work on in my free time.
It'll be "complete" someday but I'm not sure what that term really encompasses right now.

### Notes from last release (10/08/16)

I fixed some issues with the ALU logic and initialization of signals for the simulation.
Everything appears to be working as intended now.

### TODO list

1. Automatically calculate time it will take for instructions to complete and set this as the simulation time.
    * This will make it such that the user doesn't have to do it.
2. Ability to output memory to a hex file
3. Improve testing and verification.
    * Add something for testing and verification to the API
4. Make updates to whitepaper
5. Make HALT instructions raise a "stop simulation"

## Contents

code - contains code base

report - contains details about the project

## Dependencies

* [Python](https://www.python.org/)
* [MyHDL](http://www.myhdl.org/)

### Recommended

* [GTKWave](http://gtkwave.sourceforge.net/)
    * For viewing [Value Change Dump](https://en.wikipedia.org/wiki/Value_change_dump) files