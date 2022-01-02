## LeoSchofield 31/12/2021

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.graphics import Rectangle, Color, Line
from kivy.core.window import Window
import random

MOVING = 1
STILL = 0

SELECTED = 1 
RELEASED = 0

OPAQUE = 1 

X = 0
Y = 1 

BLOCK_WIDTH = 100 
BLOCK_HEIGHT = 50

COLLISION = 1
NO_COLLISION = 0

BUTTON_HEIGHT = 30

THRESH = 20

#========================================================================        
#============================Block=======================================
#========================================================================
class Block(Widget):
    def __init__(self,name,inputConnector,outputConnector,nParams, **kwargs):
        super(Block, self).__init__(**kwargs)
        self.Xpos = random.randrange(200, 1000)
        self.Ypos = random.randrange(100, 600)
        Color(0.4,0.4,0.4,OPAQUE, mode="rgba")
        #self.rect = Rectangle(pos=(0,0), size=(100,50))
        self.rect = Rectangle(pos=(self.Xpos,self.Ypos), size=(BLOCK_WIDTH,BLOCK_HEIGHT))
        #Color(0.5,0.4,0.2,OPAQUE, mode="rgba")
        #self.line = Line(points=[0, 0, 100, 0, 100, 50,0,50,0,0], width=3)
        self.label = Label(pos=(self.Xpos, self.Ypos - (self.rect.size[Y]/2)),text=name)

        self.selected = RELEASED
        self.nParams = nParams
        self.inputExists = 0 
        self.outputExists = 0

        if inputConnector: ## todo need multiple inputs for mixers,stereo effects, etc
            Color(0.2,0.2,0.2,OPAQUE, mode="rgba")
            self.input = Rectangle(pos=(self.Xpos,self.Ypos+20), size=(5,10))
            self.inputExists = True

        if outputConnector: ## todo need multiple outputs for splitters,stereo effects, etc
            Color(0.2,0.2,0.2,OPAQUE, mode="rgba")
            self.output = Rectangle(pos=(self.Xpos+95,self.Ypos+20), size=(5,10))
            self.outputExists = True

        if self.nParams == 6:  
            Color(0.2,0.2,0.2,OPAQUE, mode="rgba")
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
        if self.inputExists is True:
            temp = list(self.input.pos)
            if moveX:
                temp[X] = touch.pos[0] + 0
            if moveY:
                temp[Y] = touch.pos[1] + 20
            self.input.pos = tuple(temp)

        if self.outputExists is True:
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

        if self.nParams == 5:  
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

        if self.nParams == 4:  
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

        if self.nParams == 3:  
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
            
        if self.nParams == 2:  
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

        if self.nParams == 1: 
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
                    if len(blocks) == 1:#if is only this block in the list             
                        self.rect.pos = touch.pos
                        self.label.pos[X] = touch.pos[X]
                        self.label.pos[Y] = touch.pos[Y] - (self.rect.size[Y]/2)
                        self.move_connectors(touch,1,1)
                    else:  # check for block-block collisions  
                        for secondBlock in blocks:              
                            if self.label.text is not secondBlock.label.text: # dont compare a block with itself
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
    def release_block(self):
        self.selected = RELEASED 

    #------------------------------------------- is_touch_detected
    def is_touch_detected(self,touch,moving):
        if touch.pos[X] > self.rect.pos[X] and touch.pos[X] < (self.rect.pos[X] + self.rect.size[X]):
            if touch.pos[1] > self.rect.pos[Y] and touch.pos[Y] < (self.rect.pos[Y] + self.rect.size[Y]):
                if moving == STILL:
                    self.selected = SELECTED

    #------------------------------------------- is_collision
    def is_collision(self,secondBlock):
        if self.rect.pos[X] < secondBlock.rect.pos[X] + BLOCK_WIDTH + THRESH:        
            if self.rect.pos[X] + BLOCK_WIDTH > secondBlock.rect.pos[X] - THRESH:
                if self.rect.pos[Y] < secondBlock.rect.pos[Y] + BLOCK_HEIGHT + THRESH:        
                    if self.rect.pos[Y] + BLOCK_HEIGHT > secondBlock.rect.pos[Y] - THRESH:
                        return COLLISION
        return NO_COLLISION                


