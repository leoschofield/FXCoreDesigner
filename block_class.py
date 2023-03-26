import random
from kivy.uix.button import Label
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from line_class import MyLine
from asm_node_class import asm_node
from config import *


class Block(Widget):
    def __init__(self,name,nameID,inputConnector,outputConnector,nParams,nUsers,nSwitches,tapSwitch, **kwargs):
        super(Block, self).__init__(**kwargs)     
        self.name = name
        self.ID = nameID
        self.Xpos = random.randrange(200, 1400)
        self.Ypos = random.randrange(100, 800)
        self.selected = RELEASED
        self.inputConnector = inputConnector
        self.outputConnector = outputConnector
        self.nParams = nParams
        self.nUserOuts = nUsers
        self.nSwitches = nSwitches
        self.tapSwitch = tapSwitch
        self.paramCons = []
        self.conLines = []
        self.usageState = 0
        self.valOut = None # control block connectors
        self.tapOut = None
        self.switchOut = None
        self.userOut = None

        with self.canvas:
            #----------------------------------------------------------------------------
            if "Tap Tempo" in self.name:
                Color(0.4,0.4,0.4,OPAQUE, mode="rgba")
                self.rect = Rectangle(pos=(self.Xpos,self.Ypos), size=(SMALL_BLOCK_WIDTH,SMALL_BLOCK_HEIGHT))
                self.label = Label(pos=(self.Xpos, self.Ypos - (self.rect.size[Y]/2)),text=name)
                Color(1.0,0.0,0.0,OPAQUE, mode="rgba")
                self.tapOut = Rectangle(pos=(self.Xpos+45,self.Ypos+40), size=(10,10))
                return

            #----------------------------------------------------------------------------    
            if "Switch" in self.name:
                Color(0.4,0.4,0.4,OPAQUE, mode="rgba")
                self.rect = Rectangle(pos=(self.Xpos,self.Ypos), size=(SMALL_BLOCK_WIDTH,SMALL_BLOCK_HEIGHT))
                self.label = Label(pos=(self.Xpos, self.Ypos - (self.rect.size[Y]/2)),text=name)
                Color(1.0,0.5,0.0,OPAQUE, mode="rgba")
                self.switchOut = Rectangle(pos=(self.Xpos+45,self.Ypos+40), size=(10,10))
                return
            
            #----------------------------------------------------------------------------
            if "Constant" in self.name or "Pot" in self.name:
                self.constant = 0.5   
                Color(0.4,0.4,0.4,OPAQUE, mode="rgba")
                self.rect = Rectangle(pos=(self.Xpos,self.Ypos), size=(SMALL_BLOCK_WIDTH,SMALL_BLOCK_HEIGHT))
                self.label = Label(pos=(self.Xpos, self.Ypos - (self.rect.size[Y]/2)),text=name)
                Color(0.5,0.0,1.0,OPAQUE, mode="rgba")
                self.valOut = Rectangle(pos=(self.Xpos+45,self.Ypos), size=(10,10))
                return

            #----------------------------------------------------------------------------
            if "User" in self.name:
                Color(0.4,0.4,0.4,OPAQUE, mode="rgba")
                self.rect = Rectangle(pos=(self.Xpos,self.Ypos), size=(SMALL_BLOCK_WIDTH,SMALL_BLOCK_HEIGHT))
                self.label = Label(pos=(self.Xpos, self.Ypos - (self.rect.size[Y]/2)),text=name)
                Color(0.0,1.0,0.0,OPAQUE, mode="rgba")
                self.userOut = Rectangle(pos=(self.Xpos,self.Ypos+20), size=(10,10))
                return
            
            #----------------------------------------------------------------------------
            if "Output" in self.name:
                Color(0.4,0.4,0.4,OPAQUE, mode="rgba")
                self.rect = Rectangle(pos=(self.Xpos,self.Ypos), size=(SMALL_BLOCK_WIDTH,SMALL_BLOCK_HEIGHT))
                self.label = Label(pos=(self.Xpos, self.Ypos - (self.rect.size[Y]/2)),text=name)
                Color(0,0.5,1,OPAQUE, mode="rgba")
                self.input = Rectangle(pos=(self.Xpos,self.Ypos+20), size=(10,10))
                return
            
            #----------------------------------------------------------------------------
            if "Input" in self.name:
                Color(0.4,0.4,0.4,OPAQUE, mode="rgba")
                self.rect = Rectangle(pos=(self.Xpos,self.Ypos), size=(SMALL_BLOCK_WIDTH,SMALL_BLOCK_HEIGHT))
                self.label = Label(pos=(self.Xpos, self.Ypos - (self.rect.size[Y]/2)),text=name)

                Color(0,0.5,1,OPAQUE, mode="rgba")
                self.output = Rectangle(pos=(self.Xpos+90,self.Ypos+20), size=(10,10))
                return
            
            #----------------------------------------------------------------------------
            if "Envelope" in self.name:
                Color(0.4,0.4,0.4,OPAQUE, mode="rgba")
                self.rect = Rectangle(pos=(self.Xpos,self.Ypos), size=(SMALL_BLOCK_WIDTH,SMALL_BLOCK_HEIGHT))
                self.label = Label(pos=(self.Xpos, self.Ypos - (self.rect.size[Y]/2)),text=name)
                
                Color(0,0.5,1.0,OPAQUE, mode="rgba")
                self.input = Rectangle(pos=(self.Xpos,self.Ypos+20), size=(10,10))
                self.output = Rectangle(pos=(self.Xpos+90,self.Ypos+20), size=(10,10))
                
                Color(0.5,0.0,1.0,OPAQUE, mode="rgba")
                self.valOut = Rectangle(pos=(self.Xpos+45,self.Ypos), size=(10,10))
                return
            
            #----------------------------------------------------------------------------
            if "Splitter" in self.name:
                Color(0.4,0.4,0.4,OPAQUE, mode="rgba")
                self.rect = Rectangle(pos=(self.Xpos,self.Ypos), size=(SMALL_BLOCK_WIDTH,SMALL_BLOCK_HEIGHT))
                self.label = Label(pos=(self.Xpos, self.Ypos - (self.rect.size[Y]/2)),text=name)

                Color(0,0.5,1,OPAQUE, mode="rgba")
                self.output1 = Rectangle(pos=(self.Xpos+90,self.Ypos+30), size=(10,10))
                self.output2 = Rectangle(pos=(self.Xpos+90,self.Ypos+10), size=(10,10))

                self.input = Rectangle(pos=(self.Xpos,self.Ypos+20), size=(10,10))
                return
            
            #----------------------------------------------------------------------------
            if "Mixer" in self.name: 
                Color(0.4,0.4,0.4,OPAQUE, mode="rgba")
                self.rect = Rectangle(pos=(self.Xpos,self.Ypos), size=(SMALL_BLOCK_WIDTH,SMALL_BLOCK_HEIGHT))
                self.label = Label(pos=(self.Xpos, self.Ypos - (self.rect.size[Y]/2)),text=name)

                Color(0,0.5,1,OPAQUE, mode="rgba")
                self.input1 = Rectangle(pos=(self.Xpos,self.Ypos+30), size=(10,10))
                self.input2 = Rectangle(pos=(self.Xpos,self.Ypos+10), size=(10,10))
                self.output = Rectangle(pos=(self.Xpos+90,self.Ypos+20), size=(10,10))

                Color(0.5,0,1,OPAQUE, mode="rgba")
                self.param1Con = Rectangle(pos=(self.Xpos+30,self.Ypos+40), size=(10,10))
                self.param2Con = Rectangle(pos=(self.Xpos+60,self.Ypos+40), size=(10,10))
                return
            
            #============================================================================================
            Color(0.4,0.4,0.4,OPAQUE, mode="rgba")   
            self.rect = Rectangle(pos=(self.Xpos,self.Ypos), size=(BLOCK_WIDTH,BLOCK_HEIGHT))
            self.label = Label(pos=(self.Xpos + 15, self.Ypos-5),text=name)

            #----------------------------------------------------------------------------
            if inputConnector:   
                Color(0,0.5,1,OPAQUE, mode="rgba")
                self.input = Rectangle(pos=(self.Xpos,self.Ypos+40), size=(10,10))

            #----------------------------------------------------------------------------
            if outputConnector: 
                Color(0,0.5,1,OPAQUE, mode="rgba")
                self.output = Rectangle(pos=(self.Xpos+120,self.Ypos+40), size=(10,10))

            #----------------------------------------------------------------------------    
            if self.nUserOuts == 2:
                Color(0.0,1.0,0.0,OPAQUE, mode="rgba")
                self.user1Con = Rectangle(pos=(self.Xpos+120,self.Ypos+10), size=(10,10))
                
            if self.nUserOuts >= 1:
                Color(0.0,1.0,0.0,OPAQUE, mode="rgba")
                self.user0Con = Rectangle(pos=(self.Xpos+120,self.Ypos+70), size=(10,10))  

            #----------------------------------------------------------------------------
            if self.tapSwitch:
                Color(1.0,0.0,0.0,OPAQUE, mode="rgba") 
                self.tapCon = Rectangle(pos=(self.Xpos+10,self.Ypos), size=(10,10))  

            #----------------------------------------------------------------------------
            if self.nSwitches == 5:
                Color(1.0,0.5,0,OPAQUE, mode="rgba")
                self.sw4Con = Rectangle(pos=(self.Xpos+110,self.Ypos), size=(10,10))  
            
            if self.nSwitches >= 4:
                Color(1.0,0.5,0,OPAQUE, mode="rgba")
                self.sw3Con = Rectangle(pos=(self.Xpos+90,self.Ypos), size=(10,10))  
            
            if self.nSwitches >= 3:
                Color(1.0,0.5,0,OPAQUE, mode="rgba")
                self.sw2Con = Rectangle(pos=(self.Xpos+70,self.Ypos), size=(10,10))  
            
            if self.nSwitches >= 2:
                Color(1.0,0.5,0,OPAQUE, mode="rgba")
                self.sw1Con = Rectangle(pos=(self.Xpos+50,self.Ypos), size=(10,10))  
            
            if self.nSwitches >= 1:
                Color(1.0,0.5,0,OPAQUE, mode="rgba")
                self.sw0Con = Rectangle(pos=(self.Xpos+30,self.Ypos), size=(10,10))  

            #----------------------------------------------------------------------------
            if self.nParams == 6:  
                Color(0.5,0,1,OPAQUE, mode="rgba")
                self.param6Con = Rectangle(pos=(self.Xpos+110,self.Ypos+80), size=(10,10))         

            if self.nParams >= 5:
                Color(0.5,0,1,OPAQUE, mode="rgba")
                self.param5Con = Rectangle(pos=(self.Xpos+90,self.Ypos+80), size=(10,10))

            if self.nParams >= 4: 
                Color(0.5,0,1,OPAQUE, mode="rgba")
                self.param4Con = Rectangle(pos=(self.Xpos+70,self.Ypos+80), size=(10,10))

            if self.nParams >= 3:
                Color(0.5,0,1,OPAQUE, mode="rgba")
                self.param3Con = Rectangle(pos=(self.Xpos+50,self.Ypos+80), size=(10,10))

            if self.nParams >= 2:
                Color(0.5,0,1,OPAQUE, mode="rgba")
                self.param2Con = Rectangle(pos=(self.Xpos+30,self.Ypos+80), size=(10,10))

            if self.nParams >= 1:
                Color(0.5,0,1,OPAQUE, mode="rgba")
                self.param1Con = Rectangle(pos=(self.Xpos+10,self.Ypos+80), size=(10,10))
 
    def get_connector_name(self,connector):
        if connector == OUTPUT:
            return 'Input'

        if connector == INPUT:
            return 'Output'

        if connector == USER_BLOCK_IN:
            return 'User Output'
        
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

    def remove_block(self):
        with self.canvas:
            self.canvas.remove(self.rect)
            self.label.text = ""
            if self.inputConnector:
                self.canvas.remove(self.input)
            if self.outputConnector: 
                self.canvas.remove(self.output)                
            if "Splitter" in self.name:
                self.canvas.remove(self.output1)      
                self.canvas.remove(self.output2)  
            if "Mixer" in self.name:
                self.canvas.remove(self.input1)      
                self.canvas.remove(self.input2)  
                self.canvas.remove(self.param1Con)
                self.canvas.remove(self.param2Con)
            if self.nParams == 6:
                self.canvas.remove(self.param6Con)
            if self.nParams >= 5:
                self.canvas.remove(self.param5Con)
            if self.nParams >= 4:                
                self.canvas.remove(self.param4Con)
            if self.nParams >= 3:
                self.canvas.remove(self.param3Con)
            if self.nParams >= 2:
                self.canvas.remove(self.param2Con)
            if self.nParams >= 1:
                self.canvas.remove(self.param1Con)   
            if self.nUserOuts == 2:
                self.canvas.remove(self.user1Con)
            if self.nUserOuts >= 1:
                self.canvas.remove(self.user0Con)
            if self.tapSwitch:
                self.canvas.remove(self.tapCon)
            if self.nSwitches == 5:
                self.canvas.remove(self.sw4Con) 
            if self.nSwitches >= 4:
                self.canvas.remove(self.sw3Con) 
            if self.nSwitches >= 3:
                self.canvas.remove(self.sw2Con) 
            if self.nSwitches >= 2:
                self.canvas.remove(self.sw1Con) 
            if self.nSwitches >= 1:
                self.canvas.remove(self.sw0Con) 
            if self.valOut is not None:
                self.canvas.remove(self.valOut)
            if self.tapOut is not None:
                self.canvas.remove(self.tapOut)
            if self.switchOut is not None:
                self.canvas.remove(self.switchOut)   
            if self.userOut is not None:
                self.canvas.remove(self.userOut)      
            self.canvas.ask_update()

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
                                    
                                    if self.rect.size[X] == 100: # small blocks
                                        self.label.pos[X] = touch.pos[X]
                                        self.label.pos[Y] = touch.pos[Y] - (self.rect.size[Y]/2)
                                    else: 
                                        self.label.pos[X] = touch.pos[X] + 15
                                        self.label.pos[Y] = touch.pos[Y] - 5
                                    self.move_connectors(touch,1,1)

    def release_block(self,touch):
        self.selected = RELEASED 

    def is_touch_detected(self,touch,moving):
        if touch.pos[X] > self.rect.pos[X] and touch.pos[X] < (self.rect.pos[X] + self.rect.size[X]):
            if touch.pos[Y] > self.rect.pos[Y] and touch.pos[Y] < (self.rect.pos[Y] + self.rect.size[Y]):
                if moving == STILL:
                    self.selected = SELECTED
                    self.is_inside_connector(touch,ASSIGN_LINE) #assign a line if inside a connector
                    return 1 
        return 0            
                    
    def is_collision(self,secondBlock):
        if self.rect.pos[X] < secondBlock.rect.pos[X] + secondBlock.rect.size[X] + THRESH:        
            if self.rect.pos[X] + self.rect.size[X] > secondBlock.rect.pos[X] - THRESH:
                if self.rect.pos[Y] < secondBlock.rect.pos[Y] + secondBlock.rect.size[Y] + THRESH:        
                    if self.rect.pos[Y] + self.rect.size[Y] > secondBlock.rect.pos[Y] - THRESH:
                        return COLLISION

        # if self.name is not None:
        #     if self.collide_widget(secondBlock):
        #         return COLLISION
        return NO_COLLISION                

    def assign_line(self,touch, start_connector):
        with self.canvas:
            conLine = MyLine(touch,self,start_connector)
            self.conLines.append(conLine)

    def move_connectors(self,touch,moveX,moveY):
        #======================================== Switch
        if "Switch" in self.name:
            temp = list(self.switchOut.pos)
            if moveX:
                temp[X] = touch.pos[0] + 45
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    conLine.move_line(temp[X]+5,temp[Y]+5)
            self.switchOut.pos = tuple(temp)

        #======================================== Tap Tempo
        if "Tap" in self.name:
            temp = list(self.tapOut.pos)
            if moveX:
                temp[X] = touch.pos[0] + 45
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    conLine.move_line(temp[X]+5,temp[Y]+5)
            self.tapOut.pos = tuple(temp)    

        #======================================== Tap Tempo
        if "Pot" in self.name or "Constant" in self.name or "Envelope" in self.name:
            temp = list(self.valOut.pos)
            if moveX:
                temp[X] = touch.pos[0] + 45
            if moveY:
                temp[Y] = touch.pos[1] + 0
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    conLine.move_line(temp[X]+5,temp[Y]+5)
            self.valOut.pos = tuple(temp)    
            
        #========================================Splitter
        if "Splitter" in self.name: 
            #**********************************input
            temp = list(self.input.pos)
            if moveX:
                temp[X] = touch.pos[0] + 0
            if moveY:
                temp[Y] = touch.pos[1] + 20
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == INPUT:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.start_connector == INPUT:
                        conLine.move_line(temp[X]+5,temp[Y]+5)
            self.input.pos = tuple(temp)

            #**********************************output 1
            temp = list(self.output1.pos)
            if moveX:
                temp[X] = touch.pos[0] + 90
            if moveY:
                temp[Y] = touch.pos[1] + 30
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == SPLITTER + 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == SPLITTER + 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.output1.pos = tuple(temp)

            #**********************************output 1
            temp = list(self.output2.pos)
            if moveX:
                temp[X] = touch.pos[0] + 90
            if moveY:
                temp[Y] = touch.pos[1] + 10
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == SPLITTER + 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == SPLITTER + 2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.output2.pos = tuple(temp)
            return

        #========================================Mixer
        if "Mixer" in self.name: 

            #**********************************output
            temp = list(self.output.pos)
            if moveX:
                temp[X] = touch.pos[0] + 90
            if moveY:
                temp[Y] = touch.pos[1] + 20
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == OUTPUT:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == OUTPUT:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.output.pos = tuple(temp)    

            #**********************************Level 1
            temp = list(self.param1Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 30
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == PARAM1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == PARAM1:
                        conLine.move_line(temp[X]+5,temp[Y]+5)  
            self.param1Con.pos = tuple(temp)

            #**********************************Level 2
            temp = list(self.param2Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 60
            if moveY:
                temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == PARAM2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == PARAM2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param2Con.pos = tuple(temp)

            #**********************************input 1
            temp = list(self.input1.pos)
            if moveX:
                temp[X] = touch.pos[0] + 0
            if moveY:
                temp[Y] = touch.pos[1] + 30
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == MIXER+1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == MIXER+1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.input1.pos = tuple(temp)

            #**********************************input 2
            temp = list(self.input2.pos)
            if moveX:
                temp[X] = touch.pos[0] + 0
            if moveY:
                temp[Y] = touch.pos[1] + 10
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == MIXER+2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == MIXER+2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.input2.pos = tuple(temp)
            return
    
        #========================================
        if "User" in self.name:
            temp = list(self.userOut.pos)
            if moveX:
                temp[X] = touch.pos[0] + 0
            if moveY:
                temp[Y] = touch.pos[1] + 20
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == USER_BLOCK_IN:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == USER_BLOCK_IN:
                        conLine.move_line(temp[X]+5,temp[Y]+5)
            self.userOut.pos = tuple(temp)

      #========================================
        if self.inputConnector:
            temp = list(self.input.pos)
            if moveX:
                temp[X] = touch.pos[0] + 0
            if moveY:
                if "Output" in self.name or  "Envelope" in self.name:
                    temp[Y] = touch.pos[1] + 20
                else:
                    temp[Y] = touch.pos[1] + 40
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == INPUT:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == INPUT:
                        conLine.move_line(temp[X]+5,temp[Y]+5)
            self.input.pos = tuple(temp)

        #========================================
        if self.outputConnector: 
            temp = list(self.output.pos)
            if "Input" in self.name or  "Envelope" in self.name:
                if moveX:
                    temp[X] = touch.pos[0] + 90
                if moveY:
                    temp[Y] = touch.pos[1] + 20
            else:
                if moveX:
                    temp[X] = touch.pos[0] + 120
                if moveY:
                    temp[Y] = touch.pos[1] + 40

            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == OUTPUT:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == OUTPUT:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.output.pos = tuple(temp)    

        if self.nParams == 6:
            #**********************************Connector 6
            temp = list(self.param6Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 110
            if moveY:
                temp[Y] = touch.pos[1] + 80
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == PARAM6:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == PARAM6:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param6Con.pos = tuple(temp)

        if self.nParams >= 5:
            #**********************************Connector 5
            temp = list(self.param5Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 90
            if moveY:
                temp[Y] = touch.pos[1] + 80
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == PARAM5:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == PARAM5:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param5Con.pos = tuple(temp)    

        if self.nParams >= 4:
            #**********************************Connector 4
            temp = list(self.param4Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 70
            if moveY:
                temp[Y] = touch.pos[1] + 80
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == PARAM4:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == PARAM4:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param4Con.pos = tuple(temp)

        if self.nParams >= 3:
            #**********************************Connector 3
            temp = list(self.param3Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 50
            if moveY:
                temp[Y] = touch.pos[1] + 80
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == PARAM3:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == PARAM3:
                        conLine.move_line(temp[X]+5,temp[Y]+5)  
            self.param3Con.pos = tuple(temp)

        if self.nParams >= 2:        
            #**********************************Connector 2
            temp = list(self.param2Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 30
            if moveY:
                temp[Y] = touch.pos[1] + 80
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == PARAM2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == PARAM2:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param2Con.pos = tuple(temp)

        if self.nParams >= 1: 
            #**********************************Connector 1
            temp = list(self.param1Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 10
            if moveY:
                temp[Y] = touch.pos[1] + 80
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == PARAM1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == PARAM1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.param1Con.pos = tuple(temp)


        #**********************************
        if self.nUserOuts == 2:
            temp = list(self.user1Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 120
            if moveY:
                temp[Y] = touch.pos[1] + 10
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == USER1OUT:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == USER1OUT:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.user1Con.pos = tuple(temp)
            
        if self.nUserOuts >= 1:
            temp = list(self.user0Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 120
            if moveY:
                temp[Y] = touch.pos[1] + 70
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == USER0OUT:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == USER0OUT:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.user0Con.pos = tuple(temp)

        #**********************************
        if self.tapSwitch:
            temp = list(self.tapCon.pos)
            if moveX:
                temp[X] = touch.pos[0] + 10
            if moveY:
                temp[Y] = touch.pos[1] + 0
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == TAP_IN:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == TAP_IN:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.tapCon.pos = tuple(temp)

        #**********************************
        if self.nSwitches == 5:
            temp = list(self.sw4Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 110
            if moveY:
                temp[Y] = touch.pos[1] + 0
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == SW4_IN:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == SW4_IN:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.sw4Con.pos = tuple(temp)
            
        if self.nSwitches >= 4:
            temp = list(self.sw3Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 90
            if moveY:
                temp[Y] = touch.pos[1] + 0
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == SW3_IN:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == SW3_IN:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.sw3Con.pos = tuple(temp) 

        if self.nSwitches >= 3:
            temp = list(self.sw2Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 70
            if moveY:
                temp[Y] = touch.pos[1] + 0
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == SW2_IN:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == 1:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.sw2Con.pos = tuple(temp)      


        if self.nSwitches >= 2:
            temp = list(self.sw1Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 50
            if moveY:
                temp[Y] = touch.pos[1] + 0
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == SW1_IN:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == SW1_IN:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.sw1Con.pos = tuple(temp)      

        if self.nSwitches >= 1:
            temp = list(self.sw0Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 30
            if moveY:
                temp[Y] = touch.pos[1] + 0
            for conLine in self.conLines: # move connected lines
                if conLine.start_block.name == self.name:
                    if conLine.start_connector == SW0_IN:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
                elif conLine.end_block.name == self.name:
                    if conLine.end_connector == SW0_IN:
                        conLine.move_line(temp[X]+5,temp[Y]+5) 
            self.sw0Con.pos = tuple(temp)     

    def is_inside_connector(self,touch,allow_assign_line):

        #============================================
        if self.inputConnector:
            if touch.pos[X] > self.input.pos[X] and touch.pos[X] < (self.input.pos[X] + self.input.size[X]):
                if touch.pos[Y] > self.input.pos[Y] and touch.pos[Y] < (self.input.pos[Y] + self.input.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == INPUT: #dont assign a new line if there is one on this connector   
                                        return INPUT 
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == INPUT: #dont assign a new line if there is one on this connector   
                                        return INPUT  
                            self.assign_line(touch,INPUT)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,INPUT)
                    return INPUT  
                
        #============================================
        if self.outputConnector:
            if touch.pos[X] > self.output.pos[X] and touch.pos[X] < (self.output.pos[X] + self.output.size[X]):
                if touch.pos[Y] > self.output.pos[Y] and touch.pos[Y] < (self.output.pos[Y] + self.output.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == OUTPUT: #dont assign a new line if there is one on this connector   
                                        return OUTPUT  
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == OUTPUT: #dont assign a new line if there is one on this connector   
                                        return OUTPUT  
                            self.assign_line(touch,OUTPUT)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,OUTPUT)
                    return OUTPUT  

        #============================================
        if "Tap Tempo" in self.name:
            if touch.pos[X] > self.tapOut.pos[X] and touch.pos[X] < (self.tapOut.pos[X] + self.tapOut.size[X]):
                if touch.pos[Y] > self.tapOut.pos[Y] and touch.pos[Y] < (self.tapOut.pos[Y] + self.tapOut.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == TAP_OUT: #dont assign a new line if there is one on this connector   
                                        return TAP_OUT 
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == TAP_OUT: #dont assign a new line if there is one on this connector   
                                        return TAP_OUT  
                            self.assign_line(touch,TAP_OUT)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,TAP_OUT)
                    return TAP_OUT      

        #----------------------------------------------------------------------------    
        if "Switch" in self.name:
            if touch.pos[X] > self.switchOut.pos[X] and touch.pos[X] < (self.switchOut.pos[X] + self.switchOut.size[X]):
                if touch.pos[Y] > self.switchOut.pos[Y] and touch.pos[Y] < (self.switchOut.pos[Y] + self.switchOut.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == SWITCH_OUT: #dont assign a new line if there is one on this connector   
                                        return SWITCH_OUT 
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == SWITCH_OUT: #dont assign a new line if there is one on this connector   
                                        return SWITCH_OUT  
                            self.assign_line(touch,SWITCH_OUT)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,SWITCH_OUT)
                    return SWITCH_OUT      

            #----------------------------------------------------------------------------
        if "Constant" in self.name or "Pot" in self.name or "Envelope" in self.name:
            if touch.pos[X] > self.valOut.pos[X] and touch.pos[X] < (self.valOut.pos[X] + self.valOut.size[X]):
                if touch.pos[Y] > self.valOut.pos[Y] and touch.pos[Y] < (self.valOut.pos[Y] + self.valOut.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == VAL_OUT: #dont assign a new line if there is one on this connector   
                                        return VAL_OUT 
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == VAL_OUT: #dont assign a new line if there is one on this connector   
                                        return VAL_OUT  
                            self.assign_line(touch,VAL_OUT)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,VAL_OUT)
                    return VAL_OUT      

        if "User" in self.name:
            if touch.pos[X] > self.userOut.pos[X] and touch.pos[X] < (self.userOut.pos[X] + self.userOut.size[X]):
                if touch.pos[Y] > self.userOut.pos[Y] and touch.pos[Y] < (self.userOut.pos[Y] + self.userOut.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == USER_BLOCK_IN: #dont assign a new line if there is one on this connector   
                                        return USER_BLOCK_IN 
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == USER_BLOCK_IN: #dont assign a new line if there is one on this connector   
                                        return USER_BLOCK_IN  
                            self.assign_line(touch,USER_BLOCK_IN)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,USER_BLOCK_IN)
                    return USER_BLOCK_IN
                
        #============================================SPLITTER
        if "Splitter" in self.name: 
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
        if "Mixer" in self.name: 
            if touch.pos[X] > self.input1.pos[X] and touch.pos[X] < (self.input1.pos[X] + self.input1.size[X]):
                if touch.pos[Y] > self.input1.pos[Y] and touch.pos[Y] < (self.input1.pos[Y] + self.input1.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector ==MIXER+1: #dont assign a new line if there is one on this connector   
                                        return MIXER+1 
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == MIXER+1: #dont assign a new line if there is one on this connector   
                                        return MIXER+1  
                            self.assign_line(touch,MIXER+1)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,MIXER+1)
                    return MIXER+1

            if touch.pos[X] > self.input2.pos[X] and touch.pos[X] < (self.input2.pos[X] + self.input2.size[X]):
                if touch.pos[Y] > self.input2.pos[Y] and touch.pos[Y] < (self.input2.pos[Y] + self.input2.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == MIXER+2: #dont assign a new line if there is one on this connector   
                                        return MIXER+2
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == MIXER+2: #dont assign a new line if there is one on this connector   
                                        return MIXER+2  
                            self.assign_line(touch,MIXER+2)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,MIXER+2)
                    return MIXER+2
            
            if touch.pos[X] > self.param2Con.pos[X] and touch.pos[X] < (self.param2Con.pos[X] + self.param2Con.size[X]):
                if touch.pos[Y] > self.param2Con.pos[Y] and touch.pos[Y] < (self.param2Con.pos[Y] + self.param2Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == PARAM2: #dont assign a new line if there is one on this connector   
                                        return PARAM2  
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == PARAM2: #dont assign a new line if there is one on this connector   
                                        return PARAM2 
                            self.assign_line(touch,PARAM2)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,PARAM2)
                    return PARAM2     

            if touch.pos[X] > self.param1Con.pos[X] and touch.pos[X] < (self.param1Con.pos[X] + self.param1Con.size[X]):
                if touch.pos[Y] > self.param1Con.pos[Y] and touch.pos[Y] < (self.param1Con.pos[Y] + self.param1Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == PARAM1: #dont assign a new line if there is one on this connector   
                                        return PARAM1  
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == PARAM1: #dont assign a new line if there is one on this connector   
                                        return PARAM1 
                            self.assign_line(touch,PARAM1)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,PARAM1)
                    return PARAM1 

        #==============Parameter 6   
        if self.nParams == 6:
            if touch.pos[X] > self.param6Con.pos[X] and touch.pos[X] < (self.param6Con.pos[X] + self.param6Con.size[X]):
                if touch.pos[Y] > self.param6Con.pos[Y] and touch.pos[Y] < (self.param6Con.pos[Y] + self.param6Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == PARAM6: #dont assign a new line if there is one on this connector   
                                        return PARAM6  
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == PARAM6: #dont assign a new line if there is one on this connector   
                                        return PARAM6  
                            self.assign_line(touch,PARAM6)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,PARAM6)
                    return PARAM6 

        #==============Parameter 5
        if self.nParams >= 5:                
            if touch.pos[X] > self.param5Con.pos[X] and touch.pos[X] < (self.param5Con.pos[X] + self.param5Con.size[X]):
                if touch.pos[Y] > self.param5Con.pos[Y] and touch.pos[Y] < (self.param5Con.pos[Y] + self.param5Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == PARAM5: #dont assign a new line if there is one on this connector   
                                        return PARAM5  
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == PARAM5: #dont assign a new line if there is one on this connector   
                                        return PARAM5  
                            self.assign_line(touch,PARAM5)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,PARAM5)
                    return PARAM5

        #==============Parameter 4              
        if self.nParams >=4:                
            if touch.pos[X] > self.param4Con.pos[X] and touch.pos[X] < (self.param4Con.pos[X] + self.param4Con.size[X]):
                if touch.pos[Y] > self.param4Con.pos[Y] and touch.pos[Y] < (self.param4Con.pos[Y] + self.param4Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == PARAM4: #dont assign a new line if there is one on this connector   
                                        return PARAM4  
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == PARAM4: #dont assign a new line if there is one on this connector   
                                        return PARAM4  
                            self.assign_line(touch,PARAM4)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,PARAM4)
                    return PARAM4

        #==============Parameter 3 
        if self.nParams >= 3:                
            if touch.pos[X] > self.param3Con.pos[X] and touch.pos[X] < (self.param3Con.pos[X] + self.param3Con.size[X]):
                if touch.pos[Y] > self.param3Con.pos[Y] and touch.pos[Y] < (self.param3Con.pos[Y] + self.param3Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == PARAM3: #dont assign a new line if there is one on this connector   
                                        return PARAM3 
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == PARAM3: #dont assign a new line if there is one on this connector   
                                        return PARAM3 
                            self.assign_line(touch,PARAM3)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,PARAM3)
                    return PARAM3 
        
        #==============Parameter 2 
        if self.nParams >= 2:                
            if touch.pos[X] > self.param2Con.pos[X] and touch.pos[X] < (self.param2Con.pos[X] + self.param2Con.size[X]):
                if touch.pos[Y] > self.param2Con.pos[Y] and touch.pos[Y] < (self.param2Con.pos[Y] + self.param2Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == PARAM2: #dont assign a new line if there is one on this connector   
                                        return PARAM2  
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == PARAM2: #dont assign a new line if there is one on this connector   
                                        return PARAM2 
                            self.assign_line(touch,PARAM2)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,PARAM2)
                    return PARAM2     

        #==============Parameter 1 
        if self.nParams >= 1:                
            if touch.pos[X] > self.param1Con.pos[X] and touch.pos[X] < (self.param1Con.pos[X] + self.param1Con.size[X]):
                if touch.pos[Y] > self.param1Con.pos[Y] and touch.pos[Y] < (self.param1Con.pos[Y] + self.param1Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == PARAM1: #dont assign a new line if there is one on this connector   
                                        return PARAM1  
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == PARAM1: #dont assign a new line if there is one on this connector   
                                        return PARAM1 
                            self.assign_line(touch,PARAM1)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,PARAM1)
                    return PARAM1 

        #=============================================================================  
        if self.nUserOuts == 2:
            if touch.pos[X] > self.user1Con.pos[X] and touch.pos[X] < (self.user1Con.pos[X] + self.user1Con.size[X]):
                if touch.pos[Y] > self.user1Con.pos[Y] and touch.pos[Y] < (self.user1Con.pos[Y] + self.user1Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == USER1OUT: #dont assign a new line if there is one on this connector   
                                        return USER1OUT  
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == USER1OUT: #dont assign a new line if there is one on this connector   
                                        return USER1OUT 
                            self.assign_line(touch,USER1OUT)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,USER1OUT)
                    return USER1OUT 
                
        if self.nUserOuts >= 1:
            if touch.pos[X] > self.user0Con.pos[X] and touch.pos[X] < (self.user0Con.pos[X] + self.user0Con.size[X]):
                if touch.pos[Y] > self.user0Con.pos[Y] and touch.pos[Y] < (self.user0Con.pos[Y] + self.user0Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == USER0OUT: #dont assign a new line if there is one on this connector   
                                        return USER0OUT  
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == USER0OUT: #dont assign a new line if there is one on this connector   
                                        return USER0OUT 
                            self.assign_line(touch,USER0OUT)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,USER0OUT)
                    return USER0OUT

        #=============================================================================           
        if self.tapSwitch:
            if touch.pos[X] > self.tapCon.pos[X] and touch.pos[X] < (self.tapCon.pos[X] + self.tapCon.size[X]):
                if touch.pos[Y] > self.tapCon.pos[Y] and touch.pos[Y] < (self.tapCon.pos[Y] + self.tapCon.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == TAP_IN: #dont assign a new line if there is one on this connector   
                                        return TAP_IN  
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == TAP_IN: #dont assign a new line if there is one on this connector   
                                        return TAP_IN 
                            self.assign_line(touch,TAP_IN)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,TAP_IN)
                    return TAP_IN
                
        #=============================================================================        
        if self.nSwitches == 5:
            if touch.pos[X] > self.sw4Con.pos[X] and touch.pos[X] < (self.sw4Con.pos[X] + self.sw4Con.size[X]):
                if touch.pos[Y] > self.sw4Con.pos[Y] and touch.pos[Y] < (self.sw4Con.pos[Y] + self.sw4Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == SW4_IN: #dont assign a new line if there is one on this connector   
                                        return SW4_IN  
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == SW4_IN: #dont assign a new line if there is one on this connector   
                                        return SW4_IN 
                            self.assign_line(touch,SW4_IN)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,SW4_IN)
                    return SW4_IN     
                                    
        if self.nSwitches >= 4:
            if touch.pos[X] > self.sw3Con.pos[X] and touch.pos[X] < (self.sw3Con.pos[X] + self.sw3Con.size[X]):
                if touch.pos[Y] > self.sw3Con.pos[Y] and touch.pos[Y] < (self.sw3Con.pos[Y] + self.sw3Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == SW3_IN: #dont assign a new line if there is one on this connector   
                                        return SW3_IN  
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == SW3_IN: #dont assign a new line if there is one on this connector   
                                        return SW3_IN 
                            self.assign_line(touch,SW3_IN)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,SW3_IN)
                    return SW3_IN
                                
        if self.nSwitches >= 3:
            if touch.pos[X] > self.sw2Con.pos[X] and touch.pos[X] < (self.sw2Con.pos[X] + self.sw2Con.size[X]):
                if touch.pos[Y] > self.sw2Con.pos[Y] and touch.pos[Y] < (self.sw2Con.pos[Y] + self.sw2Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == SW2_IN: #dont assign a new line if there is one on this connector   
                                        return SW2_IN  
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == SW2_IN: #dont assign a new line if there is one on this connector   
                                        return SW2_IN 
                            self.assign_line(touch,SW2_IN)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,SW2_IN)
                    return SW2_IN    
                
        if self.nSwitches >= 2:
            if touch.pos[X] > self.sw1Con.pos[X] and touch.pos[X] < (self.sw1Con.pos[X] + self.sw1Con.size[X]):
                if touch.pos[Y] > self.sw1Con.pos[Y] and touch.pos[Y] < (self.sw1Con.pos[Y] + self.sw1Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == SW1_IN: #dont assign a new line if there is one on this connector   
                                        return SW1_IN  
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == SW1_IN: #dont assign a new line if there is one on this connector   
                                        return SW1_IN 
                            self.assign_line(touch,SW1_IN)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,SW1_IN)
                    return SW1_IN   
                
        if self.nSwitches >= 1:
            if touch.pos[X] > self.sw0Con.pos[X] and touch.pos[X] < (self.sw0Con.pos[X] + self.sw0Con.size[X]):
                if touch.pos[Y] > self.sw0Con.pos[Y] and touch.pos[Y] < (self.sw0Con.pos[Y] + self.sw0Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        if self.conLines != []: # if there are conlines
                            for conLine in self.conLines:
                                if conLine.start_block.name == self.name: #line starts in this block
                                    if conLine.start_connector == SW0_IN: #dont assign a new line if there is one on this connector   
                                        return SW0_IN  
                                elif conLine.end_block.name == self.name: #line ends in this block
                                    if conLine.end_connector == SW0_IN: #dont assign a new line if there is one on this connector   
                                        return SW0_IN 
                            self.assign_line(touch,SW0_IN)                  
                        else: #assign a line as there are none connected to this block
                            self.assign_line(touch,SW0_IN)
                    return SW0_IN         
                    
        return 0