This is my implementation of A* pathfinding algorithm using Python and PyGame for GUI.
Maze grid is fully interactive, both beginning and the end of the path can be manipulated.
Walls can be created and erased using right click. When you click on the wall it becomes floor
and vise versa.

Any symmetrical 2D array can be used as a maze, but it should consist of numbers 0,1,2,3,4.
Where 0 - wall, 1 - free space, 2 - beginning of the path, 3 - end of the path, and 4 is the
path calulated by the algorithm.

How to install and run:

1. `pip3 install -r requirements.txt`
2. `python3 main.py`