#========================================================================        
#============================Click=======================================
#========================================================================
class Click(Widget):
    
    def __init__(self, **kwargs):
        super(Click, self).__init__(**kwargs)
        self.blocks = []

    def assign_block(self,name,inputNode,outputNode,nParams):
        with self.canvas:
            nameCounter = 1
            create_block = 0
            temp = name + " " + str(nameCounter)

            if not self.blocks:
                block = Block(temp,inputNode,outputNode,nParams)
                self.blocks.append(block)
            else:
                while not create_block:
                    for block in self.blocks: 
                        temp = name + " " + str(nameCounter)
                        if temp[:-1] == block.label.text[:-1]: # if word match 
                            if temp[-1] <= block.label.text[-1]:
                                create_block = 0
                                nameCounter = nameCounter + 1
                            if temp[-1] > block.label.text[-1]:
                                create_block = 1              
                        else:
                            create_block = 1
                block = Block(temp,inputNode,outputNode,nParams)
                self.blocks.append(block)

    def on_touch_down(self, touch):
        self.detect_collisions(touch, STILL)
            
    def on_touch_move(self, touch):
        self.detect_collisions(touch, MOVING)

        for block in self.blocks:
            block.move_block(touch,self.blocks)

    def on_touch_up(self,touch):
        for block in self.blocks:
            block.release_block()

    def detect_collisions(self, touch, moving):
        for block in self.blocks:
            if block.is_touch_detected(touch,moving): 
                return

#========================================================================        
#===========================FXCoreDesignerApp============================
#========================================================================
class FXCoreDesignerApp(App):

    def build(self):

        Window.size = (1200, 800)

        click = Click() 

        layout = GridLayout(cols = 4, row_force_default = True, row_default_height = BUTTON_HEIGHT)
        
        #--------------------------------IOdrop
        IOdrop = DropDown()
        inBtn = Button(text ='Input', size_hint_y = None, height = BUTTON_HEIGHT)
        inBtn.bind(on_release = lambda none: click.assign_block('Input',0,1,0))
        IOdrop.add_widget(inBtn)
        #
        outBtn = Button(text ='Output', size_hint_y = None, height = BUTTON_HEIGHT)
        outBtn.bind(on_release = lambda none: click.assign_block('Output',1,0,0))
        IOdrop.add_widget(outBtn)
        
        #--------------------------------FXdrop
        FXdrop = DropDown()
        reverbBtn = Button(text ='Reverb', size_hint_y = None, height = BUTTON_HEIGHT)
        reverbBtn.bind(on_release = lambda none: click.assign_block('Reverb',1,1,6))
        FXdrop.add_widget(reverbBtn)
        #
        delayBtn = Button(text ='Delay', size_hint_y = None, height = BUTTON_HEIGHT)
        delayBtn.bind(on_release = lambda none: click.assign_block('Delay',1,1,5))
        FXdrop.add_widget(delayBtn)

        #--------------------------------Routingdrop
        Routingdrop = DropDown()
        splitterBtn = Button(text ='Splitter', size_hint_y = None, height = BUTTON_HEIGHT)
        splitterBtn.bind(on_release = lambda none: click.assign_block('Splitter',1,1,4))
        Routingdrop.add_widget(splitterBtn)
        #
        mixerBtn = Button(text ='Mixer', size_hint_y = None, height = BUTTON_HEIGHT)
        mixerBtn.bind(on_release = lambda none: click.assign_block('Mixer',1,1,3))
        Routingdrop.add_widget(mixerBtn)

        #--------------------------------AnalysisDrop
        AnalysisDrop = DropDown()
        FFTBtn = Button(text ='FFT', size_hint_y = None, height = BUTTON_HEIGHT)
        FFTBtn.bind(on_release = lambda  none: click.assign_block('FFT',1,1,1))
        # then add the button inside the dropdown
        AnalysisDrop.add_widget(FFTBtn)
        #
        envelopeFollowerBtn = Button(text ='Envelope Follower', size_hint_y = None, height = BUTTON_HEIGHT)
        envelopeFollowerBtn.bind(on_release = lambda  none: click.assign_block('Envelope Follower',1,1,1))
        AnalysisDrop.add_widget(envelopeFollowerBtn)
        
        #--------------------------------
        IObutton = Button(text ='IO')
        IObutton.bind(on_release = IOdrop.open)
        FXbutton = Button(text ='FX')
        FXbutton.bind(on_release = FXdrop.open)
        RoutingButton = Button(text ='Routing')
        RoutingButton.bind(on_release = Routingdrop.open)
        AnalysisButton = Button(text ='Analysis')
        AnalysisButton.bind(on_release = AnalysisDrop.open)

        layout.add_widget(IObutton)
        layout.add_widget(FXbutton)
        layout.add_widget(RoutingButton)
        layout.add_widget(AnalysisButton)
        layout.add_widget(click)

        return layout

if __name__ == '__main__':
    FXCoreDesignerApp().run()
