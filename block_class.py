from kivy.uix.button import Label
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from line_class import MyLine
from asm_node_class import asm_node
from config import blocks
import random

COLLISION = 1
NO_COLLISION = 0

SELECTED = 1 
RELEASED = 0

DRAGGING = 1
NOT_DRAGGING = 0

BLOCK_WIDTH = 100 
BLOCK_HEIGHT = 50

OPAQUE = 1 

MIXER = 20
SPLITTER = 30

INPUT = 11
OUTPUT = 10

MAX_PARAMS = 6

MOVING = 1
STILL = 0

DONT_ASSIGN_LINE = 0
ASSIGN_LINE = 1

X = 0
Y = 1 

THRESH = 20

class Block(Widget):
    def __init__(self,name,nameID,inputConnector,outputConnector,nParams, **kwargs):
        super(Block, self).__init__(**kwargs)     
        self.name = name
        self.ID = nameID
        self.Xpos = random.randrange(100, 1500)
        self.Ypos = random.randrange(100, 800)
        self.selected = RELEASED
        self.nParams = nParams
        self.paramCons = []
        self.conLines = []
        self.inputExists = 0 
        self.outputExists = 0
        self.usageState = 0
        self.constant = 0
        with self.canvas:
            Color(0.4,0.4,0.4,OPAQUE, mode="rgba")

            self.rect = Rectangle(pos=(self.Xpos,self.Ypos), size=(BLOCK_WIDTH,BLOCK_HEIGHT))
            self.label = Label(pos=(self.Xpos, self.Ypos - (self.rect.size[Y]/2)),text=name)

       
            if inputConnector: 
                Color(0,0.5,1,OPAQUE, mode="rgba")
                self.input = Rectangle(pos=(self.Xpos,self.Ypos+20), size=(10,10))
                self.inputExists = True

            if outputConnector: 
                Color(0,0.5,1,OPAQUE, mode="rgba")
                self.output = Rectangle(pos=(self.Xpos+90,self.Ypos+20), size=(10,10))
                self.outputExists = True

            if self.nParams == SPLITTER: 
                Color(0,0.5,1,OPAQUE, mode="rgba")
                self.output1 = Rectangle(pos=(self.Xpos+90,self.Ypos+30), size=(10,10))
                self.output2 = Rectangle(pos=(self.Xpos+90,self.Ypos+10), size=(10,10))

            elif self.nParams == MIXER: 
                Color(0,0.5,1,OPAQUE, mode="rgba")
                self.input1 = Rectangle(pos=(self.Xpos,self.Ypos+30), size=(10,10))
                self.input2 = Rectangle(pos=(self.Xpos,self.Ypos+10), size=(10,10))
                Color(0.5,0,1,OPAQUE, mode="rgba")
                self.param1Con = Rectangle(pos=(self.Xpos+30,self.Ypos+40), size=(10,10))
                self.param2Con = Rectangle(pos=(self.Xpos+60,self.Ypos+40), size=(10,10))

            elif self.nParams == 6:  
                Color(0.5,0,1,OPAQUE, mode="rgba")
                self.param1Con = Rectangle(pos=(self.Xpos+15,self.Ypos+40), size=(10,10))
                self.param2Con = Rectangle(pos=(self.Xpos+45,self.Ypos+40), size=(10,10))
                self.param3Con = Rectangle(pos=(self.Xpos+75,self.Ypos+40), size=(10,10))
                self.param4Con = Rectangle(pos=(self.Xpos+15,self.Ypos), size=(10,10))
                self.param5Con = Rectangle(pos=(self.Xpos+45,self.Ypos), size=(10,10))
                self.param6Con = Rectangle(pos=(self.Xpos+75,self.Ypos), size=(10,10))         

            elif self.nParams == 5:
                Color(0.5,0,1,OPAQUE, mode="rgba")
                self.param1Con = Rectangle(pos=(self.Xpos+15,self.Ypos+40), size=(10,10))
                self.param2Con = Rectangle(pos=(self.Xpos+45,self.Ypos+40), size=(10,10))
                self.param3Con = Rectangle(pos=(self.Xpos+75,self.Ypos+40), size=(10,10))
                self.param4Con = Rectangle(pos=(self.Xpos+30,self.Ypos), size=(10,10))
                self.param5Con = Rectangle(pos=(self.Xpos+60,self.Ypos), size=(10,10))

            elif self.nParams == 4: 
                Color(0.5,0,1,OPAQUE, mode="rgba")
                self.param1Con = Rectangle(pos=(self.Xpos+30,self.Ypos+40), size=(10,10))
                self.param2Con = Rectangle(pos=(self.Xpos+60,self.Ypos+40), size=(10,10))
                self.param3Con = Rectangle(pos=(self.Xpos+30,self.Ypos), size=(10,10))
                self.param4Con = Rectangle(pos=(self.Xpos+60,self.Ypos), size=(10,10))

            elif self.nParams == 3:
                Color(0.5,0,1,OPAQUE, mode="rgba")
                self.param1Con = Rectangle(pos=(self.Xpos+30,self.Ypos+40), size=(10,10))
                self.param2Con = Rectangle(pos=(self.Xpos+60,self.Ypos+40), size=(10,10))
                self.param3Con = Rectangle(pos=(self.Xpos+45,self.Ypos), size=(10,10))

            elif self.nParams == 2:
                Color(0.5,0,1,OPAQUE, mode="rgba")
                self.param1Con = Rectangle(pos=(self.Xpos+30,self.Ypos+40), size=(10,10))
                self.param2Con = Rectangle(pos=(self.Xpos+60,self.Ypos+40), size=(10,10))

            elif self.nParams == 1:
                Color(0.5,0,1,OPAQUE, mode="rgba")
                if self.outputExists:
                    self.param1Con = Rectangle(pos=(self.Xpos+45,self.Ypos+40), size=(10,10))
                else: # if a potentiometer or constant block
                    self.param1Con = Rectangle(pos=(self.Xpos+45,self.Ypos+0), size=(10,10))

                    
    #-------------------------------------------
    def get_connector_name(self,connector):
        if connector == OUTPUT:
            return 'Output'

        if connector == INPUT:
            return 'Input'
            
        if connector == MIXER + 1:
            return 'Input 1'
        if connector == MIXER + 2:
            return 'Input 2'   

        if connector == SPLITTER + 1:
            return 'Output 1'
        if connector == SPLITTER + 2:
            return 'Output 2'   
        else:
            temp_node = asm_node(self)
            return temp_node.get_connector_name(connector)


    #-------------------------------------------
    def remove_block(self):
        with self.canvas:
            self.canvas.remove(self.rect)
            self.label.text = ""
            if self.inputExists:
                self.canvas.remove(self.input)
            if self.outputExists: 
                self.canvas.remove(self.output)                
            if self.nParams == SPLITTER:
                self.canvas.remove(self.output1)      
                self.canvas.remove(self.output2)  
            elif self.nParams == MIXER:
                self.canvas.remove(self.input1)      
                self.canvas.remove(self.input2)  
                self.canvas.remove(self.param1Con)
                self.canvas.remove(self.param2Con)
            elif self.nParams == 6:
                self.canvas.remove(self.param1Con)
                self.canvas.remove(self.param2Con)
                self.canvas.remove(self.param3Con)
                self.canvas.remove(self.param4Con)
                self.canvas.remove(self.param5Con)
                self.canvas.remove(self.param6Con)
            elif self.nParams == 5:
                self.canvas.remove(self.param1Con)
                self.canvas.remove(self.param2Con)
                self.canvas.remove(self.param3Con)
                self.canvas.remove(self.param4Con)
                self.canvas.remove(self.param5Con)
            elif self.nParams == 4:                
                self.canvas.remove(self.param1Con)
                self.canvas.remove(self.param2Con)
                self.canvas.remove(self.param3Con)
                self.canvas.remove(self.param4Con)
            elif self.nParams == 3:
                self.canvas.remove(self.param1Con)
                self.canvas.remove(self.param2Con)
                self.canvas.remove(self.param3Con)
            elif self.nParams == 2:
                self.canvas.remove(self.param1Con)
                self.canvas.remove(self.param2Con)
            elif self.nParams == 1:
                self.canvas.remove(self.param1Con)
            self.canvas.ask_update()

    #------------------------------------------- move_block
    def move_block(self,touch):
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
    def assign_line(self,touch, start_connector):
        with self.canvas:
            conLine = MyLine(touch,self,start_connector)
            self.conLines.append(conLine)


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
                if conLine.start_block.name == self.name:
                    conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 10:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == 10:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.output.pos = tuple(temp)
        
        #========================================Splitter
        if self.nParams == SPLITTER: 
            #**********************************output 1
            temp = list(self.output1.pos)
            if moveX:
                temp[X] = touch.pos[0] + 90
            if moveY:
                temp[Y] = touch.pos[1] + 30
            for conLine in self.conLines: #move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 31:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 32:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 21:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 22:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 3:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 4:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 5:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 6:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 3:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 4:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 5:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 3:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 4:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 3:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
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
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == 11: #dont assign a new line if there is one on this connector   
                                        return 11 
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == 11: #dont assign a new line if there is one on this connector   
                                        return 11  
                            self.assign_line(touch,11)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,11)
                    return 11  
        #============================================
        if self.outputExists:
            if touch.pos[X] > self.output.pos[X] and touch.pos[X] < (self.output.pos[X] + self.output.size[X]):
                if touch.pos[Y] > self.output.pos[Y] and touch.pos[Y] < (self.output.pos[Y] + self.output.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == 10: #dont assign a new line if there is one on this connector   
                                        return 10  
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == 10: #dont assign a new line if there is one on this connector   
                                        return 10  
                            self.assign_line(touch,10)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,10)
                    return 10  
        #============================================SPLITTER
        if self.nParams == SPLITTER:
            if touch.pos[X] > self.output1.pos[X] and touch.pos[X] < (self.output1.pos[X] + self.output1.size[X]):
                if touch.pos[Y] > self.output1.pos[Y] and touch.pos[Y] < (self.output1.pos[Y] + self.output1.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == SPLITTER+1: #dont assign a new line if there is one on this connector   
                                        return SPLITTER+1  
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == SPLITTER+1: #dont assign a new line if there is one on this connector   
                                        return SPLITTER+1  
                            self.assign_line(touch,SPLITTER+1)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,SPLITTER+1)
                    return SPLITTER+1

            if touch.pos[X] > self.output2.pos[X] and touch.pos[X] < (self.output2.pos[X] + self.output2.size[X]):
                if touch.pos[Y] > self.output2.pos[Y] and touch.pos[Y] < (self.output2.pos[Y] + self.output2.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == SPLITTER+2: #dont assign a new line if there is one on this connector   
                                        return SPLITTER+2 
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == SPLITTER+2: #dont assign a new line if there is one on this connector   
                                        return SPLITTER+2  
                            self.assign_line(touch,SPLITTER+2)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,SPLITTER+2)
                    return SPLITTER+2      
            
        #============================================MIXER
        if self.nParams == MIXER:
            if touch.pos[X] > self.input1.pos[X] and touch.pos[X] < (self.input1.pos[X] + self.input1.size[X]):
                if touch.pos[Y] > self.input1.pos[Y] and touch.pos[Y] < (self.input1.pos[Y] + self.input1.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == 21: #dont assign a new line if there is one on this connector   
                                        return 21 
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == 21: #dont assign a new line if there is one on this connector   
                                        return 21  
                            self.assign_line(touch,21)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,21)
                    return 21

            if touch.pos[X] > self.input2.pos[X] and touch.pos[X] < (self.input2.pos[X] + self.input2.size[X]):
                if touch.pos[Y] > self.input2.pos[Y] and touch.pos[Y] < (self.input2.pos[Y] + self.input2.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == 22: #dont assign a new line if there is one on this connector   
                                        return 22
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == 22: #dont assign a new line if there is one on this connector   
                                        return 22  
                            self.assign_line(touch,22)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,22)
                    return 22
            
            #==============Parameter 2 
            if self.nParams >= 2:                
                if touch.pos[X] > self.param2Con.pos[X] and touch.pos[X] < (self.param2Con.pos[X] + self.param2Con.size[X]):
                    if touch.pos[Y] > self.param2Con.pos[Y] and touch.pos[Y] < (self.param2Con.pos[Y] + self.param2Con.size[Y]):
                        self.selected = RELEASED
                        if allow_assign_line:
                            if self.conLines != []: # if there are conlines
                                for conLine in self.conLines:
                                    if conLine.start_block.name == self.name: #line starts in this block
                                        if conLine.start_connector == 2: #dont assign a new line if there is one on this connector   
                                            return 2  
                                    elif conLine.end_block.name == self.name: #line ends in this block
                                        if conLine.end_connector == 2: #dont assign a new line if there is one on this connector   
                                            return 2 
                                self.assign_line(touch,2)                  
                            else: #assign a line as there are none connected to this block
                                self.assign_line(touch,2)
                        return 2     

            #==============Parameter 1 
            if self.nParams >= 1:                
                if touch.pos[X] > self.param1Con.pos[X] and touch.pos[X] < (self.param1Con.pos[X] + self.param1Con.size[X]):
                    if touch.pos[Y] > self.param1Con.pos[Y] and touch.pos[Y] < (self.param1Con.pos[Y] + self.param1Con.size[Y]):
                        self.selected = RELEASED
                        if allow_assign_line:
                            if self.conLines != []: # if there are conlines
                                for conLine in self.conLines:
                                    if conLine.start_block.name == self.name: #line starts in this block
                                        if conLine.start_connector == 1: #dont assign a new line if there is one on this connector   
                                            return 1  
                                    elif conLine.end_block.name == self.name: #line ends in this block
                                        if conLine.end_connector == 1: #dont assign a new line if there is one on this connector   
                                            return 1 
                                self.assign_line(touch,1)                  
                            else: #assign a line as there are none connected to this block
                                self.assign_line(touch,1)
                        return 1 

        #======================================================================== Other Blocks
        if self.nParams <= MAX_PARAMS:
            #==============Parameter 6   
            if self.nParams == 6:
                if touch.pos[X] > self.param6Con.pos[X] and touch.pos[X] < (self.param6Con.pos[X] + self.param6Con.size[X]):
                    if touch.pos[Y] > self.param6Con.pos[Y] and touch.pos[Y] < (self.param6Con.pos[Y] + self.param6Con.size[Y]):
                        self.selected = RELEASED
                        if allow_assign_line:
                            if self.conLines != []: # if there are conlines
                                for conLine in self.conLines:
                                    if conLine.start_block.name == self.name: #line starts in this block
                                        if conLine.start_connector == 6: #dont assign a new line if there is one on this connector   
                                            return 6  
                                    elif conLine.end_block.name == self.name: #line ends in this block
                                        if conLine.end_connector == 6: #dont assign a new line if there is one on this connector   
                                            return 6  
                                self.assign_line(touch,6)                  
                            else: #assign a line as there are none connected to this block
                                self.assign_line(touch,6)
                        return 6  

            #==============Parameter 5
            if self.nParams >= 5:                
                if touch.pos[X] > self.param5Con.pos[X] and touch.pos[X] < (self.param5Con.pos[X] + self.param5Con.size[X]):
                    if touch.pos[Y] > self.param5Con.pos[Y] and touch.pos[Y] < (self.param5Con.pos[Y] + self.param5Con.size[Y]):
                        self.selected = RELEASED
                        if allow_assign_line:
                            if self.conLines != []: # if there are conlines
                                for conLine in self.conLines:
                                    if conLine.start_block.name == self.name: #line starts in this block
                                        if conLine.start_connector == 5: #dont assign a new line if there is one on this connector   
                                            return 5  
                                    elif conLine.end_block.name == self.name: #line ends in this block
                                        if conLine.end_connector == 5: #dont assign a new line if there is one on this connector   
                                            return 5  
                                self.assign_line(touch,5)                  
                            else: #assign a line as there are none connected to this block
                                self.assign_line(touch,5)
                        return 5

            #==============Parameter 4              
            if self.nParams >=4:                
                if touch.pos[X] > self.param4Con.pos[X] and touch.pos[X] < (self.param4Con.pos[X] + self.param4Con.size[X]):
                    if touch.pos[Y] > self.param4Con.pos[Y] and touch.pos[Y] < (self.param4Con.pos[Y] + self.param4Con.size[Y]):
                        self.selected = RELEASED
                        if allow_assign_line:
                            if self.conLines != []: # if there are conlines
                                for conLine in self.conLines:
                                    if conLine.start_block.name == self.name: #line starts in this block
                                        if conLine.start_connector == 4: #dont assign a new line if there is one on this connector   
                                            return 4  
                                    elif conLine.end_block.name == self.name: #line ends in this block
                                        if conLine.end_connector == 4: #dont assign a new line if there is one on this connector   
                                            return 4  
                                self.assign_line(touch,4)                  
                            else: #assign a line as there are none connected to this block
                                self.assign_line(touch,4)
                        return 4

            #==============Parameter 3 
            if self.nParams >= 3:                
                if touch.pos[X] > self.param3Con.pos[X] and touch.pos[X] < (self.param3Con.pos[X] + self.param3Con.size[X]):
                    if touch.pos[Y] > self.param3Con.pos[Y] and touch.pos[Y] < (self.param3Con.pos[Y] + self.param3Con.size[Y]):
                        self.selected = RELEASED
                        if allow_assign_line:
                            if self.conLines != []: # if there are conlines
                                for conLine in self.conLines:
                                    if conLine.start_block.name == self.name: #line starts in this block
                                        if conLine.start_connector == 3: #dont assign a new line if there is one on this connector   
                                            return 3  
                                    elif conLine.end_block.name == self.name: #line ends in this block
                                        if conLine.end_connector == 3: #dont assign a new line if there is one on this connector   
                                            return 3 
                                self.assign_line(touch,3)                  
                            else: #assign a line as there are none connected to this block
                                self.assign_line(touch,3)
                        return 3 
            
            #==============Parameter 2 
            if self.nParams >= 2:                
                if touch.pos[X] > self.param2Con.pos[X] and touch.pos[X] < (self.param2Con.pos[X] + self.param2Con.size[X]):
                    if touch.pos[Y] > self.param2Con.pos[Y] and touch.pos[Y] < (self.param2Con.pos[Y] + self.param2Con.size[Y]):
                        self.selected = RELEASED
                        if allow_assign_line:
                            if self.conLines != []: # if there are conlines
                                for conLine in self.conLines:
                                    if conLine.start_block.name == self.name: #line starts in this block
                                        if conLine.start_connector == 2: #dont assign a new line if there is one on this connector   
                                            return 2  
                                    elif conLine.end_block.name == self.name: #line ends in this block
                                        if conLine.end_connector == 2: #dont assign a new line if there is one on this connector   
                                            return 2 
                                self.assign_line(touch,2)                  
                            else: #assign a line as there are none connected to this block
                                self.assign_line(touch,2)
                        return 2     

            #==============Parameter 1 
            if self.nParams >= 1:                
                if touch.pos[X] > self.param1Con.pos[X] and touch.pos[X] < (self.param1Con.pos[X] + self.param1Con.size[X]):
                    if touch.pos[Y] > self.param1Con.pos[Y] and touch.pos[Y] < (self.param1Con.pos[Y] + self.param1Con.size[Y]):
                        self.selected = RELEASED
                        if allow_assign_line:
                            if self.conLines != []: # if there are conlines
                                for conLine in self.conLines:
                                    if conLine.start_block.name == self.name: #line starts in this block
                                        if conLine.start_connector == 1: #dont assign a new line if there is one on this connector   
                                            return 1  
                                    elif conLine.end_block.name == self.name: #line ends in this block
                                        if conLine.end_connector == 1: #dont assign a new line if there is one on this connector   
                                            return 1 
                                self.assign_line(touch,1)                  
                            else: #assign a line as there are none connected to this block
                                self.assign_line(touch,1)
                        return 1 
        return 0   
