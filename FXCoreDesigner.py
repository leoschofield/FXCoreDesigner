# LeoSchofield 01/01/2022
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle, Color, Line
from kivy.core.window import Window
import random

BLOCK_WIDTH = 100 
BLOCK_HEIGHT = 50

BUTTON_HEIGHT = 30

OPAQUE = 1 

THRESH = 20

blocks = []

DONT_ASSIGN_LINE = 0
ASSIGN_LINE = 1

DRAG_MODE0 = 0
DRAG_MODE1 = 1

STOPPED = 0 
STARTED = 1 

X = 0
Y = 1 

TRUE = 1
FALSE = 0

MOVING = 1
STILL = 0

SELECTED = 1 
RELEASED = 0

COLLISION = 1
NO_COLLISION = 0

DRAGGING = 1
NOT_DRAGGING = 0

MIXER = 20
SPLITTER = 30

MAX_PARAMS = 6
#========================================================================        
#============================Line========================================
#========================================================================
class MyLine(Widget):

    def __init__(self, touch, start_block, start_connector,nblockParams, **kwargs): 
        super(MyLine, self).__init__(**kwargs)
        self.start_point = touch.pos
        self.end_point = touch.pos
        self.start_block = start_block
        self.end_block = None
        self.start_connector = start_connector
        self.end_connector = None
        self.dragging = DRAGGING
        #self.nBlockParams = nblockParams
        self.name = "line_"+start_block +"_"+str(start_connector)
        if start_connector >= 10:
            Color(0.00, 0.60, 0.00, OPAQUE)
        else: #purple line
            Color(0.50, 0.00, 0.70, OPAQUE)    
        self.line = Line(points=[self.start_point[X], self.start_point[Y], self.end_point[X], self.end_point[Y]], width=2.5, cap='round', joint='none')
        
    def drag_line(self, touch,mode):
        with self.canvas:
            if mode == 0:
                for block in blocks:
                    if block.name == self.start_block: #if in the block that created the connector line
                            self.end_point = touch.pos
                            self.line.points=[self.start_point[X], self.start_point[Y], self.end_point[X], self.end_point[Y]]
            elif mode == 1:
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
    def delete_line(self):
        pass

