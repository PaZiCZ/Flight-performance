# Flight-performance
The repository contains a basic flight performance analysis discussed in the Flight Mechanics course at the Institute of Aerospace Engineering.

The main parts of the project are:
main.py - main control file which calls a sequence of the flight performance analysis and can include an optimisation loop
plane.py - Input file with aircraft description, which includes geometrical characteristics, power unit choice, and drag polar characteristics
isa.py - define international standard atmosphere parameters
power.py - functions which return power of the engine and propeller
polar.py - function which returns a drag polar of the aircraft
performance.py - analyse flight performance
out.py - plot graphical results of the flight performance analysis
