from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from config import blocks 


DRAGGING = 1
NOT_DRAGGING = 0

OPAQUE = 1 

SELECTED = 1 
RELEASED = 0

DRAG_MODE0 = 0
DRAG_MODE1 = 1

X = 0
Y = 1 

class MyLine(Widget):

    def __init__(self, touch, start_block, start_connector, **kwargs): 
        super(MyLine, self).__init__(**kwargs)
        self.start_point = touch.pos
        self.end_point = touch.pos
        self.start_block = start_block
        self.end_block = None
        self.start_connector = start_connector
        self.end_connector = None
        self.dragging = DRAGGING
        self.name = "line_"+start_block +"_"+str(start_connector)
        self.removed = 0
        with self.canvas:
            if start_connector >= 10:#green line for inputs/outputs etc
                Color(0.00, 0.60, 0.00, OPAQUE)
            else: #purple line for parameter controls etc
                Color(0.50, 0.00, 0.70, OPAQUE)    
            self.line = Line(points=[self.start_point[X], self.start_point[Y], self.end_point[X], self.end_point[Y]], width=2.5, cap='round', joint='none')
        
    def drag_line(self, touch,mode):
        with self.canvas:
            if mode == DRAG_MODE0:#for touch.pos coords
                for block in blocks:
                    if block.name == self.start_block: #if in the block that created the connector line
                            self.end_point = touch.pos
                            self.line.points=[self.start_point[X], self.start_point[Y], self.end_point[X], self.end_point[Y]]
            elif mode == DRAG_MODE1:#for touch coord array without
                for block in blocks:
                    if block.name == self.start_block: #if in the block that created the connector line
                            self.end_point = touch #touch is pos passed to this function in main function
                            self.line.points=[self.start_point[X], self.start_point[Y], self.end_point[X], self.end_point[Y]]    
      
    def move_line(self, conX,conY):
        with self.canvas:
            for block in blocks:
                if block.selected == SELECTED:
                    if block.name == self.start_block: #if in the block that created the connector line
                            self.start_point = [conX, conY]
                            self.line.points=[self.start_point[X], self.start_point[Y], self.end_point[X], self.end_point[Y]]

                    if block.name == self.end_block: #if in the block that the line finished dragging in
                            self.end_point = [conX, conY]
                            self.line.points=[self.start_point[X], self.start_point[Y], self.end_point[X], self.end_point[Y]]      
    def remove_line(self):
        with self.canvas:
            if self.removed == 0:
                self.canvas.remove(self.line)
                self.canvas.ask_update()
                self.removed = 1
