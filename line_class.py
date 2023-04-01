from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from config import * 


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
        self.name = "line_"+start_block.name +"_"+str(start_connector)
        self.removed = 0
        with self.canvas:
            if start_connector == INPUT or start_connector == OUTPUT or start_connector == MIXER + 1  or start_connector == MIXER + 2:
                Color(0,0.5,1,OPAQUE, mode="rgba") # blue
            elif "Tap" in start_block.name or start_connector == TAP_IN:
                Color(1.0,0.0,0.0,OPAQUE, mode="rgba") # red
            elif "Pot" in start_block.name or "Constant" in start_block.name or "Envelope" in start_block.name or start_connector <= PARAM6:
                Color(0.50, 0.00, 1.00, OPAQUE)  # purple
            elif "Switch" in start_block.name or (start_connector >= SW0_IN and start_connector <= SW4_IN):
                Color(1,0.5,0,OPAQUE, mode="rgba") # orange
            elif "User" in start_block.name or start_connector == USER0OUT or start_connector == USER1OUT:
                Color(0,1,0,OPAQUE, mode="rgba") # green
            self.line = Line(points=[self.start_point[X], self.start_point[Y], self.end_point[X], self.end_point[Y]], width=2.5, cap='round', joint='none')
        
    def drag_line(self, touch,mode):
        with self.canvas:
            if mode == DRAG_MODE0: # for touch.pos coords
                for block in blocks:
                    if block.name == self.start_block.name: # if in the block that created the connector line
                            self.end_point = touch.pos
                            self.line.points=[self.start_point[X], self.start_point[Y], self.end_point[X], self.end_point[Y]]
            elif mode == DRAG_MODE1: # for touch coord array without
                for block in blocks:
                    if block.name == self.start_block.name: # if in the block that created the connector line
                            self.end_point = touch # touch is pos passed to this function in main function
                            self.line.points=[self.start_point[X], self.start_point[Y], self.end_point[X], self.end_point[Y]]    

    def move_line(self, conX,conY):
        with self.canvas:
            for block in blocks:
                if block.selected == SELECTED:
                    if block.name == self.start_block.name: # if in the block that created the connector line
                            self.start_point = [conX, conY]
                            self.line.points=[self.start_point[X], self.start_point[Y], self.end_point[X], self.end_point[Y]]

                    if block.name == self.end_block.name: # if in the block that the line finished dragging in
                            self.end_point = [conX, conY]
                            self.line.points=[self.start_point[X], self.start_point[Y], self.end_point[X], self.end_point[Y]]      
    
    def remove_line(self):
        with self.canvas:
            if self.removed == 0:
                self.canvas.remove(self.line)
                self.canvas.ask_update()
                self.removed = 1
