# Multiprocessing-Pool-map
This program offers a rapid solution for processing extensive lists of coordinates representing polygon points. It efficiently calculates the area using the Shoelace Method. In the solution it give 2 solution a serial and a parallelized parallelized, where the parallelized it's faster than the serial, as long as you have a large file (more poligon better time performance for the parallelized vertion) .
-
To run the program use a `.txt` file which have to have this structure per line: `[(x,y),(x,y)]`. Where `x` and `y` are coordinates.
The list of the can be as long as you need and every line means 1 polygon.

