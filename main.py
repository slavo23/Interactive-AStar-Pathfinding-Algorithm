from grid import Grid
import pygame
import sys

grid1 = [[0,0,0,0,0,0,0,0,0,0],
        [0,1,1,0,2,1,1,1,1,0],
        [0,1,1,0,1,1,1,1,1,0],
        [0,1,1,0,1,1,1,1,1,0],
        [0,1,1,0,0,0,0,1,1,0],
        [0,1,1,1,1,1,1,1,1,0],
        [0,1,0,1,1,1,1,1,1,0],
        [0,1,0,1,1,1,1,1,1,0],
        [0,3,0,1,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0]]



SCREEN_SIZE = (600, 600)

class Cell:
    def __init__(self, x, y, value, b_box = None):
        self.x = x
        self.y = y
        self.value = value
        self.b_box = b_box


class App:
    def __init__(self, grid, width=600, height=600):
        self.grid   = grid
        self.width  = width
        self.height = height

        # State related stuff
        self.running = True
        self.app     = pygame
        self.app.init()
        self.window  = self.app.display.set_mode(SCREEN_SIZE, 0, 32)
        self.clock   = self.app.time.Clock()
        self.dragged = False
        self.current = None

        self.objects = []

       


    
        self.app.display.set_caption("A* Pathfinding")

    def replace(self, prev, curr):
        value_pair = [prev.value, curr.value]
        if 0 not in value_pair:
            self.swap(prev, curr)
            self.current = False
        
            
    def swap(self, prev, curr):
        to_swap = self.grid.clean_map()

        temp = to_swap[prev.x][prev.y]
        to_swap[prev.x][prev.y] = to_swap[curr.x][curr.y]
        to_swap[curr.x][curr.y] = temp

        new_grid = Grid(to_swap)

        self.grid = new_grid
        self.draw_grid()


    def edit(self, event):
        node = self.get_cell(event)
        inv  = not bool(node.value)
        if node.value in [0, 1]:
            new_grid = self.grid.clean_map()
            new_grid[node.x][node.y] = int(inv)
            self.grid = Grid(new_grid)
            self.draw_grid()


    def hover(self, event):
        next_node = self.get_cell(event)
        prev_node = self.current
        self.replace(prev_node, next_node)
        return
        
    
    def get_cell(self, event):

        # This variables in the beginning are used
        # because PyGame demonstrated strange behavour
        # of event loop when i tried to return there values
        # right out of for loop.

        x, y = 0, 0
        val  = 0
        for obj in self.objects:
            if obj.b_box.collidepoint(event.pos):
                x, y = obj.x, obj.y
                val  = obj.value
        return Cell(x, y, val, None)

    def left_click(self, event):
        node = self.get_cell(event)
        if node != None:
            if self.dragged:
                self.dragged = False
                self.replace(self.current, node)
            else:
                self.current = node
                self.dragged = True
                

    def draw_grid(self):
        self.objects = []
        
        rect_x = self.width   // self.grid.rows
        rect_y = self.height // self.grid.cols
        maze   = self.grid.solve(4)

        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                x1 = i * rect_x
                y1 = j * rect_y
                x2 = x1 + rect_x
                y2 = y1 + rect_y
                
                lightblue = (230,230,250) # lightblue
                red       = (255, 0, 0)   # red
                blue      = (0,0,205)     # blue
                green     = (60,179,113)  # green
                gold      = (255,215,0)   # gold


                code  = maze[i][j]

                color = (0, 0, 0)

                if code == 0:
                    color = blue
                if code == 1:
                    color = lightblue
                if code == 2:
                    color = red
                if code == 3:
                    color = red
                if code == 4:
                    color = gold
                

                rect = pygame.Rect(x1,y1,x2,y2)
               
                cell = Cell(i, j, code, rect)
                self.app.draw.rect(self.window, color, rect, 0)
                self.objects.append(cell)


    def event_loop(self):
        
        self.draw_grid()
        while self.running:
            
            for e in self.app.event.get():
                if e.type == self.app.QUIT:
                    self.running = False
                if e.type == self.app.MOUSEBUTTONDOWN:
                    if e.button == 1: # Left click (Positioning mode)
                        self.left_click(e)
                        self.app.display.update()
                    if e.button == 3: # Right click (Editing mode)
                        self.edit(e)
                        
            self.app.display.update()
        
        self.clock.tick(60)
        self.app.quit()
        self.app.display.quit()
        sys.exit()




grid = [[0,0,0,0,0,0,0,0,0,0],
        [0,1,1,0,2,1,1,1,1,0],
        [0,1,1,0,1,1,1,1,1,0],
        [0,1,1,0,1,1,1,1,1,0],
        [0,1,1,0,0,0,0,1,1,0],
        [0,1,1,1,1,1,1,1,1,0],
        [0,1,0,1,1,1,1,1,1,0],
        [0,1,0,1,1,1,1,1,1,0],
        [0,3,0,1,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0]]



app = App(Grid(grid), 600, 600)

app.event_loop()