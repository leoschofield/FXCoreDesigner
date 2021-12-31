## LeoSchofield 31/12/2021

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.graphics import Rectangle, Color, Line, Ellipse
from kivy.core.window import Window
import random

MOVING = 1
STILL = 0

SELECTED = 1 
RELEASED = 0

OPAQUE = 1 

X = 0
Y = 1 


#========================================================================        
#============================Block=======================================
#========================================================================
class Block(Widget):
    def __init__(self,name,inputNode,outputNode,nParams, **kwargs):
        super(Block, self).__init__(**kwargs)
        self.Xpos = random.randrange(200, 1000)
        self.Ypos = random.randrange(100, 600)
        Color(0.4,0.4,0.4,OPAQUE, mode="rgba")
        #self.rect = Rectangle(pos=(0,0), size=(100,50))
        self.rect = Rectangle(pos=(self.Xpos,self.Ypos), size=(100,50))
        #Color(0.5,0.4,0.2,OPAQUE, mode="rgba")
        #self.line = Line(points=[0, 0, 100, 0, 100, 50,0,50,0,0], width=3)
        self.label = Label(pos=(self.Xpos,self.Ypos - (self.rect.size[Y]/2)),text= name)

        self.selected = RELEASED
        self.nParams = nParams
        self.inputExists = 0 
        self.outputExists = 0

        if inputNode:
            Color(0.2,0.2,0.2,OPAQUE, mode="rgba")
            self.input = Rectangle(pos=(self.Xpos,self.Ypos+20), size=(5,10))
            self.inputExists = True

        if outputNode:
            Color(0.2,0.2,0.2,OPAQUE, mode="rgba")
            self.output = Rectangle(pos=(self.Xpos+95,self.Ypos+20), size=(5,10))
            self.outputExists = True

        if self.nParams is 6:  
            Color(0.2,0.2,0.2,OPAQUE, mode="rgba")
            self.param1Con = Rectangle(pos=(self.Xpos+15,self.Ypos+45), size=(10,5))
            self.param2Con = Rectangle(pos=(self.Xpos+45,self.Ypos+45), size=(10,5))
            self.param3Con = Rectangle(pos=(self.Xpos+75,self.Ypos+45), size=(10,5))
            self.param4Con = Rectangle(pos=(self.Xpos+15,self.Ypos), size=(10,5))
            self.param5Con = Rectangle(pos=(self.Xpos+45,self.Ypos), size=(10,5))
            self.param6Con = Rectangle(pos=(self.Xpos+75,self.Ypos), size=(10,5))
        elif self.nParams is 5:
            self.param1Con = Rectangle(pos=(self.Xpos+15,self.Ypos+45), size=(10,5))
            self.param2Con = Rectangle(pos=(self.Xpos+45,self.Ypos+45), size=(10,5))
            self.param3Con = Rectangle(pos=(self.Xpos+75,self.Ypos+45), size=(10,5))
            self.param4Con = Rectangle(pos=(self.Xpos+30,self.Ypos), size=(10,5))
            self.param5Con = Rectangle(pos=(self.Xpos+60,self.Ypos), size=(10,5))
        elif self.nParams is 4:
            self.param1Con = Rectangle(pos=(self.Xpos+30,self.Ypos+45), size=(10,5))
            self.param2Con = Rectangle(pos=(self.Xpos+60,self.Ypos+45), size=(10,5))
            self.param3Con = Rectangle(pos=(self.Xpos+30,self.Ypos), size=(10,5))
            self.param4Con = Rectangle(pos=(self.Xpos+60,self.Ypos), size=(10,5))
        elif self.nParams is 3:
            self.param1Con = Rectangle(pos=(self.Xpos+30,self.Ypos+45), size=(10,5))
            self.param2Con = Rectangle(pos=(self.Xpos+60,self.Ypos+45), size=(10,5))
            self.param3Con = Rectangle(pos=(self.Xpos+45,self.Ypos), size=(10,5))
        elif self.nParams is 2:
            self.param1Con = Rectangle(pos=(self.Xpos+30,self.Ypos+45), size=(10,5))
            self.param2Con = Rectangle(pos=(self.Xpos+60,self.Ypos+45), size=(10,5))
        elif self.nParams is 1:
            self.param1Con = Rectangle(pos=(self.Xpos+45,self.Ypos+45), size=(10,5))
 

    #======================================================================== move_connectors
    def move_connectors(self,touch):
        if self.inputExists is True:
            temp = list(self.input.pos)
            temp[X] = touch.pos[0] + 0
            temp[Y] = touch.pos[1] + 20
            self.input.pos = tuple(temp)


        if self.outputExists is True:
            temp = list(self.output.pos)
            temp[X] = touch.pos[0] + 95
            temp[Y] = touch.pos[1] + 20
            self.output.pos = tuple(temp)


        if self.nParams is 6:  
            temp = list(self.param1Con.pos)
            temp[X] = touch.pos[0] + 15
            temp[Y] = touch.pos[1] + 45
            self.param1Con.pos = tuple(temp)

            temp = list(self.param2Con.pos)
            temp[X] = touch.pos[0] + 45
            temp[Y] = touch.pos[1] + 45
            self.param2Con.pos = tuple(temp)

            self.param3Con.pos = touch.pos
            temp = list(self.param3Con.pos)
            temp[X] = touch.pos[0] + 75
            temp[Y] = touch.pos[1] + 45
            self.param3Con.pos = tuple(temp)

            self.param4Con.pos = touch.pos
            temp = list(self.param4Con.pos)
            temp[X] = touch.pos[0] + 15
            temp[Y] = touch.pos[1] + 0
            self.param4Con.pos = tuple(temp)

            self.param5Con.pos = touch.pos
            temp = list(self.param5Con.pos)
            temp[X] = touch.pos[0] + 45
            temp[Y] = touch.pos[1] + 0
            self.param5Con.pos = tuple(temp)

            self.param6Con.pos = touch.pos
            temp = list(self.param6Con.pos)
            temp[X] = touch.pos[0] + 75
            temp[Y] = touch.pos[1] + 0
            self.param6Con.pos = tuple(temp)


        if self.nParams is 5:  
            temp = list(self.param1Con.pos)
            temp[X] = touch.pos[0] + 15
            temp[Y] = touch.pos[1] + 45
            self.param1Con.pos = tuple(temp)

            temp = list(self.param2Con.pos)
            temp[X] = touch.pos[0] + 45
            temp[Y] = touch.pos[1] + 45
            self.param2Con.pos = tuple(temp)

            self.param3Con.pos = touch.pos
            temp = list(self.param3Con.pos)
            temp[X] = touch.pos[0] + 75
            temp[Y] = touch.pos[1] + 45
            self.param3Con.pos = tuple(temp)

            self.param4Con.pos = touch.pos
            temp = list(self.param4Con.pos)
            temp[X] = touch.pos[0] + 30
            temp[Y] = touch.pos[1] + 0
            self.param4Con.pos = tuple(temp)

            self.param5Con.pos = touch.pos
            temp = list(self.param5Con.pos)
            temp[X] = touch.pos[0] + 60
            temp[Y] = touch.pos[1] + 0
            self.param5Con.pos = tuple(temp)    


        if self.nParams is 4:  
            temp = list(self.param1Con.pos)
            temp[X] = touch.pos[0] + 30
            temp[Y] = touch.pos[1] + 45
            self.param1Con.pos = tuple(temp)

            temp = list(self.param2Con.pos)
            temp[X] = touch.pos[0] + 60
            temp[Y] = touch.pos[1] + 45
            self.param2Con.pos = tuple(temp)

            self.param3Con.pos = touch.pos
            temp = list(self.param3Con.pos)
            temp[X] = touch.pos[0] + 30
            temp[Y] = touch.pos[1] + 0
            self.param3Con.pos = tuple(temp)

            self.param4Con.pos = touch.pos
            temp = list(self.param4Con.pos)
            temp[X] = touch.pos[0] + 60
            temp[Y] = touch.pos[1] + 0
            self.param4Con.pos = tuple(temp)


        if self.nParams is 3:  
            temp = list(self.param1Con.pos)
            temp[X] = touch.pos[0] + 30
            temp[Y] = touch.pos[1] + 45
            self.param1Con.pos = tuple(temp)

            temp = list(self.param2Con.pos)
            temp[X] = touch.pos[0] + 60
            temp[Y] = touch.pos[1] + 45
            self.param2Con.pos = tuple(temp)

            self.param3Con.pos = touch.pos
            temp = list(self.param3Con.pos)
            temp[X] = touch.pos[0] + 45
            temp[Y] = touch.pos[1] + 0
            self.param3Con.pos = tuple(temp)
            
        if self.nParams is 2:  
            temp = list(self.param1Con.pos)
            temp[X] = touch.pos[0] + 30
            temp[Y] = touch.pos[1] + 45
            self.param1Con.pos = tuple(temp)

            temp = list(self.param2Con.pos)
            temp[X] = touch.pos[0] + 60
            temp[Y] = touch.pos[1] + 45
            self.param2Con.pos = tuple(temp)

        if self.nParams is 1:  
            temp = list(self.param1Con.pos)
            temp[X] = touch.pos[0] + 45
            temp[Y] = touch.pos[1] + 45
            self.param1Con.pos = tuple(temp)


    #========================================================================select_block
    def select_block(self,touch):
        if self.selected is SELECTED:
            if touch.pos[0] + self.rect.size[0] < 1200:
                if touch.pos[1] + self.rect.size[1] < 770:
                    self.rect.pos = touch.pos
                    #Color(0.5,0.4,0.2,OPAQUE, mode="rgba")
                    #self.line = Line(points=[touch.pos[0], touch.pos[1],touch.pos[0]+100, touch.pos[1],touch.pos[0]+100,touch.pos[1] + 50,touch.pos[0],touch.pos[1] + 50,touch.pos[0],touch.pos[1]], width=3)
                    self.label.pos[X] = touch.pos[X]
                    self.label.pos[Y] = touch.pos[Y] - (self.rect.size[Y]/2)
    
                    self.move_connectors(touch)

                    #print("Selected block",touch)


    #========================================================================move_block
    def move_block(self,touch):
        if self.selected == SELECTED:
            if touch.pos[0] + self.rect.size[0] < 1200:
                if touch.pos[1] + self.rect.size[1] < 770:
                    self.rect.pos = touch.pos
                    #Color(0.5,0.4,0.2,OPAQUE, mode="rgba")
                    #self.line = Line(points=[touch.pos[0], touch.pos[1],touch.pos[0]+100, touch.pos[1],touch.pos[0]+100,touch.pos[1] + 50,touch.pos[0],touch.pos[1] + 50,touch.pos[0],touch.pos[1]], width=3)
                    self.label.pos[X] = touch.pos[X]
                    self.label.pos[Y] = touch.pos[Y] - (self.rect.size[Y]/2)

                    self.move_connectors(touch)

    #========================================================================release_block
    def release_block(self,touch):
        #print("Released block",touch)
        self.selected = RELEASED 

    #========================================================================is_touch_detected
    def is_touch_detected(self,touch,moving):
        if touch.pos[X] > self.rect.pos[X] and touch.pos[X] < (self.rect.pos[X] + self.rect.size[X]):
            if touch.pos[1] > self.rect.pos[Y] and touch.pos[Y] < (self.rect.pos[Y] + self.rect.size[Y]):
                if moving == STILL:
                    self.selected = SELECTED 
                #print("collision")
            else:
                pass
                #print("no collision")   
        else:
            pass
            #print("no collision")



