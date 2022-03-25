# LeoSchofield 01/01/2022
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.graphics import Rectangle, Color, Line
from kivy.core.window import Window
import random

TRUE = 1
FALSE = 0

MOVING = 1
STILL = 0

SELECTED = 1 
RELEASED = 0

DRAGGING = 1
NOT_DRAGGING = 0

OPAQUE = 1 

X = 0
Y = 1 

BLOCK_WIDTH = 100 
BLOCK_HEIGHT = 50

COLLISION = 1
NO_COLLISION = 0

BUTTON_HEIGHT = 30

THRESH = 20

LINE_STARTED = ()
LINE_END = ()

STOPPED = 0 
STARTED = 1 

blocks = []

DONT_ASSIGN_LINE = 0
ASSIGN_LINE = 1
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
        self.nBlockParams = nblockParams
        self.dragging = DRAGGING
        self.name = "line_"+start_block +"_"+str(start_connector)
        print("NEW!"+self.name)
        self.line = Line(points=[self.start_point[X], self.start_point[Y], self.end_point[X], self.end_point[Y]], width=1.4, cap='none', joint='none')
        
    def move_line(self, touch):
        with self.canvas:
            for block in blocks:
                if block.name == self.start_block: #if in the block that created the connector line
                    if self.dragging == DRAGGING:  #if dragging the line on intial creation 
                        Color(0.7, 0.7, 0.7, 1)
                        self.end_point = touch.pos
                        self.line.points=[self.start_point[X], self.start_point[Y], self.end_point[X], self.end_point[Y]]

                    elif block.selected == SELECTED: #if moving the block that created the line
                        self.start_point = touch.pos
                        self.line.points=[self.start_point[X], self.start_point[Y], self.end_point[X], self.end_point[Y]]

                if block.name == self.end_block: #if in the block that the line finished dragging in
                    if block.selected == SELECTED:
                        self.end_point = touch.pos
                        self.line.points=[self.start_point[X], self.start_point[Y], self.end_point[X], self.end_point[Y]]
                        

