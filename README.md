# Flight-performance
The repository contains a basic flight performance analysis discussed in the Flight Mechanics course at the Institute of Aerospace Engineering. The code can analyse an existing aircraft model or create a new model based on some aircraft parameters and description.

The main parts of the project are:  
main.py - main control file which calls a sequence of the flight performance analysis  
plane.py - Input file with aircraft description, includes aircraft geometrical characteristics, power unit choice, and drag polar characteristics  
isa.py - define international standard atmosphere parameters  
power.py - functions which return power estimation of the engine and propeller based on engine type  
polar.py - function which returns a drag polar of the aircraft  
performance.py - analyse flight performance  
out.py - plot graphical results of the flight performance analysis  