#========================================================================        
#============================Block=======================================
#========================================================================
class Block(Widget):
    def __init__(self,name,inputConnector,outputConnector,nParams, **kwargs):
        super(Block, self).__init__(**kwargs)
        self.name = name
        self.Xpos = random.randrange(100, 1500)
        self.Ypos = random.randrange(100, 800)
        Color(0.4,0.4,0.4,OPAQUE, mode="rgba")
        self.rect = Rectangle(pos=(self.Xpos,self.Ypos), size=(BLOCK_WIDTH,BLOCK_HEIGHT))
        self.label = Label(pos=(self.Xpos, self.Ypos - (self.rect.size[Y]/2)),text=name)
        self.selected = RELEASED
        self.nParams = nParams
        self.paramCons = []
        self.conLines = []
        self.inputExists = 0 
        self.outputExists = 0
        Color(0.8,0.8,0.8,OPAQUE, mode="rgba")
        
        if inputConnector: ## todo need multiple inputs for mixers,stereo effects, etc 
            self.input = Rectangle(pos=(self.Xpos,self.Ypos+20), size=(10,10))
            self.inputExists = True

        if outputConnector: ## todo need multiple outputs for splitters,stereo effects, etc
            self.output = Rectangle(pos=(self.Xpos+90,self.Ypos+20), size=(10,10))
            self.outputExists = True

        if self.nParams == SPLITTER: 
            self.output1 = Rectangle(pos=(self.Xpos+90,self.Ypos+30), size=(10,10))
            self.output2 = Rectangle(pos=(self.Xpos+90,self.Ypos+10), size=(10,10))
            self.param1Con = Rectangle(pos=(self.Xpos+30,self.Ypos+40), size=(10,10))
            self.param2Con = Rectangle(pos=(self.Xpos+60,self.Ypos+40), size=(10,10))

        elif self.nParams == MIXER: 
            self.input1 = Rectangle(pos=(self.Xpos,self.Ypos+30), size=(10,10))
            self.input2 = Rectangle(pos=(self.Xpos,self.Ypos+10), size=(10,10))
            self.param1Con = Rectangle(pos=(self.Xpos+30,self.Ypos+40), size=(10,10))
            self.param2Con = Rectangle(pos=(self.Xpos+60,self.Ypos+40), size=(10,10))

        elif self.nParams == 10: #potentiometers/constant
            pass

        elif self.nParams == 6:  
            self.param1Con = Rectangle(pos=(self.Xpos+15,self.Ypos+40), size=(10,10))
            self.param2Con = Rectangle(pos=(self.Xpos+45,self.Ypos+40), size=(10,10))
            self.param3Con = Rectangle(pos=(self.Xpos+75,self.Ypos+40), size=(10,10))
            self.param4Con = Rectangle(pos=(self.Xpos+15,self.Ypos), size=(10,10))
            self.param5Con = Rectangle(pos=(self.Xpos+45,self.Ypos), size=(10,10))
            self.param6Con = Rectangle(pos=(self.Xpos+75,self.Ypos), size=(10,10))         

        elif self.nParams == 5:
            self.param1Con = Rectangle(pos=(self.Xpos+15,self.Ypos+40), size=(10,10))
            self.param2Con = Rectangle(pos=(self.Xpos+45,self.Ypos+40), size=(10,10))
            self.param3Con = Rectangle(pos=(self.Xpos+75,self.Ypos+40), size=(10,10))
            self.param4Con = Rectangle(pos=(self.Xpos+30,self.Ypos), size=(10,10))
            self.param5Con = Rectangle(pos=(self.Xpos+60,self.Ypos), size=(10,10))

        elif self.nParams == 4: 
            self.param1Con = Rectangle(pos=(self.Xpos+30,self.Ypos+40), size=(10,10))
            self.param2Con = Rectangle(pos=(self.Xpos+60,self.Ypos+40), size=(10,10))
            self.param3Con = Rectangle(pos=(self.Xpos+30,self.Ypos), size=(10,10))
            self.param4Con = Rectangle(pos=(self.Xpos+60,self.Ypos), size=(10,10))

        elif self.nParams == 3:
            self.param1Con = Rectangle(pos=(self.Xpos+30,self.Ypos+40), size=(10,10))
            self.param2Con = Rectangle(pos=(self.Xpos+60,self.Ypos+40), size=(10,10))
            self.param3Con = Rectangle(pos=(self.Xpos+45,self.Ypos), size=(10,10))

        elif self.nParams == 2:
            self.param1Con = Rectangle(pos=(self.Xpos+30,self.Ypos+40), size=(10,10))
            self.param2Con = Rectangle(pos=(self.Xpos+60,self.Ypos+40), size=(10,10))

        elif self.nParams == 1:
            if self.inputExists:
                self.param1Con = Rectangle(pos=(self.Xpos+45,self.Ypos+40), size=(10,10))
            else: # if a potentiometer or constant block
                self.param1Con = Rectangle(pos=(self.Xpos+45,self.Ypos+0), size=(10,10))

    def delete_block(self):
        pass


    #------------------------------------------- move connectors and lines
    def move_connectors(self,touch,moveX,moveY):
        #========================================Input Connector
        if self.inputExists == True:
            temp = list(self.input.pos)
            if moveX:
                temp[X] = touch.pos[0] + 0
            if moveY:
                temp[Y] = touch.pos[1] + 20
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 11:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 11:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.input.pos = tuple(temp)

        #========================================Output Connector
        if self.outputExists == True: 
            temp = list(self.output.pos)
            if moveX:
                temp[X] = touch.pos[0] + 90
            if moveY:
                temp[Y] = touch.pos[1] + 20
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 10:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 10:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.output.pos = tuple(temp)
        
        #========================================Splitter
        if self.nParams == SPLITTER: 
            #**********************************Level 1
            temp = list(self.param1Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 30
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5)  
            self.param1Con.pos = tuple(temp)

            #**********************************Level 2
            temp = list(self.param2Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 60
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param2Con.pos = tuple(temp)

            #**********************************output 1
            temp = list(self.output1.pos)
            if moveX:
                temp[X] = touch.pos[0] + 90
            if moveY:
                temp[Y] = touch.pos[1] + 30
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 31:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 31:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.output1.pos = tuple(temp)

            #**********************************output 1
            temp = list(self.output2.pos)
            if moveX:
                temp[X] = touch.pos[0] + 90
            if moveY:
                temp[Y] = touch.pos[1] + 10
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 32:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 32:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.output2.pos = tuple(temp)
        #========================================Mixer
        if self.nParams == MIXER: 
            #**********************************Level 1
            temp = list(self.param1Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 30
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5)  
            self.param1Con.pos = tuple(temp)

            #**********************************Level 2
            temp = list(self.param2Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 60
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param2Con.pos = tuple(temp)

            #**********************************input 1
            temp = list(self.input1.pos)
            if moveX:
                temp[X] = touch.pos[0] + 0
            if moveY:
                temp[Y] = touch.pos[1] + 30
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 21:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 21:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.input1.pos = tuple(temp)

            #**********************************input 2
            temp = list(self.input2.pos)
            if moveX:
                temp[X] = touch.pos[0] + 0
            if moveY:
                temp[Y] = touch.pos[1] + 10
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 22:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 22:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.input2.pos = tuple(temp)
        #========================================6 Parameters
        if self.nParams == 6:  
            #**********************************Connector 1
            temp = list(self.param1Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 15
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param1Con.pos = tuple(temp)

            #**********************************Connector 2
            temp = list(self.param2Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 45
            if moveY:    
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param2Con.pos = tuple(temp)

            #**********************************Connector 3
            temp = list(self.param3Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 75
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 3:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 3:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param3Con.pos = tuple(temp)

            #**********************************Connector 4
            temp = list(self.param4Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 15
            if moveY:
                temp[Y] = touch.pos[1] + 0
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 4:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 4:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param4Con.pos = tuple(temp)

            #**********************************Connector 5
            temp = list(self.param5Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 45
            if moveY:
                temp[Y] = touch.pos[1] + 0
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 5:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 5:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param5Con.pos = tuple(temp)

            #**********************************Connector 6
            temp = list(self.param6Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 75
            if moveY:
                temp[Y] = touch.pos[1] + 0
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 6:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 6:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param6Con.pos = tuple(temp)

        #========================================5 Parameters
        elif self.nParams == 5:  
            #**********************************Connector 1
            temp = list(self.param1Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 15
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param1Con.pos = tuple(temp)

            #**********************************Connector 2
            temp = list(self.param2Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 45
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param2Con.pos = tuple(temp)

            #**********************************Connector 3
            temp = list(self.param3Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 75
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 3:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 3:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param3Con.pos = tuple(temp)

            #**********************************Connector 4
            temp = list(self.param4Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 30
            if moveY:
                temp[Y] = touch.pos[1] + 0
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 4:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 4:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param4Con.pos = tuple(temp)

            #**********************************Connector 5
            temp = list(self.param5Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 60
            if moveY:
                temp[Y] = touch.pos[1] + 0
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 5:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 5:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param5Con.pos = tuple(temp)    


        #========================================4 Parameters
        elif self.nParams == 4:  
            #**********************************Connector 1
            temp = list(self.param1Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 30
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param1Con.pos = tuple(temp)

            #**********************************Connector 2
            temp = list(self.param2Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 60
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param2Con.pos = tuple(temp)

            #**********************************Connector 3
            temp = list(self.param3Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 30
            if moveY:
                temp[Y] = touch.pos[1] + 0
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 3:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 3:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param3Con.pos = tuple(temp)

            #**********************************Connector 4
            temp = list(self.param4Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 60
            if moveY:
                temp[Y] = touch.pos[1] + 0
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 4:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 4:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param4Con.pos = tuple(temp)

        #========================================3 Parameters
        elif self.nParams == 3:  
            #**********************************Connector 1
            temp = list(self.param1Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 30
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param1Con.pos = tuple(temp)

            #**********************************Connector 2
            temp = list(self.param2Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 60
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param2Con.pos = tuple(temp)

            #**********************************Connector 3
            temp = list(self.param3Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 45
            if moveY:
                temp[Y] = touch.pos[1] + 0
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 3:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 3:
                        conLine.move_line(temp[X]+5,temp[Y]+5)  
            self.param3Con.pos = tuple(temp)

        #========================================2 Parameters
        elif self.nParams == 2:  
            #**********************************Connector 1
            temp = list(self.param1Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 30
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5)  
            self.param1Con.pos = tuple(temp)

            #**********************************Connector 2
            temp = list(self.param2Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 60
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param2Con.pos = tuple(temp)

        #========================================1 Parameter
        elif self.nParams == 1: 
            #**********************************Connector 1
            temp = list(self.param1Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 45
            if moveY:
                if self.inputExists:
                    temp[Y] = touch.pos[1] + 40
                else:
                    temp[Y] = touch.pos[1] + 0
            for conLine in self.conLines: #move connected lines
                if conLine.start_block == self.name:
                    if conLine.start_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block == self.name:
                    if conLine.end_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param1Con.pos = tuple(temp)



  #-------------------------------------------is touch inside connector
    def is_inside_connector(self,touch,allow_assign_line):
        if self.inputExists:
            if touch.pos[X] > self.input.pos[X] and touch.pos[X] < (self.input.pos[X] + self.input.size[X]):
                if touch.pos[Y] > self.input.pos[Y] and touch.pos[Y] < (self.input.pos[Y] + self.input.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block == self.name: #line starts in this block
                                    if conLine.start_connector == 11: #dont assign a new line if there is one on this connector   
                                        return 11 
                                elif conLine.end_block == self.name: #line ends in this block
                                    if conLine.end_connector == 11: #dont assign a new line if there is one on this connector   
                                        return 11  
                            self.assign_line(touch,self.name,11,self.nParams)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,self.name,11,self.nParams)
                    return 11  

        if self.outputExists:
            if touch.pos[X] > self.output.pos[X] and touch.pos[X] < (self.output.pos[X] + self.output.size[X]):
                if touch.pos[Y] > self.output.pos[Y] and touch.pos[Y] < (self.output.pos[Y] + self.output.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block == self.name: #line starts in this block
                                    if conLine.start_connector == 10: #dont assign a new line if there is one on this connector   
                                        return 10  
                                elif conLine.end_block == self.name: #line ends in this block
                                    if conLine.end_connector == 10: #dont assign a new line if there is one on this connector   
                                        return 10  
                            self.assign_line(touch,self.name,10,self.nParams)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,self.name,10,self.nParams)
                    return 10  

        if self.nParams == SPLITTER:
            if touch.pos[X] > self.output1.pos[X] and touch.pos[X] < (self.output1.pos[X] + self.output1.size[X]):
                if touch.pos[Y] > self.output1.pos[Y] and touch.pos[Y] < (self.output1.pos[Y] + self.output1.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block == self.name: #line starts in this block
                                    if conLine.start_connector == 31: #dont assign a new line if there is one on this connector   
                                        return 31  
                                elif conLine.end_block == self.name: #line ends in this block
                                    if conLine.end_connector == 31: #dont assign a new line if there is one on this connector   
                                        return 31  
                            self.assign_line(touch,self.name,31,self.nParams)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,self.name,31,self.nParams)
                    return 31

            if touch.pos[X] > self.output2.pos[X] and touch.pos[X] < (self.output2.pos[X] + self.output2.size[X]):
                if touch.pos[Y] > self.output2.pos[Y] and touch.pos[Y] < (self.output2.pos[Y] + self.output2.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block == self.name: #line starts in this block
                                    if conLine.start_connector == 32: #dont assign a new line if there is one on this connector   
                                        return 32 
                                elif conLine.end_block == self.name: #line ends in this block
                                    if conLine.end_connector == 32: #dont assign a new line if there is one on this connector   
                                        return 32  
                            self.assign_line(touch,self.name,32,self.nParams)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,self.name,32,self.nParams)
                    return 32      
            
          #==============Parameter 2 
            if self.nParams >= 2:                
                if touch.pos[X] > self.param2Con.pos[X] and touch.pos[X] < (self.param2Con.pos[X] + self.param2Con.size[X]):
                    if touch.pos[Y] > self.param2Con.pos[Y] and touch.pos[Y] < (self.param2Con.pos[Y] + self.param2Con.size[Y]):
                        self.selected = RELEASED
                        if allow_assign_line:
                            if self.conLines != []: # if there are conlines
                                for conLine in self.conLines:
                                    if conLine.start_block == self.name: #line starts in this block
                                        if conLine.start_connector == 2: #dont assign a new line if there is one on this connector   
                                            return 2  
                                    elif conLine.end_block == self.name: #line ends in this block
                                        if conLine.end_connector == 2: #dont assign a new line if there is one on this connector   
                                            return 2 
                                self.assign_line(touch,self.name,2,self.nParams)                  
                            else: #assign a line as there are none connected to this block
                                self.assign_line(touch,self.name,2,self.nParams)
                        return 2     

            #==============Parameter 1 
            if self.nParams >= 1:                
                if touch.pos[X] > self.param1Con.pos[X] and touch.pos[X] < (self.param1Con.pos[X] + self.param1Con.size[X]):
                    if touch.pos[Y] > self.param1Con.pos[Y] and touch.pos[Y] < (self.param1Con.pos[Y] + self.param1Con.size[Y]):
                        self.selected = RELEASED
                        if allow_assign_line:
                            if self.conLines != []: # if there are conlines
                                for conLine in self.conLines:
                                    if conLine.start_block == self.name: #line starts in this block
                                        if conLine.start_connector == 1: #dont assign a new line if there is one on this connector   
                                            return 1  
                                    elif conLine.end_block == self.name: #line ends in this block
                                        if conLine.end_connector == 1: #dont assign a new line if there is one on this connector   
                                            return 1 
                                self.assign_line(touch,self.name,1,self.nParams)                  
                            else: #assign a line as there are none connected to this block
                                self.assign_line(touch,self.name,1,self.nParams)
                        return 1 

        if self.nParams == MIXER:
            if touch.pos[X] > self.input1.pos[X] and touch.pos[X] < (self.input1.pos[X] + self.input1.size[X]):
                if touch.pos[Y] > self.input1.pos[Y] and touch.pos[Y] < (self.input1.pos[Y] + self.input1.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block == self.name: #line starts in this block
                                    if conLine.start_connector == 21: #dont assign a new line if there is one on this connector   
                                        return 21 
                                elif conLine.end_block == self.name: #line ends in this block
                                    if conLine.end_connector == 21: #dont assign a new line if there is one on this connector   
                                        return 21  
                            self.assign_line(touch,self.name,21,self.nParams)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,self.name,21,self.nParams)
                    return 21

            if touch.pos[X] > self.input2.pos[X] and touch.pos[X] < (self.input2.pos[X] + self.input2.size[X]):
                if touch.pos[Y] > self.input2.pos[Y] and touch.pos[Y] < (self.input2.pos[Y] + self.input2.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block == self.name: #line starts in this block
                                    if conLine.start_connector == 22: #dont assign a new line if there is one on this connector   
                                        return 22
                                elif conLine.end_block == self.name: #line ends in this block
                                    if conLine.end_connector == 22: #dont assign a new line if there is one on this connector   
                                        return 22  
                            self.assign_line(touch,self.name,22,self.nParams)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,self.name,22,self.nParams)
                    return 22
            
            #==============Parameter 2 
            if self.nParams >= 2:                
                if touch.pos[X] > self.param2Con.pos[X] and touch.pos[X] < (self.param2Con.pos[X] + self.param2Con.size[X]):
                    if touch.pos[Y] > self.param2Con.pos[Y] and touch.pos[Y] < (self.param2Con.pos[Y] + self.param2Con.size[Y]):
                        self.selected = RELEASED
                        if allow_assign_line:
                            if self.conLines != []: # if there are conlines
                                for conLine in self.conLines:
                                    if conLine.start_block == self.name: #line starts in this block
                                        if conLine.start_connector == 2: #dont assign a new line if there is one on this connector   
                                            return 2  
                                    elif conLine.end_block == self.name: #line ends in this block
                                        if conLine.end_connector == 2: #dont assign a new line if there is one on this connector   
                                            return 2 
                                self.assign_line(touch,self.name,2,self.nParams)                  
                            else: #assign a line as there are none connected to this block
                                self.assign_line(touch,self.name,2,self.nParams)
                        return 2     

            #==============Parameter 1 
            if self.nParams >= 1:                
                if touch.pos[X] > self.param1Con.pos[X] and touch.pos[X] < (self.param1Con.pos[X] + self.param1Con.size[X]):
                    if touch.pos[Y] > self.param1Con.pos[Y] and touch.pos[Y] < (self.param1Con.pos[Y] + self.param1Con.size[Y]):
                        self.selected = RELEASED
                        if allow_assign_line:
                            if self.conLines != []: # if there are conlines
                                for conLine in self.conLines:
                                    if conLine.start_block == self.name: #line starts in this block
                                        if conLine.start_connector == 1: #dont assign a new line if there is one on this connector   
                                            return 1  
                                    elif conLine.end_block == self.name: #line ends in this block
                                        if conLine.end_connector == 1: #dont assign a new line if there is one on this connector   
                                            return 1 
                                self.assign_line(touch,self.name,1,self.nParams)                  
                            else: #assign a line as there are none connected to this block
                                self.assign_line(touch,self.name,1,self.nParams)
                        return 1 

        if self.nParams <= MAX_PARAMS:
            #==============Parameter 6   
            if self.nParams == 6:
                if touch.pos[X] > self.param6Con.pos[X] and touch.pos[X] < (self.param6Con.pos[X] + self.param6Con.size[X]):
                    if touch.pos[Y] > self.param6Con.pos[Y] and touch.pos[Y] < (self.param6Con.pos[Y] + self.param6Con.size[Y]):
                        self.selected = RELEASED
                        if allow_assign_line:
                            if self.conLines != []: # if there are conlines
                                for conLine in self.conLines:
                                    if conLine.start_block == self.name: #line starts in this block
                                        if conLine.start_connector == 6: #dont assign a new line if there is one on this connector   
                                            return 6  
                                    elif conLine.end_block == self.name: #line ends in this block
                                        if conLine.end_connector == 6: #dont assign a new line if there is one on this connector   
                                            return 6  
                                self.assign_line(touch,self.name,6,self.nParams)                  
                            else: #assign a line as there are none connected to this block
                                self.assign_line(touch,self.name,6,self.nParams)
                        return 6  

            #==============Parameter 5
            if self.nParams >= 5:                
                if touch.pos[X] > self.param5Con.pos[X] and touch.pos[X] < (self.param5Con.pos[X] + self.param5Con.size[X]):
                    if touch.pos[Y] > self.param5Con.pos[Y] and touch.pos[Y] < (self.param5Con.pos[Y] + self.param5Con.size[Y]):
                        self.selected = RELEASED
                        if allow_assign_line:
                            if self.conLines != []: # if there are conlines
                                for conLine in self.conLines:
                                    if conLine.start_block == self.name: #line starts in this block
                                        if conLine.start_connector == 5: #dont assign a new line if there is one on this connector   
                                            return 5  
                                    elif conLine.end_block == self.name: #line ends in this block
                                        if conLine.end_connector == 5: #dont assign a new line if there is one on this connector   
                                            return 5  
                                self.assign_line(touch,self.name,5,self.nParams)                  
                            else: #assign a line as there are none connected to this block
                                self.assign_line(touch,self.name,5,self.nParams)
                        return 5

            #==============Parameter 4              
            if self.nParams >=4:                
                if touch.pos[X] > self.param4Con.pos[X] and touch.pos[X] < (self.param4Con.pos[X] + self.param4Con.size[X]):
                    if touch.pos[Y] > self.param4Con.pos[Y] and touch.pos[Y] < (self.param4Con.pos[Y] + self.param4Con.size[Y]):
                        self.selected = RELEASED
                        if allow_assign_line:
                            if self.conLines != []: # if there are conlines
                                for conLine in self.conLines:
                                    if conLine.start_block == self.name: #line starts in this block
                                        if conLine.start_connector == 4: #dont assign a new line if there is one on this connector   
                                            return 4  
                                    elif conLine.end_block == self.name: #line ends in this block
                                        if conLine.end_connector == 4: #dont assign a new line if there is one on this connector   
                                            return 4  
                                self.assign_line(touch,self.name,4,self.nParams)                  
                            else: #assign a line as there are none connected to this block
                                self.assign_line(touch,self.name,4,self.nParams)
                        return 4

            #==============Parameter 3 
            if self.nParams >= 3:                
                if touch.pos[X] > self.param3Con.pos[X] and touch.pos[X] < (self.param3Con.pos[X] + self.param3Con.size[X]):
                    if touch.pos[Y] > self.param3Con.pos[Y] and touch.pos[Y] < (self.param3Con.pos[Y] + self.param3Con.size[Y]):
                        self.selected = RELEASED
                        if allow_assign_line:
                            if self.conLines != []: # if there are conlines
                                for conLine in self.conLines:
                                    if conLine.start_block == self.name: #line starts in this block
                                        if conLine.start_connector == 3: #dont assign a new line if there is one on this connector   
                                            return 3  
                                    elif conLine.end_block == self.name: #line ends in this block
                                        if conLine.end_connector == 3: #dont assign a new line if there is one on this connector   
                                            return 3 
                                self.assign_line(touch,self.name,3,self.nParams)                  
                            else: #assign a line as there are none connected to this block
                                self.assign_line(touch,self.name,3,self.nParams)
                        return 3 
            
            #==============Parameter 2 
            if self.nParams >= 2:                
                if touch.pos[X] > self.param2Con.pos[X] and touch.pos[X] < (self.param2Con.pos[X] + self.param2Con.size[X]):
                    if touch.pos[Y] > self.param2Con.pos[Y] and touch.pos[Y] < (self.param2Con.pos[Y] + self.param2Con.size[Y]):
                        self.selected = RELEASED
                        if allow_assign_line:
                            if self.conLines != []: # if there are conlines
                                for conLine in self.conLines:
                                    if conLine.start_block == self.name: #line starts in this block
                                        if conLine.start_connector == 2: #dont assign a new line if there is one on this connector   
                                            return 2  
                                    elif conLine.end_block == self.name: #line ends in this block
                                        if conLine.end_connector == 2: #dont assign a new line if there is one on this connector   
                                            return 2 
                                self.assign_line(touch,self.name,2,self.nParams)                  
                            else: #assign a line as there are none connected to this block
                                self.assign_line(touch,self.name,2,self.nParams)
                        return 2     

            #==============Parameter 1 
            if self.nParams >= 1:                
                if touch.pos[X] > self.param1Con.pos[X] and touch.pos[X] < (self.param1Con.pos[X] + self.param1Con.size[X]):
                    if touch.pos[Y] > self.param1Con.pos[Y] and touch.pos[Y] < (self.param1Con.pos[Y] + self.param1Con.size[Y]):
                        self.selected = RELEASED
                        if allow_assign_line:
                            if self.conLines != []: # if there are conlines
                                for conLine in self.conLines:
                                    if conLine.start_block == self.name: #line starts in this block
                                        if conLine.start_connector == 1: #dont assign a new line if there is one on this connector   
                                            return 1  
                                    elif conLine.end_block == self.name: #line ends in this block
                                        if conLine.end_connector == 1: #dont assign a new line if there is one on this connector   
                                            return 1 
                                self.assign_line(touch,self.name,1,self.nParams)                  
                            else: #assign a line as there are none connected to this block
                                self.assign_line(touch,self.name,1,self.nParams)
                        return 1 
        return 0   




    #------------------------------------------- move_block
    def move_block(self,touch,blocks):
        if self.selected == SELECTED:
            if touch.pos[X] > 20:
                if touch.pos[X] + self.rect.size[X] < 1650: 
                    if touch.pos[Y] > 20:
                        if touch.pos[Y] + self.rect.size[Y] < 1000: 
                            if len(blocks) == 1:#if only this block is in the list - move block                    
                                self.rect.pos = touch.pos
                                self.label.pos[X] = touch.pos[X]
                                self.label.pos[Y] = touch.pos[Y] - (self.rect.size[Y]/2)
                                self.move_connectors(touch,1,1)
                                
                            else:  # check for block-block collisions  
                                for secondBlock in blocks:              
                                    if self.label.text != secondBlock.label.text: # dont compare a block with itself
                                        if self.is_collision(secondBlock):
                                            NO_UP = 0
                                            NO_DOWN = 0
                                            NO_LEFT = 0
                                            NO_RIGHT = 0
                                            ALLOW_X = 0
                                            ALLOW_Y = 0
                                            #restrict movement based on relative position of colliding blocks
                                            if self.rect.pos[X] + BLOCK_WIDTH > secondBlock.rect.pos[X] + BLOCK_WIDTH + THRESH:
                                                NO_LEFT = 1
                                            if self.rect.pos[X] < secondBlock.rect.pos[X] - THRESH:
                                                NO_RIGHT = 1
                                            if self.rect.pos[Y] + BLOCK_HEIGHT > secondBlock.rect.pos[Y] + BLOCK_HEIGHT + THRESH:
                                                NO_DOWN = 1
                                            if self.rect.pos[Y] < secondBlock.rect.pos[Y] - THRESH:
                                                NO_UP = 1
                                            #check movement and movement restrictions    
                                            if touch.pos[X] < self.rect.pos[X]: # left movement
                                                if not NO_LEFT:
                                                    ALLOW_X = 1
                                            else: # right movement
                                                if not NO_RIGHT:
                                                    ALLOW_X = 1
                                            if touch.pos[Y] > self.rect.pos[Y]: # up movement
                                                if not NO_UP:
                                                    ALLOW_Y = 1
                                            else: # down movement
                                                if not NO_DOWN:
                                                    ALLOW_Y = 1   
                                            #move the block if allowed
                                            temp = list(self.rect.pos)
                                            if ALLOW_X:
                                                temp[X] = touch.pos[0]
                                                self.label.pos[X] = touch.pos[X]
                                            if ALLOW_Y:
                                                temp[Y] = touch.pos[1]
                                                self.label.pos[Y] = touch.pos[Y] - (self.rect.size[Y]/2)
                                            self.rect.pos = tuple(temp)
                                            self.move_connectors(touch,ALLOW_X,ALLOW_Y)  
                                            return
                                else: # no collisions - move block            
                                    self.rect.pos = touch.pos
                                    self.label.pos[X] = touch.pos[X]
                                    self.label.pos[Y] = touch.pos[Y] - (self.rect.size[Y]/2)
                                    self.move_connectors(touch,1,1)

    #------------------------------------------- release_block
    def release_block(self,touch):
        self.selected = RELEASED 

    #------------------------------------------- is_touch_detected
    def is_touch_detected(self,touch,moving):
        if touch.pos[X] > self.rect.pos[X] and touch.pos[X] < (self.rect.pos[X] + self.rect.size[X]):
            if touch.pos[Y] > self.rect.pos[Y] and touch.pos[Y] < (self.rect.pos[Y] + self.rect.size[Y]):
                if moving == STILL:
                    self.selected = SELECTED
                    self.is_inside_connector(touch,ASSIGN_LINE) #assign a line if inside a connector
                    return 1 
        return 0            
                    
    #------------------------------------------- is_collision
    def is_collision(self,secondBlock):
        if self.rect.pos[X] < secondBlock.rect.pos[X] + BLOCK_WIDTH + THRESH:        
            if self.rect.pos[X] + BLOCK_WIDTH > secondBlock.rect.pos[X] - THRESH:
                if self.rect.pos[Y] < secondBlock.rect.pos[Y] + BLOCK_HEIGHT + THRESH:        
                    if self.rect.pos[Y] + BLOCK_HEIGHT > secondBlock.rect.pos[Y] - THRESH:
                        return COLLISION

                # if self.name is not None:
        #     if self.collide_widget(secondBlock):
        #         return COLLISION
        return NO_COLLISION                

 #------------------------------------------- assign_line
    def assign_line(self,touch, start_block, start_connector,nParams):
        with self.canvas:
            conLine = MyLine(touch,start_block,start_connector,nParams)
            self.conLines.append(conLine)

#========================================================================        
#============================Click=======================================
#========================================================================
class Click(Widget):

    def __init__(self, **kwargs):
        super(Click, self).__init__(**kwargs)

    #-------------------------------------------
    def assign_block(self,name,inputNode,outputNode,nParams):
        with self.canvas:
            nameCounter = 1
            create_block = 0
            temp = name + " " + str(nameCounter)

            if blocks == []:
                block = Block(temp,inputNode,outputNode,nParams)   
                blocks.append(block)
            else:
                while create_block == 0:
                    for block in blocks: 
                        temp = name + " " + str(nameCounter)
                        #if word match 
                        if temp[:-1] == block.label.text[:-1]: 
                            if temp[-1] <= block.label.text[-1]:
                                create_block = 0
                                nameCounter = nameCounter + 1
                            if temp[-1] > block.label.text[-1]:
                                create_block = 1              
                        else:
                            create_block = 1
                block = Block(temp,inputNode,outputNode,nParams)
                blocks.append(block)

    #--------------------------------------------
    def detect_collisions(self, touch, moving):
        for block in blocks:
            if block.is_touch_detected(touch,moving): 
                return TRUE
        return FALSE

    #-------------------------------------------
    def on_touch_down(self, touch):
        if blocks != []:
            for block in blocks:
                if block.conLines != []:
                    for line in block.conLines:   
                        if line.dragging == DRAGGING:
                            line.drag_line(touch,DRAG_MODE0)
                            return #don't check for collision with block if dragging a line
            self.detect_collisions(touch,STILL)

    #-------------------------------------------
    def on_touch_move(self, touch):
        if blocks != []:
            for block in blocks:
                block.move_block(touch,blocks)
                if block.conLines != []:
                    for conLine in block.conLines:
                        if conLine.dragging == DRAGGING:
                            conLine.drag_line(touch,DRAG_MODE0)

    #-------------------------------------------
    def on_touch_up(self,touch):
        for block1 in blocks:
            block1.release_block(touch)
            if block1.conLines != []: #if there are lines 
                for conLine in block1.conLines: 
                    if conLine.dragging == DRAGGING:#letting go of a line that hasn't been linked to end block yet
                        for block2 in blocks: #search through the other blocks to see if end of line (mouse pointer) is inside a connector
                            if block1.name != block2.name: #dont let a block connect to itself
                                newConnector = block2.is_inside_connector(touch,DONT_ASSIGN_LINE) #inside a connector of block 2?
                                if newConnector != 0: #...#yes!
                                    if newConnector is not None:                           #here only allow line to stop dragging if inside a valid connector, which depends on the start connector
                                        if((conLine.start_connector == 10 or conLine.start_connector == 31 or conLine.start_connector == 32) and (newConnector == 11 or newConnector == 21 or newConnector == 22)) or \
                                            ((conLine.start_connector == 11 or conLine.start_connector == 21 or conLine.start_connector == 22) and (newConnector == 10 or newConnector == 31 or newConnector == 32)) or \
                                            (conLine.start_connector <=6 and newConnector == 1 and (block2.inputExists == 0)) or\
                                            (conLine.start_connector == 1 and (block1.inputExists == 0) and newConnector <=6):
                                                if block2.conLines != []: # block2 has lines?
                                                    for conLine2 in block2.conLines:
                                                        if conLine2.start_block == block2.name: #only check the connections that start on block 2
                                                            if conLine2.start_connector == newConnector:
                                                                return #found line that is connected here so break out so cursor keeps hold of line
                                                        elif conLine2.end_block == block2.name:#...or end on block 2 
                                                            if conLine2.end_connector == newConnector:
                                                                return #found line that is connected here so break out so that cursor keeps hold of line              
                                                    conLine.dragging = NOT_DRAGGING
                                                    conLine.end_block=block2.name
                                                    block2.conLines.append(conLine)# add the newly connected line to the list of lines
                                                    conLine.end_connector = newConnector
                                                    conLine.name += (" " + block2.name + " " + str(conLine.end_connector))


                                                else: #block 2 has no lines            
                                                    conLine.dragging = NOT_DRAGGING
                                                    conLine.end_block=block2.name
                                                    block2.conLines.append(conLine)# add the newly connected line to the list of lines
                                                    conLine.end_connector = newConnector
                                                    conLine.name += (" " + block2.name + " " + str(conLine.end_connector))
                                                    break                

#========================================================================        
#============================overlaySquare===============================
#========================================================================
# class overlaySquare(Widget):
#     def __init__(self, conPos, **kwargs):
#         super(overlaySquare, self).__init__(**kwargs)
#         with self.canvas:
#             Color(0.4,0.0,0.0,OPAQUE, mode="rgba")
#             self.rect = Rectangle(pos = (conPos[X],conPos[Y]), size=(100,100))


#========================================================================        
#==============================myMousePos================================
#========================================================================
class myMousePos():
    def __init__(self, **kwargs):
        super(myMousePos, self).__init__(**kwargs)
        self.pos = []

    def assign_pos(self,pos):    
        self.pos = pos
        

#========================================================================        
#===========================FXCoreDesignerApp============================
#========================================================================
class FXCoreDesignerApp(App):

    def build(self):
        
        #self.isOverlay = 0
        Window.size = (1920, 1080)
        #Window.fullscreen = 'auto'
        Window.bind(mouse_pos=self.on_mouse_pos)

        self.my_mouse_pos = myMousePos();    

        click = Click() 
        layout = GridLayout(cols = 9, row_force_default = True, row_default_height = BUTTON_HEIGHT)
        
        #--------------------------------IOdrop
        IOdrop = DropDown()
        #
        inBtn = Button(text ='Input', size_hint_y = None, height = BUTTON_HEIGHT)
        inBtn.bind(on_release = lambda none: click.assign_block('Input',0,1,0))
        IOdrop.add_widget(inBtn)
        #
        outBtn = Button(text ='Output', size_hint_y = None, height = BUTTON_HEIGHT)
        outBtn.bind(on_release = lambda none: click.assign_block('Output',1,0,0))
        IOdrop.add_widget(outBtn)
        
        #--------------------------------FXdrop
        FXdrop = DropDown()
        #
        reverbBtn = Button(text ='Reverb', size_hint_y = None, height = BUTTON_HEIGHT)
        reverbBtn.bind(on_release = lambda none: click.assign_block('Reverb',1,1,6))
        FXdrop.add_widget(reverbBtn)
        #
        delayBtn = Button(text ='Delay', size_hint_y = None, height = BUTTON_HEIGHT)
        delayBtn.bind(on_release = lambda none: click.assign_block('Delay',1,1,5))
        FXdrop.add_widget(delayBtn)
        #Chorus
        chorusBtn = Button(text ='Chorus', size_hint_y = None, height = BUTTON_HEIGHT)
        chorusBtn.bind(on_release = lambda none: click.assign_block('Chorus',1,1,4))
        FXdrop.add_widget(chorusBtn)
        #Tremelo
        tremoloBtn = Button(text ='Tremelo', size_hint_y = None, height = BUTTON_HEIGHT)
        tremoloBtn.bind(on_release = lambda none: click.assign_block('Tremelo',1,1,3))
        FXdrop.add_widget(tremoloBtn)

        #--------------------------------AnalysisDrop
        AnalysisDrop = DropDown()
        #
        FFTBtn = Button(text ='FFT', size_hint_y = None, height = BUTTON_HEIGHT)
        FFTBtn.bind(on_release = lambda  none: click.assign_block('FFT',1,1,2))
        AnalysisDrop.add_widget(FFTBtn)
        #
        envelopeFollowerBtn = Button(text ='Envelope', size_hint_y = None, height = BUTTON_HEIGHT)
        envelopeFollowerBtn.bind(on_release = lambda  none: click.assign_block('Envelope',1,1,1))
        AnalysisDrop.add_widget(envelopeFollowerBtn)
        
        #--------------------------------ControlsDrop
        ControlsDrop = DropDown()
        # 
        PotentiomenterBtn = Button(text ='Potentiometer', size_hint_y = None, height = BUTTON_HEIGHT)
        PotentiomenterBtn.bind(on_release = lambda  none: click.assign_block('Pot',0,0,1))
        ControlsDrop.add_widget(PotentiomenterBtn)
        #
        ConstantBtn = Button(text ='Constant', size_hint_y = None, height = BUTTON_HEIGHT)
        ConstantBtn.bind(on_release = lambda  none: click.assign_block('Constant',0,0,1))
        ControlsDrop.add_widget(ConstantBtn)

        #--------------------------------Routingdrop
        #Routingdrop = DropDown()
        #
        splitterBtn = Button(text ='Splitter', size_hint_y = None, height = BUTTON_HEIGHT)
        splitterBtn.bind(on_release = lambda none: click.assign_block('Splitter',1,0,SPLITTER))
        #Routingdrop.add_widget(splitterBtn)temp fix
        #
        mixerBtn = Button(text ='Mixer', size_hint_y = None, height = BUTTON_HEIGHT)
        mixerBtn.bind(on_release = lambda none: click.assign_block('Mixer',0,1,MIXER))
        #Routingdrop.add_widget(mixerBtn)temp fix
        
        #--------------------------------
        IObutton = Button(text ='IO')
        IObutton.bind(on_release = IOdrop.open)

        FXbutton = Button(text ='FX')
        FXbutton.bind(on_release = FXdrop.open)

        AnalysisButton = Button(text ='Analysis')
        AnalysisButton.bind(on_release = AnalysisDrop.open)

        ControlsButton = Button(text ='Controls')
        ControlsButton.bind(on_release = ControlsDrop.open)

        # RoutingButton = Button(text ='Routing')
        # RoutingButton.bind(on_release = Routingdrop.open)

         #--------------------------------
        CodeButton = Button(text ='Generate Code')
        CodeButton.bind(on_release =  lambda none: self.printLines())

        #--------------------------------
        ClearButton = Button(text ='Clear Screen')
        #ClearButton.bind(on_release = 
        
        #--------------------------------
        AboutButton = Button(text ='About')
        popup = Popup(title='FXCore Designer',
            content=Label(text='Instructions:'),
            size_hint=(None, None), size=(400, 400))

        AboutButton.bind(on_release = lambda none: popup.open())


        layout.add_widget(IObutton)
        layout.add_widget(FXbutton)
        layout.add_widget(AnalysisButton)
        layout.add_widget(ControlsButton)
       #layout.add_widget(RoutingButton)
        layout.add_widget(splitterBtn)#temp fix for RoutingButton failing to open if another block...
        layout.add_widget(mixerBtn)#... is generated from another dropdown before a block from RoutingButton
        layout.add_widget(CodeButton)
        layout.add_widget(ClearButton)
        layout.add_widget(AboutButton)
        layout.add_widget(click)
    
        return layout


  #------------------------------------------- mouse hover event
    def on_mouse_pos(self, window, pos):
        if blocks is not None:
            for block in blocks:
                if block.conLines is not None:
                    for conLine in block.conLines:
                        if conLine.dragging == DRAGGING:# when first dragging the line keep hold of it until clicked in block or deleted
                            conLine.drag_line(pos,DRAG_MODE1)

                            ##todo highlight connector when hovered over
                # self.my_mouse_pos.assign_pos(pos)
                # newConnector = block.is_inside_connector(self.my_mouse_pos,DONT_ASSIGN_LINE)
                # if newConnector != 0:
                #     print(newConnector)
                #     if newConnector == 11:
                #         if self.isOverlay == 0:
                #             overlay_square = overlaySquare(block.input.pos)
                #             self.isOverlay = 1
                #             layout.add_widget(click)
                #     elif isOverlay == 1:
                #         overlay_square.__del__()
                #         isOverlay = 0

    #-------------------------------------------
    def printLines(self):
        print("Code Generating...")
        for block in blocks:
            if block.conLines != []:
                for conLine in block.conLines:
                    if conLine.end_block != block.name:
                        print(block.name, conLine.start_connector, conLine.end_connector, conLine.end_block)


if __name__ == '__main__':
    FXCoreDesignerApp().run()


   