#========================================================================        
#============================Click=======================================
#========================================================================
class Click(Widget):
    def assign_block(self,name,inputNode,outputNode,nParams):
        with self.canvas:
            block = Block(name,inputNode,outputNode,nParams)
            self.blocks.append(block)
            #print("created block")
            print(self.blocks)

    def __init__(self, **kwargs):
        super(Click, self).__init__(**kwargs)
        #self.block_manager = block_manager
        self.blocks = []

    def on_touch_down(self, touch):
        self.detect_collisions(touch, STILL)

        for block in self.blocks:
            block.select_block(touch)
            
    def on_touch_move(self, touch):
        self.detect_collisions(touch, MOVING)

        for block in self.blocks:
            block.move_block(touch)

    def on_touch_up(self,touch):
        for block in self.blocks:
            block.release_block(touch)

    def detect_collisions(self, touch, moving):
        for block in self.blocks:
            if block.is_touch_detected(touch,moving) == MOVING:## this may need fixing
                return
            ## todo need efficient block-block collision detection!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#========================================================================        
#========================FXCoreApp=======================================
#========================================================================
class FXCoreDesignerApp(App):

    def build(self):

        Window.size = (1200, 800)

        click = Click() 

        layout = GridLayout(cols = 4, row_force_default = True,
                            row_default_height = 30)
        
        #--------------------------------IOdrop
        IOdrop = DropDown()
        inBtn = Button(text ='Input', size_hint_y = None, height = 40)
        inBtn.bind(on_release = lambda none: click.assign_block('Input',0,1,0))
        IOdrop.add_widget(inBtn)
        #
        outBtn = Button(text ='Output', size_hint_y = None, height = 40)
        outBtn.bind(on_release = lambda none: click.assign_block('Output',1,0,0))
        IOdrop.add_widget(outBtn)

        #--------------------------------FXdrop
        FXdrop = DropDown()
        reverbBtn = Button(text ='Reverb', size_hint_y = None, height = 40)
        reverbBtn.bind(on_release = lambda none: click.assign_block('Reverb',1,1,6))
        FXdrop.add_widget(reverbBtn)
        #
        delayBtn = Button(text ='Delay', size_hint_y = None, height = 40)
        delayBtn.bind(on_release = lambda none: click.assign_block('Delay',1,1,5))
        FXdrop.add_widget(delayBtn)

        #--------------------------------Routingdrop
        Routingdrop = DropDown()
        splitterBtn = Button(text ='Splitter', size_hint_y = None, height = 40)
        splitterBtn.bind(on_release = lambda none: click.assign_block('Splitter',1,1,4))
        Routingdrop.add_widget(splitterBtn)
        #
        mixerBtn = Button(text ='Mixer', size_hint_y = None, height = 40)
        mixerBtn.bind(on_release = lambda none: click.assign_block('Mixer',1,1,3))
        Routingdrop.add_widget(mixerBtn)

        #--------------------------------AnalysisDrop
        AnalysisDrop = DropDown()
        FFTBtn = Button(text ='FFT', size_hint_y = None, height = 40)
        FFTBtn.bind(on_release = lambda  none: click.assign_block('FFT',1,1,1))
        # then add the button inside the dropdown
        AnalysisDrop.add_widget(FFTBtn)
        #
        envelopeFollowerBtn = Button(text ='Envelope Follower', size_hint_y = None, height = 40)
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
