# Leo Schofield 01/01/2022
from xml.dom.minicompat import NodeList
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.core.window import Window
from click_class import Click
from asm_node_class import asm_node
from config import blocks 
import os

BUTTON_HEIGHT = 30

DONT_ASSIGN_LINE = 0
ASSIGN_LINE = 1

DRAG_MODE0 = 0
DRAG_MODE1 = 1

X = 0
Y = 1 

TRUE = 1
FALSE = 0

SELECTED = 1 
RELEASED = 0

DRAGGING = 1
NOT_DRAGGING = 0

MIXER = 20
SPLITTER = 30

class popUpParamLabel(Widget):
    def __init__(self,**kwargs):
        super(popUpParamLabel, self).__init__(**kwargs)
        with self.canvas:
            self.paramlabel = Label(pos=(0, 0),text="")
        self.released = 1

    def destroy_label(self):
        with self.canvas:
            self.paramlabel.text =""
            self.released = 1

    def update_label(self,mousepos,name):
        with self.canvas:
            if self.released == 1:
                self.paramlabel.pos=(mousepos[X]-50, mousepos[Y]+20)
                self.paramlabel.text=name
                self.released = 0


class myMousePos():
    def __init__(self):
        self.pos = [0,0]

class FXCoreDesignerApp(App):
    def build(self):
        #self.isOverlay = 0
        Window.size = (1920, 1080)
        #Window.fullscreen = 'auto'
        Window.bind(mouse_pos=self.on_mouse_pos)
        Window.bind(on_key_down=self.key_action)   
        self.popUpLabel = popUpParamLabel()
        self.click = Click() 
        self.layout = GridLayout(cols = 12, row_force_default = True, row_default_height = BUTTON_HEIGHT)
        
        #--------------------------------IOdrop
        IOdrop = DropDown()
        #
        inBtn = Button(text ='Input', size_hint_y = None, height = BUTTON_HEIGHT)
        inBtn.bind(on_release = lambda none: self.click.assign_block('Input',0,1,0))
        IOdrop.add_widget(inBtn)
        #
        outBtn = Button(text ='Output', size_hint_y = None, height = BUTTON_HEIGHT)
        outBtn.bind(on_release = lambda none: self.click.assign_block('Output',1,0,0))
        IOdrop.add_widget(outBtn)
        
        #--------------------------------FXdrop
        FXdrop = DropDown()
        #
        reverbBtn = Button(text ='Reverb', size_hint_y = None, height = BUTTON_HEIGHT)
        reverbBtn.bind(on_release = lambda none: self.click.assign_block('Reverb',1,1,6))
        FXdrop.add_widget(reverbBtn)
        #
        delayBtn = Button(text ='Delay', size_hint_y = None, height = BUTTON_HEIGHT)
        delayBtn.bind(on_release = lambda none: self.click.assign_block('Delay',1,1,5))
        FXdrop.add_widget(delayBtn)

        #Chorus
        chorusBtn = Button(text ='Chorus', size_hint_y = None, height = BUTTON_HEIGHT)
        chorusBtn.bind(on_release = lambda none: self.click.assign_block('Chorus',1,1,4))
        FXdrop.add_widget(chorusBtn)

        #Tremelo
        tremoloBtn = Button(text ='Tremelo', size_hint_y = None, height = BUTTON_HEIGHT)
        tremoloBtn.bind(on_release = lambda none: self.click.assign_block('Tremelo',1,1,3))
        FXdrop.add_widget(tremoloBtn)

        #Distortion
        distBtn = Button(text ='Distortion', size_hint_y = None, height = BUTTON_HEIGHT)
        distBtn.bind(on_release = lambda none: self.click.assign_block('Distortion',1,1,4))
        FXdrop.add_widget(distBtn)

        #Pitch Shift
        pitchBtn = Button(text ='Pitch Shifter', size_hint_y = None, height = BUTTON_HEIGHT)
        pitchBtn.bind(on_release = lambda none: self.click.assign_block('Pitch',1,1,3))
        FXdrop.add_widget(pitchBtn)

        #Looper
        looperBtn = Button(text ='Looper', size_hint_y = None, height = BUTTON_HEIGHT)
        looperBtn.bind(on_release = lambda none: self.click.assign_block('Looper',1,1,2))
        FXdrop.add_widget(looperBtn)
        #--------------------------------AnalysisDrop
        AnalysisDrop = DropDown()
        #
        FFTBtn = Button(text ='FFT', size_hint_y = None, height = BUTTON_HEIGHT)
        FFTBtn.bind(on_release = lambda  none: self.click.assign_block('FFT',1,1,2))
        AnalysisDrop.add_widget(FFTBtn)
        #
        envelopeFollowerBtn = Button(text ='Envelope', size_hint_y = None, height = BUTTON_HEIGHT)
        envelopeFollowerBtn.bind(on_release = lambda  none: self.click.assign_block('Envelope',1,1,1))
        AnalysisDrop.add_widget(envelopeFollowerBtn)
        
        #--------------------------------ControlsDrop
        ControlsDrop = DropDown()
        # 
        PotentiomenterBtn = Button(text ='Potentiometer', size_hint_y = None, height = BUTTON_HEIGHT)
        PotentiomenterBtn.bind(on_release = lambda  none: self.click.assign_block('Pot',0,0,1))
        ControlsDrop.add_widget(PotentiomenterBtn)
        #
        ConstantBtn = Button(text ='Constant', size_hint_y = None, height = BUTTON_HEIGHT)
        ConstantBtn.bind(on_release = lambda  none: self.click.assign_block('Constant',0,0,1))
        ControlsDrop.add_widget(ConstantBtn)
        #
        TapTempoBtn = Button(text ='Tap Tempo', size_hint_y = None, height = BUTTON_HEIGHT)
        TapTempoBtn.bind(on_release = lambda  none: self.click.assign_block('Tap Tempo',0,0,1))
        ControlsDrop.add_widget(TapTempoBtn)
        #
        ToggleBtn = Button(text ='Switch', size_hint_y = None, height = BUTTON_HEIGHT)
        ToggleBtn.bind(on_release = lambda  none: self.click.assign_block('Switch',0,0,1))
        ControlsDrop.add_widget(ToggleBtn)

        #--------------------------------Routingdrop
        RoutingDrop = DropDown()
        #
        splitterBtn = Button(text ='Splitter', size_hint_y = None, height = BUTTON_HEIGHT)
        splitterBtn.bind(on_release = lambda none: self.click.assign_block('Splitter',1,0,SPLITTER))
        RoutingDrop.add_widget(splitterBtn)
        #
        mixerBtn = Button(text ='Mixer', size_hint_y = None, height = BUTTON_HEIGHT)
        mixerBtn.bind(on_release = lambda none: self.click.assign_block('Mixer',0,1,MIXER))
        RoutingDrop.add_widget(mixerBtn)

        #-------------------------------- Buttons For Dropdowns
        IObutton = Button(text ='IO')
        IObutton.bind(on_release = IOdrop.open)
        #
        FXbutton = Button(text ='FX')
        FXbutton.bind(on_release = FXdrop.open)
        #
        AnalysisButton = Button(text ='Analysis')
        AnalysisButton.bind(on_release = AnalysisDrop.open)
        #
        ControlsButton = Button(text ='Controls')
        ControlsButton.bind(on_release = ControlsDrop.open)
        #
        RoutingButton = Button(text ='Routing')
        RoutingButton.bind(on_release = RoutingDrop.open)

        #--------------------------------
        CodeButton = Button(text ='Generate Code')
        CodeButton.bind(on_release =  lambda none: self.generate_asm())

        #--------------------------------
        ClearButton = Button(text ='Clear Screen')
        ClearButton.bind(on_release = lambda none: self.clear_screen())
        
        #--------------------------------
        SaveButton = Button(text ='Save Patch')
        #SaveButton.bind(on_release = lambda none: self.
        #--------------------------------
        LoadButton = Button(text ='Load Patch')
        #LoadButton.bind(on_release = lambda none: self.
        #--------------------------------
        RunButton = Button(text ='Run From RAM')
        #RunButton.bind(on_release = lambda none: self.

        #--------------------------------
        ProgButton = Button(text ='Load to Flash')
        #ProgButton.bind(on_release = lambda none: self.

        #--------------------------------
        AboutButton = Button(text ='About')
        popup = Popup(title='FXCoreDesigner - Leo Schofield 2022',
        content=Label(text='                             Simplifies developing programs for the FXCore DSP from Experimental Noize                                                          Instructions: Click a dropdown button to select a block, link other blocks with lines by clicking in the light grey connectors on each block, green lines are for audio signals, purple lines are for control signals. Press d when dragging a block to delete that block and its lines.             Press d when dragging a line to delete that line.',text_size=(380,300)),
        size_hint=(None, None), size=(400,0))

        AboutButton.bind(on_release = lambda none: popup.open())
    
        #---------------------------------------------
        self.layout.add_widget(IObutton)
        self.layout.add_widget(FXbutton)
        self.layout.add_widget(AnalysisButton)
        self.layout.add_widget(ControlsButton)
        self.layout.add_widget(RoutingButton)
        self.layout.add_widget(CodeButton)
        self.layout.add_widget(SaveButton)
        self.layout.add_widget(LoadButton)
        self.layout.add_widget(ClearButton)
        self.layout.add_widget(RunButton)
        self.layout.add_widget(ProgButton)
        self.layout.add_widget(AboutButton)
        self.layout.add_widget(self.popUpLabel)
        self.layout.add_widget(self.click)
    
        return self.layout


   #------------------------------------------- mouse hover event
    def key_action(self, *args):
        global blocks
        # print("got a key event: %s" % list(args))
        if args[3] == 'd':
            for block in blocks:
                    if block.selected == 1:
                        block.remove_block()#remove block/connector graphics
                        for line in block.conLines:
                            line.remove_line()
                            block.conLines.remove(line)
                        for block2 in blocks:
                            for line in block2.conLines:
                                if line.start_block.name == block.name:
                                    line.remove_line()
                                    block2.conLines.remove(line)
                                elif line.end_block.name == block.name:
                                    line.remove_line()
                                    block2.conLines.remove(line)
                        blocks.remove(block)
                        # for block in blocks:
                        #     print(block.label.text)
                    else:
                        for line in block.conLines:#search for dragging lines
                            if line.dragging == DRAGGING:
                                line.dragging = NOT_DRAGGING
                                block.conLines.remove(line)
                                line.remove_line()
  #------------------------------------------- mouse hover event
    def on_mouse_pos(self, window, mousepos):
        myPos = myMousePos() 
        
        if blocks != []:
            for block in blocks:
                if block.selected == RELEASED:
                    myPos.pos[X] = mousepos[0]
                    myPos.pos[Y] = mousepos[1]
                    readConnector = block.is_inside_connector(myPos,DONT_ASSIGN_LINE)
                    if readConnector != 0:
                        self.popUpLabel.update_label(mousepos,block.get_connector_name(readConnector))
                        return
                    else:
                        self.popUpLabel.destroy_label()

                if block.conLines != []:
                    for conLine in block.conLines:
                        if conLine.dragging == DRAGGING:# when first dragging the line keep hold of it until clicked in block or deleted
                            conLine.drag_line(mousepos,DRAG_MODE1)

    #-------------------------------------------clear_screen
    def clear_screen(self):
        box = BoxLayout(orientation = 'vertical', padding = (10))
        btn1 = Button(text = "No")
        btn2 = Button(text = "Yes")
        box.add_widget(btn1)
        box.add_widget(btn2)
        popup = Popup(title="Clear Screen? Can't Undo!", title_size= (30), 
                title_align = 'center', content = box,
                size_hint=(None, None), size=(400, 400),
                auto_dismiss = True)
        btn1.bind(on_press = popup.dismiss)
        btn2.bind(on_press = lambda none:self.clear_screen2(popup))
        popup.open()

    #-------------------------------------------clear_screen2
    def clear_screen2(self,popup):       
        global blocks
        blocks = []
        self.layout.remove_widget(self.click)
        self.click = Click()
        self.layout.add_widget(self.click)
        popup.dismiss()

    #-------------------------------------------
    def recursive_add_nodes(self,node,prev_node):
        for conline in node.block.conLines:
            if conline.start_block.name == node.block.name:#if a new line ends on the current block
                if conline.end_block.name != prev_node.block.name:#dont add an existing line
                    new_node = asm_node(conline.end_block)   
                    if conline.start_connector == 1: 
                        prev_node.add_control(conline.end_connector,1,conline.end_block.ID)
                    elif conline.end_connector == 1:     
                        prev_node.add_control(conline.start_connector,1,conline.end_block.ID)        
                    else:
                        self.asm_nodes.append(new_node)
                        self.recursive_add_nodes(new_node,node)
                    
            elif conline.end_block.name == node.block.name: #if a new line ends on the current block
                if conline.start_block.name != prev_node.block.name:#dont add an existing line
                    new_node = asm_node(conline.start_block)   
                    if conline.start_connector == 1: 
                        prev_node.add_control(conline.end_connector,1,conline.start_block.ID)
                    elif conline.end_connector == 1:  
                        prev_node.add_control(conline.start_connector,1,conline.start_block.ID)        
                    else:
                        self.asm_nodes.append(new_node)
                        self.recursive_add_nodes(new_node,node)

    #-------------------------------------------generate_asm
    def generate_asm(self):
        self.asm_nodes = []
        asm_string = ""
        directive_string = ""
        loop = 1
        while loop:
            for block in blocks:#loop through blocks until a start block is found
                if block.conLines != []:
                    if 'Input' in block.name: # start building the graph from the input   !!TODO!! signal generators can start a graph too
                            input_node = asm_node(block)    
                            self.asm_nodes.append(input_node)#add input to list

                            for conline in block.conLines: # continue building from connected conline
                                if conline.start_block.name != block.name: #input block isnt the connector start block so add the start block
                                    new_node = asm_node(conline.start_block)   
                                    self.asm_nodes.append(new_node)
                                    self.recursive_add_nodes(new_node,input_node)

                                elif conline.end_block.name != block.name:#input block isnt the connector end block so add the end block
                                    new_node = asm_node(conline.end_block)    
                                    self.asm_nodes.append(new_node)
                                    self.recursive_add_nodes(new_node,input_node)                    
                        

                    # else:# if not an Input block, continue building
                    #     for node in asm_nodes:#build from next node
                    #         if node.name == block.name:#if node matches block has been added already then continue and add connected blocks  
                    #             for conLine in block.conLines: #loop through blocks connector lines to find connected blocks 
                    #                 already_added = FALSE
                    #                 if conLine.start_block != block.name:# don't add the same block again 
                    #                     #if 'Input' not in conLine.start_block:       
                    #                     if conLine.start_connector == 11: #if this is an input connector
                    #                         ser_position = ser_position + 1       
                    #                         new_node = asm_node(conLine.start_block,ser_position,par_position)
                    #                         for node in asm_nodes:#check new node hasnt already been added
                    #                             if new_node.name == node.name:
                    #                                 already_added = TRUE
                    #                                 break
                    #                         if already_added == FALSE:     
                    #                             if "Output" in new_node.name:
                    #                                 series_lock = 0                                                  
                    #                             asm_nodes.append(new_node) # add to list so that graph can be built further
                    #                     elif conLine.start_connector == 10: #if this is an output connector
                    #                         ser_position = ser_position + 1       
                    #                         new_node = asm_node(conLine.start_block,ser_position,par_position)
                    #                         for node in asm_nodes:#check new node hasnt already been added
                    #                             if new_node.name == node.name:
                    #                                 already_added = TRUE
                    #                                 break
                    #                         if already_added == FALSE:                                                       
                    #                             asm_nodes.append(new_node) # add to list so that graph can be built further
                    #                     elif conLine.start_connector == 1:#if this is a control connector
                    #                         for block2 in blocks:# find the block which matches the connector's start block name
                    #                             if conLine.start_block == block2.name:
                    #                                 node.add_control(conLine.end_connector,1,block2.ID)

                    #                 elif conLine.end_block != block.name:# don't add the same block again
                    #                     #if 'Input' not in conLine.end_block:       
                    #                     if conLine.end_connector == 11: #if this is an input connector
                    #                         ser_position = ser_position + 1
                    #                         new_node = asm_node(conLine.end_block,ser_position,par_position)
                    #                         for node in asm_nodes:#check new node hasnt already been added
                    #                             if new_node.name == node.name:
                    #                                 already_added = TRUE
                    #                                 break
                    #                         if already_added == FALSE:   
                    #                             if "Output" in new_node.name:
                    #                                 series_lock = 0                                                        
                    #                             asm_nodes.append(new_node) # add to list so that graph can be built further
                    #                     elif conLine.end_connector == 10: #if this is an output connector
                    #                         ser_position = ser_position + 1
                    #                         new_node = asm_node(conLine.end_block,ser_position,par_position)
                    #                         for node in asm_nodes:#check new node hasnt already been added
                    #                             if new_node.name == node.name:
                    #                                 already_added = TRUE
                    #                                 break
                    #                         if already_added == FALSE:                                                       
                    #                             asm_nodes.append(new_node) # add to list so that graph can be built further
                    #                     elif conLine.end_connector == 1:#if this is a control connector (POT, etc)
                    #                         # print("\n\n\n\nconLine.end_connector:",conLine.end_block,conLine.end_connector,"\n\n")
                    #                         for block2 in blocks:# find the block which matches the connector's end block name
                    #                             if conLine.end_block == block2.name:
                    #                                 node.add_control(conLine.start_connector,1,block2.ID)
                    #<---end of if not input
            #<---end of for block in blocks
 
        for node in self.asm_nodes:
            print(node.name)
            asm_string += node.asm_string

        print(asm_string)
        
        #********************************************* TODO check number of registers used in asm_string doesnt exceed hardware and create directive_string 
        R0_used = 0
        R1_used = 0
        R2_used = 0
        R3_used = 0
        R4_used = 0
        R5_used = 0
        R6_used = 0
        R7_used = 0
        R8_used = 0
        R9_used = 0
        R10_used = 0
        R11_used = 0
        R12_used = 0
        R13_used = 0
        R14_used = 0
        R15_used = 0

        #     f = open("generated.fxc", 'w')
        #     f.write(asm_string)
        #     f.close()    
        #     os.system('FXCoreCmdAsm.exe -h ')
        
if __name__ == '__main__':
    FXCoreDesignerApp().run()