#========================================================================        
#============================Block=======================================
#========================================================================
class Block(Widget):
    def __init__(self,name,inputConnector,outputConnector,nParams, **kwargs):
        super(Block, self).__init__(**kwargs)
        self.name = name
        self.Xpos = random.randrange(200, 1000)
        self.Ypos = random.randrange(100, 600)
        Color(0.4,0.4,0.4,OPAQUE, mode="rgba")
        self.rect = Rectangle(pos=(self.Xpos,self.Ypos), size=(BLOCK_WIDTH,BLOCK_HEIGHT))
        self.label = Label(pos=(self.Xpos, self.Ypos - (self.rect.size[Y]/2)),text=name)
        self.selected = RELEASED
        self.nParams = nParams
        self.paramCons = []
        self.conLines = []
        self.inputExists = 0 
        self.outputExists = 0
        Color(0.2,0.2,0.2,OPAQUE, mode="rgba")
        
        if inputConnector: ## todo need multiple inputs for mixers,stereo effects, etc 
            self.input = Rectangle(pos=(self.Xpos,self.Ypos+20), size=(5,10))
            self.inputExists = True

        if outputConnector: ## todo need multiple outputs for splitters,stereo effects, etc
            self.output = Rectangle(pos=(self.Xpos+95,self.Ypos+20), size=(5,10))
            self.outputExists = True

        if self.nParams == 6:  
            self.param1Con = Rectangle(pos=(self.Xpos+15,self.Ypos+45), size=(10,5))
            self.param2Con = Rectangle(pos=(self.Xpos+45,self.Ypos+45), size=(10,5))
            self.param3Con = Rectangle(pos=(self.Xpos+75,self.Ypos+45), size=(10,5))
            self.param4Con = Rectangle(pos=(self.Xpos+15,self.Ypos), size=(10,5))
            self.param5Con = Rectangle(pos=(self.Xpos+45,self.Ypos), size=(10,5))
            self.param6Con = Rectangle(pos=(self.Xpos+75,self.Ypos), size=(10,5))

        elif self.nParams == 5:
            self.param1Con = Rectangle(pos=(self.Xpos+15,self.Ypos+45), size=(10,5))
            self.param2Con = Rectangle(pos=(self.Xpos+45,self.Ypos+45), size=(10,5))
            self.param3Con = Rectangle(pos=(self.Xpos+75,self.Ypos+45), size=(10,5))
            self.param4Con = Rectangle(pos=(self.Xpos+30,self.Ypos), size=(10,5))
            self.param5Con = Rectangle(pos=(self.Xpos+60,self.Ypos), size=(10,5))

        elif self.nParams == 4: 
            self.param1Con = Rectangle(pos=(self.Xpos+30,self.Ypos+45), size=(10,5))
            self.param2Con = Rectangle(pos=(self.Xpos+60,self.Ypos+45), size=(10,5))
            self.param3Con = Rectangle(pos=(self.Xpos+30,self.Ypos), size=(10,5))
            self.param4Con = Rectangle(pos=(self.Xpos+60,self.Ypos), size=(10,5))

        elif self.nParams == 3:
            self.param1Con = Rectangle(pos=(self.Xpos+30,self.Ypos+45), size=(10,5))
            self.param2Con = Rectangle(pos=(self.Xpos+60,self.Ypos+45), size=(10,5))
            self.param3Con = Rectangle(pos=(self.Xpos+45,self.Ypos), size=(10,5))

        elif self.nParams == 2:
            self.param1Con = Rectangle(pos=(self.Xpos+30,self.Ypos+45), size=(10,5))
            self.param2Con = Rectangle(pos=(self.Xpos+60,self.Ypos+45), size=(10,5))

        elif self.nParams == 1:
            self.param1Con = Rectangle(pos=(self.Xpos+45,self.Ypos+45), size=(10,5))

    #------------------------------------------- move_connectors
    def move_connectors(self,touch,moveX,moveY):
        if self.inputExists == True:
            temp = list(self.input.pos)
            if moveX:
                temp[X] = touch.pos[0] + 0
            if moveY:
                temp[Y] = touch.pos[1] + 20
            self.input.pos = tuple(temp)

        if self.outputExists == True: 
            temp = list(self.output.pos)
            if moveX:
                temp[X] = touch.pos[0] + 95
            if moveY:
                temp[Y] = touch.pos[1] + 20
            self.output.pos = tuple(temp)

        if self.nParams == 6:  
            temp = list(self.param1Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 15
            if moveY:
                temp[Y] = touch.pos[1] + 45
            self.param1Con.pos = tuple(temp)

            temp = list(self.param2Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 45
            if moveY:    
                temp[Y] = touch.pos[1] + 45
            self.param2Con.pos = tuple(temp)

            temp = list(self.param3Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 75
            if moveY:
                temp[Y] = touch.pos[1] + 45
            self.param3Con.pos = tuple(temp)

            temp = list(self.param4Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 15
            if moveY:
                temp[Y] = touch.pos[1] + 0
            self.param4Con.pos = tuple(temp)

            temp = list(self.param5Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 45
            if moveY:
                temp[Y] = touch.pos[1] + 0
            self.param5Con.pos = tuple(temp)

            temp = list(self.param6Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 75
            if moveY:
                temp[Y] = touch.pos[1] + 0
            self.param6Con.pos = tuple(temp)

        elif self.nParams == 5:  
            temp = list(self.param1Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 15
            if moveY:
                temp[Y] = touch.pos[1] + 45
            self.param1Con.pos = tuple(temp)

            temp = list(self.param2Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 45
            if moveY:
                temp[Y] = touch.pos[1] + 45
            self.param2Con.pos = tuple(temp)

            temp = list(self.param3Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 75
            if moveY:
                temp[Y] = touch.pos[1] + 45
            self.param3Con.pos = tuple(temp)

            temp = list(self.param4Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 30
            if moveY:
                temp[Y] = touch.pos[1] + 0
            self.param4Con.pos = tuple(temp)

            temp = list(self.param5Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 60
            if moveY:
                temp[Y] = touch.pos[1] + 0
            self.param5Con.pos = tuple(temp)    

        elif self.nParams == 4:  
            temp = list(self.param1Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 30
            if moveY:
                temp[Y] = touch.pos[1] + 45
            self.param1Con.pos = tuple(temp)

            temp = list(self.param2Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 60
            if moveY:
                temp[Y] = touch.pos[1] + 45
            self.param2Con.pos = tuple(temp)

            temp = list(self.param3Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 30
            if moveY:
                temp[Y] = touch.pos[1] + 0
            self.param3Con.pos = tuple(temp)

            temp = list(self.param4Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 60
            if moveY:
                temp[Y] = touch.pos[1] + 0
            self.param4Con.pos = tuple(temp)

        elif self.nParams == 3:  
            temp = list(self.param1Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 30
            if moveY:
                temp[Y] = touch.pos[1] + 45
            self.param1Con.pos = tuple(temp)

            temp = list(self.param2Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 60
            if moveY:
                temp[Y] = touch.pos[1] + 45
            self.param2Con.pos = tuple(temp)

            temp = list(self.param3Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 45
            if moveY:
                temp[Y] = touch.pos[1] + 0
            self.param3Con.pos = tuple(temp)
            
        elif self.nParams == 2:  
            temp = list(self.param1Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 30
            if moveY:
                temp[Y] = touch.pos[1] + 45
            self.param1Con.pos = tuple(temp)

            temp = list(self.param2Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 60
            if moveY:
                temp[Y] = touch.pos[1] + 45
            self.param2Con.pos = tuple(temp)

        elif self.nParams == 1: 
            temp = list(self.param1Con.pos)
            if moveX:
                temp[X] = touch.pos[0] + 45
            if moveY:
                temp[Y] = touch.pos[1] + 45
            self.param1Con.pos = tuple(temp)

    #------------------------------------------- move_block
    def move_block(self,touch,blocks):
        if self.selected == SELECTED:
            if touch.pos[0] + self.rect.size[0] < 1200: #ensures block is below the drop down buttons
                if touch.pos[1] + self.rect.size[1] < 770: #ensures block is left of right border
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
     
    #-------------------------------------------is touch inside connector
    def is_inside_connector(self,touch,allow_assign_line):
        if self.inputExists:
            if touch.pos[X] > self.input.pos[X] and touch.pos[X] < (self.input.pos[X] + self.input.size[X]):
                if touch.pos[Y] > self.input.pos[Y] and touch.pos[Y] < (self.input.pos[Y] + self.input.size[Y]):
                    print("IN Input")  
                    self.selected = RELEASED
                    if allow_assign_line:
                        self.assign_line(touch,self.name,11,self.nParams)   
                    return 11 

        if self.outputExists:
            if touch.pos[X] > self.output.pos[X] and touch.pos[X] < (self.output.pos[X] + self.output.size[X]):
                if touch.pos[Y] > self.output.pos[Y] and touch.pos[Y] < (self.output.pos[Y] + self.output.size[Y]):
                    print("IN Output")  
                    self.selected = RELEASED
                    if allow_assign_line:
                        self.assign_line(touch,self.name,10,self.nParams)   
                    return 10 

        if self.nParams == 7: #todo for potentiometer blocks
            # if touch.pos[X] > self.param6Con.pos[X] and touch.pos[X] < (self.param6Con.pos[X] + self.param6Con.size[X]):
            #     if touch.pos[Y] > self.param6Con.pos[Y] and touch.pos[Y] < (self.param6Con.pos[Y] + self.param6Con.size[Y]):
            #         print("IN 6") 
            #         self.selected = RELEASED
            #         LINE_STARTED = touch.pos
            #         self.drawLine(touch)    
            return 7  

        if self.nParams == 6:
            if touch.pos[X] > self.param6Con.pos[X] and touch.pos[X] < (self.param6Con.pos[X] + self.param6Con.size[X]):
                if touch.pos[Y] > self.param6Con.pos[Y] and touch.pos[Y] < (self.param6Con.pos[Y] + self.param6Con.size[Y]):
                    #print("IN 6") 
                    self.selected = RELEASED
                    if allow_assign_line:
                        self.assign_line(touch,self.name, 6,self.nParams)  
                    return 6  
        if self.nParams >= 5:                
            if touch.pos[X] > self.param5Con.pos[X] and touch.pos[X] < (self.param5Con.pos[X] + self.param5Con.size[X]):
                if touch.pos[Y] > self.param5Con.pos[Y] and touch.pos[Y] < (self.param5Con.pos[Y] + self.param5Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        self.assign_line(touch,self.name,5,self.nParams)  
                    #print("IN 5")      
                    return 5 
        if self.nParams >=4:                
            if touch.pos[X] > self.param4Con.pos[X] and touch.pos[X] < (self.param4Con.pos[X] + self.param4Con.size[X]):
                if touch.pos[Y] > self.param4Con.pos[Y] and touch.pos[Y] < (self.param4Con.pos[Y] + self.param4Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        self.assign_line(touch,self.name,4,self.nParams)  
                    #print("IN 4") 
                    return 4      
        if self.nParams >= 3:                
            if touch.pos[X] > self.param3Con.pos[X] and touch.pos[X] < (self.param3Con.pos[X] + self.param3Con.size[X]):
                if touch.pos[Y] > self.param3Con.pos[Y] and touch.pos[Y] < (self.param3Con.pos[Y] + self.param3Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        self.assign_line(touch,self.name,3,self.nParams)  
                    #print("IN 3") 
                    return 3 
        if self.nParams >= 2:                
            if touch.pos[X] > self.param2Con.pos[X] and touch.pos[X] < (self.param2Con.pos[X] + self.param2Con.size[X]):
                if touch.pos[Y] > self.param2Con.pos[Y] and touch.pos[Y] < (self.param2Con.pos[Y] + self.param2Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        self.assign_line(touch,self.name,2,self.nParams)  
                    #print("IN 2") 
                    return 2    
        if self.nParams >= 1:                
            if touch.pos[X] > self.param1Con.pos[X] and touch.pos[X] < (self.param1Con.pos[X] + self.param1Con.size[X]):
                if touch.pos[Y] > self.param1Con.pos[Y] and touch.pos[Y] < (self.param1Con.pos[Y] + self.param1Con.size[Y]):
                    self.selected = RELEASED
                    if allow_assign_line:
                        self.assign_line(touch,self.name,1,self.nParams)   
                    #print("IN 1") 
                    return 1
        return 0   

    #------------------------------------------- is_touch_detected
    def is_touch_detected(self,touch,moving):
        if touch.pos[X] > self.rect.pos[X] and touch.pos[X] < (self.rect.pos[X] + self.rect.size[X]):
            if touch.pos[Y] > self.rect.pos[Y] and touch.pos[Y] < (self.rect.pos[Y] + self.rect.size[Y]):
                if moving == STILL:
                    self.selected = SELECTED
                    print("BLOCK SELECTED")
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

            if not blocks:
                block = Block(temp,inputNode,outputNode,nParams)   
                blocks.append(block)
            else:
                while not create_block:
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

    #-------------------------------------------
    def on_touch_down(self, touch):
        if blocks:
            for block in blocks:
                if block.conLines:
                    for line in block.conLines:   
                        if line.dragging == DRAGGING:
                            line.move_line(touch)
                            return #don't check for collision with block if dragging a line
            self.detect_collisions(touch,STILL)

    #-------------------------------------------
    def on_touch_move(self, touch):
        for block in blocks:
            block.move_block(touch,blocks)
            for conLine in block.conLines:
                conLine.move_line(touch)

    #-------------------------------------------
    def on_touch_up(self,touch):
        for block1 in blocks:
            block1.release_block(touch)
            if block1.conLines:
                for conLine in block1.conLines:
                    if conLine.dragging == DRAGGING:
                        for block2 in blocks:#search through the other blocks to see if end of line (mouse pointer) is inside a connector
                            if block1.name != block2.name:
                                if block2.is_inside_connector(touch,DONT_ASSIGN_LINE):                   
                                    conLine.dragging = NOT_DRAGGING
                                    conLine.end_block=block2.name
                                    print(conLine.end_block)


    #-------------------------------------------
    def detect_collisions(self, touch, moving):
        for block in blocks:
            if block.is_touch_detected(touch,moving): 
                return TRUE
        return FALSE

#========================================================================        
#===========================FXCoreDesignerApp============================
#========================================================================
class FXCoreDesignerApp(App):

    def build(self):

        Window.size = (1200, 800)
        Window.bind(mouse_pos=self.on_mouse_pos)

        click = Click() 

        layout = GridLayout(cols = 5, row_force_default = True, row_default_height = BUTTON_HEIGHT)
        
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

        #--------------------------------Routingdrop
        Routingdrop = DropDown()
        #
        splitterBtn = Button(text ='Splitter', size_hint_y = None, height = BUTTON_HEIGHT)
        splitterBtn.bind(on_release = lambda none: click.assign_block('Splitter',1,1,4))
        Routingdrop.add_widget(splitterBtn)
        #
        mixerBtn = Button(text ='Mixer', size_hint_y = None, height = BUTTON_HEIGHT)
        mixerBtn.bind(on_release = lambda none: click.assign_block('Mixer',1,1,3))
        Routingdrop.add_widget(mixerBtn)

        #--------------------------------AnalysisDrop
        AnalysisDrop = DropDown()
        #
        FFTBtn = Button(text ='FFT', size_hint_y = None, height = BUTTON_HEIGHT)
        FFTBtn.bind(on_release = lambda  none: click.assign_block('FFT',1,1,1))
        AnalysisDrop.add_widget(FFTBtn)
        #
        envelopeFollowerBtn = Button(text ='Envelope', size_hint_y = None, height = BUTTON_HEIGHT)
        envelopeFollowerBtn.bind(on_release = lambda  none: click.assign_block('Envelope',1,1,1))
        AnalysisDrop.add_widget(envelopeFollowerBtn)
        
        #--------------------------------ControlsDrop
        ControlsDrop = DropDown()
        # 
        PotentiomenterBtn = Button(text ='Pot', size_hint_y = None, height = BUTTON_HEIGHT)
        PotentiomenterBtn.bind(on_release = lambda  none: click.assign_block('Pot',0,0,7))
        ControlsDrop.add_widget(PotentiomenterBtn)
        #

        #--------------------------------
        IObutton = Button(text ='IO')
        IObutton.bind(on_release = IOdrop.open)
        FXbutton = Button(text ='FX')
        FXbutton.bind(on_release = FXdrop.open)
        RoutingButton = Button(text ='Routing')
        RoutingButton.bind(on_release = Routingdrop.open)
        AnalysisButton = Button(text ='Analysis')
        AnalysisButton.bind(on_release = AnalysisDrop.open)
        ControlsButton = Button(text ='Controls')
        ControlsButton.bind(on_release = ControlsDrop.open)
        layout.add_widget(IObutton)
        layout.add_widget(FXbutton)
        layout.add_widget(RoutingButton)
        layout.add_widget(AnalysisButton)
        layout.add_widget(ControlsButton)
        layout.add_widget(click)

        return layout
        
    def on_mouse_pos(self, window, pos):
        #print("pos",pos) todo highlight connectors as mouse hovers over
        pass

if __name__ == '__main__':
    FXCoreDesignerApp().run()