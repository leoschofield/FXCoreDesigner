# Leo Schofield 01/01/2022
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
import re

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

INPUT = 11
OUTPUT = 10

NUM_COLUMNS = 10

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
        self.registers_used = {
        "r1": 0,
        "r3":  0,
        "r4":  0,
        "r5":  0,
        "r6":  0,
        "r7":  0,
        "r8":  0,
        "r9":  0,
        "r10":  0,
        "r11":  0,
        "r12":  0,
        "r13":  0,
        "r14":  0,
        "r15":  0
        }

        #self.isOverlay = 0
        Window.size = (1920, 1080)
        #Window.fullscreen = 'auto'
        Window.bind(mouse_pos=self.on_mouse_pos)
        Window.bind(on_key_down=self.key_action)   
        self.popUpLabel = popUpParamLabel()
        self.click = Click() 
        self.layout = GridLayout(cols = NUM_COLUMNS, row_force_default = True, row_default_height = BUTTON_HEIGHT)
        
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
        # reverbBtn = Button(text ='Reverb', size_hint_y = None, height = BUTTON_HEIGHT)
        # reverbBtn.bind(on_release = lambda none: self.click.assign_block('Reverb',1,1,6))
        # FXdrop.add_widget(reverbBtn)
        # #
        # delayBtn = Button(text ='Delay', size_hint_y = None, height = BUTTON_HEIGHT)
        # delayBtn.bind(on_release = lambda none: self.click.assign_block('Delay',1,1,5))
        # FXdrop.add_widget(delayBtn)

        # #Chorus
        # chorusBtn = Button(text ='Chorus', size_hint_y = None, height = BUTTON_HEIGHT)
        # chorusBtn.bind(on_release = lambda none: self.click.assign_block('Chorus',1,1,4))
        # FXdrop.add_widget(chorusBtn)

        # #Tremelo
        # tremoloBtn = Button(text ='Tremelo', size_hint_y = None, height = BUTTON_HEIGHT)
        # tremoloBtn.bind(on_release = lambda none: self.click.assign_block('Tremelo',1,1,3))
        # FXdrop.add_widget(tremoloBtn)

        #Distortion
        distBtn = Button(text ='Distortion', size_hint_y = None, height = BUTTON_HEIGHT)
        distBtn.bind(on_release = lambda none: self.click.assign_block('Distortion',1,1,4))
        FXdrop.add_widget(distBtn)

        #Pitch Shift
        pitchBtn = Button(text ='Pitch Shifter', size_hint_y = None, height = BUTTON_HEIGHT)
        pitchBtn.bind(on_release = lambda none: self.click.assign_block('Pitch',1,1,3))
        FXdrop.add_widget(pitchBtn)

        # #Looper
        # looperBtn = Button(text ='Looper', size_hint_y = None, height = BUTTON_HEIGHT)
        # looperBtn.bind(on_release = lambda none: self.click.assign_block('Looper',1,1,2))
        # FXdrop.add_widget(looperBtn)

        #--------------------------------AnalysisDrop
        # AnalysisDrop = DropDown()
        #
        # FFTBtn = Button(text ='FFT', size_hint_y = None, height = BUTTON_HEIGHT)
        # FFTBtn.bind(on_release = lambda  none: self.click.assign_block('FFT',1,1,2))
        # AnalysisDrop.add_widget(FFTBtn)
        #
        # envelopeFollowerBtn = Button(text ='Envelope', size_hint_y = None, height = BUTTON_HEIGHT)
        # envelopeFollowerBtn.bind(on_release = lambda  none: self.click.assign_block('Envelope',1,1,1))
        # AnalysisDrop.add_widget(envelopeFollowerBtn)
        
        #--------------------------------ControlsDrop
        ControlsDrop = DropDown()
        # 
        PotentiomenterBtn = Button(text ='Potentiometer', size_hint_y = None, height = BUTTON_HEIGHT)
        PotentiomenterBtn.bind(on_release = lambda  none: self.click.assign_block('Pot',0,0,1))
        ControlsDrop.add_widget(PotentiomenterBtn)
        #
        # ConstantBtn = Button(text ='Constant', size_hint_y = None, height = BUTTON_HEIGHT)
        # ConstantBtn.bind(on_release = lambda  none: self.click.assign_block('Constant',0,0,1))
        # ControlsDrop.add_widget(ConstantBtn)
        # #
        # TapTempoBtn = Button(text ='Tap Tempo', size_hint_y = None, height = BUTTON_HEIGHT)
        # TapTempoBtn.bind(on_release = lambda  none: self.click.assign_block('Tap Tempo',0,0,1))
        # ControlsDrop.add_widget(TapTempoBtn)
        # #
        # ToggleBtn = Button(text ='Switch', size_hint_y = None, height = BUTTON_HEIGHT)
        # ToggleBtn.bind(on_release = lambda  none: self.click.assign_block('Switch',0,0,1))
        # ControlsDrop.add_widget(ToggleBtn)

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
        # AnalysisButton = Button(text ='Analysis')
        # AnalysisButton.bind(on_release = AnalysisDrop.open)
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
        # RunButton = Button(text ='Run From RAM')
        #RunButton.bind(on_release = lambda none: self.

        #--------------------------------
        ProgButton = Button(text ='Load to Flash')
        #ProgButton.bind(on_release = lambda none: self.

        #--------------------------------
        AboutButton = Button(text ='About')
        popup = Popup(title='FXCoreDesigner v0.1 - Leo Schofield 2023',
        content=Label(text='                             Simplifies developing programs for the FXCore DSP from Experimental Noize                                                          Instructions: Click a dropdown button to select a block, link other blocks with lines by clicking in the light grey connectors on each block, green lines are for audio signals, purple lines are for control signals. Press d when dragging a block to delete that block and its lines.             Press d when dragging a line to delete that line.',text_size=(380,300)),
        size_hint=(None, None), size=(400,0))

        AboutButton.bind(on_release = lambda none: popup.open())
    
        #---------------------------------------------
        self.layout.add_widget(IObutton)
        self.layout.add_widget(FXbutton)
        # self.layout.add_widget(AnalysisButton)
        self.layout.add_widget(ControlsButton)
        self.layout.add_widget(RoutingButton)
        self.layout.add_widget(CodeButton)
        self.layout.add_widget(SaveButton)
        self.layout.add_widget(LoadButton)
        self.layout.add_widget(ClearButton)
        # self.layout.add_widget(RunButton)
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
    def get_free_register(self):
        if self.registers_used["r1"] == 0:
            return 1
        elif self.registers_used["r2"] == 0:
            return 2
        elif self.registers_used["r3"] == 0:
            return 3
        elif self.registers_used["r4"] == 0:
            return 4
        elif self.registers_used["r5"] == 0:
            return 5
        elif self.registers_used["r6"] == 0:
            return 6
        elif self.registers_used["r7"] == 0:
            return 7     
        elif self.registers_used["r8"] == 0:
            return 8      
        elif self.registers_used["r9"] == 0:
            return 9
        elif self.registers_used["r10"] == 0:
            return 10
        elif self.registers_used["r11"] == 0:
            return 11
        elif self.registers_used["r12"] == 0:
            return 12
        elif self.registers_used["r13"] == 0:
            return 13
        elif self.registers_used["r14"] == 0:
            return 14
        elif self.registers_used["r15"] == 0:
            return 15
        return None

    def replace_substrings(self, d, s):
        for k, v in d.items():
            k2 = '$' + k + '$'
            s = s.replace(k2, k + str(v - 1))
        return s

    def add_dicts(self, dict1, dict2):
        for key in dict2.keys():
            dict1[key] = dict1.get(key, 0) + dict2[key]
        return dict1

    def find_names(self, string):
        names_dict = {}
        start_index = 0
        while True:
            start_index = string.find('$', start_index)
            if start_index == -1:
                break
            end_index = string.find('$', start_index + 1)
            if end_index == -1:
                break
            name = string[start_index+1:end_index].split(' ')[0]
            if name not in names_dict:
                names_dict[name] = 1
            start_index = end_index + 1
        return names_dict

    #-------------------------------------------
    def recursive_add_nodes(self,node,prev_node=0):
        if prev_node == 0: # input block condition:
            node.block.conLines.sort(key=lambda x: x.end_connector) # sort list by conline end connector so that control blocks come first
            node.block.conLines.sort(key=lambda x: x.start_connector) # sort list again by conline start connector
            for conline in node.block.conLines: # loop through block connector lines 
                #*****************************************************************************
                if conline.end_block.name != node.block.name: # if conline end isnt this block

                    if 'Splitter' in node.block.name:
                        if(conline.start_connector == SPLITTER + 1): # dont allow the first splitter path to be processed
                            continue

                    if "Mixer" in conline.end_block.name: # mixer block
                        if conline.end_block.usageState == 0: # if this is the first time using this mixer
                            conline.end_block.usageState = 1  # now set it as used
                            node.add_controls_to_asm() # leaving the current node so add its controls
                            node.add_registers_to_asm()
                            self.asm_string += node.asm_string
                            save_reg = self.get_free_register() # get the next free register
                            self.registers_used["r"+str(save_reg)] = conline.end_block.name # set the free register as now used by this block
                            new_node = asm_node(conline.end_block,self.registers_used,conline.end_block.usageState,save_reg,conline.end_connector) 
                            self.asm_nodes.append(new_node)
                            self.asm_string += new_node.asm_string
                            break

                        elif conline.end_block.usageState == 1: # this mixer has previously been used in another path
                            conline.end_block.usageState = 2 # second path using this mixer
                            node.add_controls_to_asm() # leaving the current node so add its controls
                            node.add_registers_to_asm()
                            self.asm_string += node.asm_string
                            for reg in range(1, 15): # loop through registers r1-r15
                                if self.registers_used["r"+str(reg)] == conline.end_block.name: # if register is used by block
                                    new_node = asm_node(conline.end_block,self.registers_used,conline.end_block.usageState,reg,conline.end_connector) #use the register in the weighted sum with the current acc32, get another free register for storing temp values
                                    self.registers_used["r"+str(reg)] = 0 # free register
                                    self.asm_nodes.append(new_node)
                                    conline.end_block.usageState = 3 
                                    self.recursive_add_nodes(new_node,node)
                                    
                    elif "Splitter" in conline.end_block.name: # mixer block
                        if conline.end_block.usageState == 0: # if this is the first time using this splitter
                            conline.end_block.usageState = 1  # now set it as used
                            node.add_controls_to_asm() # leaving the current node so add its controls
                            node.add_registers_to_asm()
                            self.asm_string += node.asm_string
                            save_reg = self.get_free_register() # get the next free register
                            self.registers_used["r"+str(save_reg)] = conline.end_block.name # set the free register as now used by this block
                            new_node = asm_node(conline.end_block,self.registers_used,conline.end_block.usageState,save_reg,conline.end_connector) 
                            self.asm_nodes.append(new_node)
                            self.recursive_add_nodes(new_node,node)
                        else:
                            continue   
                                                       
                    elif conline.end_connector != OUTPUT and conline.end_connector != SPLITTER + 1 and conline.end_connector != SPLITTER + 2: # dont go up a path
                        node.add_controls_to_asm() # leaving the current node so add its controls
                        node.add_registers_to_asm()
                        
                        dict = self.add_dicts(self.main_names_dict,self.find_names(node.asm_string)) # count occuraces of names so that unique names can be created with replace_substrings
                        self.asm_string += self.replace_substrings(dict,node.asm_string)
                        self.directive_string += self.replace_substrings(dict,node.directive_string)

                        new_node = asm_node(conline.end_block,self.registers_used)
                        self.asm_nodes.append(new_node)
                        if "Output" not in new_node.block.name:
                            self.recursive_add_nodes(new_node,node)
                        else:
                            self.asm_string += new_node.asm_string
                            break
                        
                #*****************************************************************************
                elif conline.start_block.name != node.block.name: # if conline start isnt this block

                    if 'Splitter' in node.block.name:
                        if(conline.end_connector == SPLITTER + 1): # dont allow the first splitter path to be processed
                            continue

                    if "Mixer" in conline.start_block.name:
                        if conline.start_block.usageState == 0: # if this is the first time using this mixer
                            conline.start_block.usageState = 1  # now set it as used
                            node.add_controls_to_asm() # leaving the current node so add its controls
                            node.add_registers_to_asm()
                            self.asm_string += node.asm_string
                            save_reg = self.get_free_register() # get the next free register
                            self.registers_used["r"+str(save_reg)] = conline.start_block.name # set the free register as now used by this block
                            new_node = asm_node(conline.start_block,self.registers_used,conline.start_block.usageState,conline.start_connector,save_reg)
                            self.asm_nodes.append(new_node)
                            self.asm_string += new_node.asm_string
                            break

                        elif conline.start_block.usageState == 1: # this mixer has previously been used in another path
                            conline.start_block.usageState = 2 # second path using this mixer
                            node.add_controls_to_asm() # leaving the current node so add its controls
                            node.add_registers_to_asm()
                            self.asm_string += node.asm_string
                            for reg in range(1, 15): #loop through registers r0-r15
                                if self.registers_used["r"+str(reg)] == conline.start_block.name: # if register is used by block
                                    new_node = asm_node(conline.start_block,self.registers_used,conline.start_block.usageState,reg,conline.start_connector) #use the register in the weighted sum with the current acc32, get another free register for storing temp values
                                    self.registers_used["r"+str(reg)] = 0 # free register
                                    self.asm_nodes.append(new_node)
                                    self.recursive_add_nodes(new_node,node)

                    elif 'Splitter' in conline.start_block.name:
                        if conline.start_block.usageState == 0: # first time using this splitter
                            conline.start_block.usageState = 1  # now set it as used
                            node.add_controls_to_asm() # leaving the current node so add its controls
                            node.add_registers_to_asm()
                            self.asm_string += node.asm_string
                            save_reg = self.get_free_register() # get the next free register
                            self.registers_used["r"+str(save_reg)] = conline.start_block.name # set the free register as now used by this block
                            new_node = asm_node(conline.start_block,self.registers_used,conline.start_block.usageState,save_reg,conline.start_connector)
                            self.asm_nodes.append(new_node)
                            self.recursive_add_nodes(new_node,node)
                        else:
                            continue

                    elif conline.start_connector != OUTPUT and conline.start_connector != SPLITTER + 1 and conline.start_connector != SPLITTER + 2: # dont go up a path
                        node.add_controls_to_asm() # leaving the current node so add its controls
                        node.add_registers_to_asm()

                        dict = self.add_dicts(self.main_names_dict,self.find_names(node.asm_string)) # count occuraces of names so that unique names can be created with replace_substrings
                        self.asm_string += self.replace_substrings(dict,node.asm_string)
                        self.directive_string += self.replace_substrings(dict,node.directive_string)

                        new_node = asm_node(conline.start_block,self.registers_used)   
                        self.asm_nodes.append(new_node) 
                        if "Output" not in new_node.block.name:
                            self.recursive_add_nodes(new_node,node)
                        else:
                            self.asm_string += new_node.asm_string
                            break
                        
        #========================================================= current block is not an input block                    
        else:
            node.block.conLines.sort(key=lambda x: x.end_connector)# sort list by conline end connector so that control blocks come first
            node.block.conLines.sort(key=lambda x: x.start_connector)# sort list again by conline start connector

            for conline in node.block.conLines: # loop through block connector lines

                #*****************************************************************************
                if conline.start_block.name == node.block.name:#if a new line starts on the current iteration block
                    if conline.end_block.name != prev_node.block.name:#dont add the previous block   

                        if 'Splitter' in node.block.name:
                            if(conline.start_connector == SPLITTER + 2):#dont allow the second splitter path to be processed
                                continue

                        if conline.end_connector == 1: #control connector   
                            node.add_control(conline.start_connector,1,conline.end_block.ID)     

                        elif "Mixer" in conline.end_block.name: # mixer block
                            if conline.end_block.usageState == 0: # if this is the first time using this mixer
                                conline.end_block.usageState = 1  # now set it as used
                                node.add_controls_to_asm() # leaving the current node so add its controls
                                node.add_registers_to_asm()
                                self.asm_string += node.asm_string
                                save_reg = self.get_free_register() # get the next free register
                                self.registers_used["r"+str(save_reg)] = conline.end_block.name # set the free register as now used by this block
                                new_node = asm_node(conline.end_block,self.registers_used,conline.end_block.usageState,save_reg,conline.end_connector) 
                                self.asm_nodes.append(new_node)
                                self.asm_string += new_node.asm_string
                                break

                            elif conline.end_block.usageState == 1: # this mixer has previously been used in another path
                                conline.end_block.usageState = 2 # second path using this mixer
                                node.add_controls_to_asm() # leaving the current node so add its controls
                                node.add_registers_to_asm()
                                self.asm_string += node.asm_string
                                for reg in range(1, 15): # loop through registers r1-r15
                                    if self.registers_used["r"+str(reg)] == conline.end_block.name: # if register is used by block
                                        new_node = asm_node(conline.end_block,self.registers_used,conline.end_block.usageState,reg,conline.end_connector) #use the register in the weighted sum with the current acc32, get another free register for storing temp values
                                        self.registers_used["r"+str(reg)] = 0 # free register
                                        self.asm_nodes.append(new_node)    
                                        self.recursive_add_nodes(new_node,node)

                        elif "Splitter" in conline.end_block.name: # splitter block
                            if conline.end_block.usageState == 0: # if this is the first time using this splitter
                                conline.end_block.usageState = 1  # now set it as used
                                node.add_controls_to_asm() # leaving the current node so add its controls
                                node.add_registers_to_asm()
                                self.asm_string += node.asm_string
                                save_reg = self.get_free_register() # get the next free register
                                self.registers_used["r"+str(save_reg)] = conline.end_block.name # set the free register as now used by this block
                                new_node = asm_node(conline.end_block,self.registers_used,conline.end_block.usageState,save_reg,conline.end_connector) 
                                self.asm_nodes.append(new_node)
                                self.recursive_add_nodes(new_node,node)
                            else:
                                continue

                        elif conline.end_connector != OUTPUT and conline.end_connector != SPLITTER + 1 and conline.end_connector != SPLITTER + 2: # dont go up a path
                            node.add_controls_to_asm() # leaving the current node so add its controls
                            node.add_registers_to_asm()

                            dict = self.add_dicts(self.main_names_dict,self.find_names(node.asm_string)) # count occuraces of names so that unique names can be created with replace_substrings
                            self.asm_string += self.replace_substrings(dict,node.asm_string)
                            self.directive_string += self.replace_substrings(dict,node.directive_string)

                            new_node = asm_node(conline.end_block,self.registers_used)
                            self.asm_nodes.append(new_node)
                            if "Output" not in new_node.block.name:
                                self.recursive_add_nodes(new_node,node)
                            else:
                                self.asm_string += new_node.asm_string
                                break

                #*****************************************************************************
                elif conline.end_block.name == node.block.name: #if a new line ends on the current iteration block
                    if conline.start_block.name != prev_node.block.name:#dont add the previous block

                        if 'Splitter' in node.block.name:
                            if(conline.end_connector == SPLITTER + 2):#dont allow the second splitter path to be processed
                                break   
                            
                        if conline.start_connector == 1: # control connector  
                            node.add_control(conline.end_connector,1,conline.start_block.ID)  
                            
                        elif "Mixer" in conline.start_block.name:
                            if conline.start_block.usageState == 0: # if this is the first time using this mixer
                                conline.start_block.usageState = 1  # now set it as used
                                node.add_controls_to_asm()
                                node.add_registers_to_asm()
                                self.asm_string += node.asm_string
                                save_reg = self.get_free_register() # get the next free register
                                self.registers_used["r"+str(save_reg)] = conline.start_block.name # set the free register as now used by this block
                                new_node = asm_node(conline.start_block,self.registers_used,conline.start_block.usageState,save_reg,conline.start_connector)
                                self.asm_nodes.append(new_node)
                                self.asm_string += new_node.asm_string
                                break

                            elif conline.start_block.usageState == 1: # this mixer has previously been used in another path
                                conline.start_block.usageState = 2 # second path using this mixer
                                node.add_controls_to_asm()
                                node.add_registers_to_asm()
                                self.asm_string += node.asm_string
                                for reg in range(1, 15): #loop through registers r0-r15
                                    if self.registers_used["r"+str(reg)] == conline.start_block.name: # if register is used by block
                                        new_node = asm_node(conline.start_block,self.registers_used,conline.start_block.usageState,reg,conline.start_connector) #use the register in the weighted sum with the current acc32, get another free register for storing temp values
                                        self.registers_used["r"+str(reg)] = 0 # free register
                                        self.asm_nodes.append(new_node)
                                        self.recursive_add_nodes(new_node,node)

                        elif "Splitter" in conline.start_block.name:
                            if conline.start_block.usageState == 0: # if this is the first time using this splitter
                                conline.start_block.usageState = 1  # now set it as used
                                node.add_controls_to_asm()
                                node.add_registers_to_asm()
                                self.asm_string += node.asm_string
                                save_reg = self.get_free_register() # get the next free register
                                self.registers_used["r"+str(save_reg)] = conline.start_block.name # set the free register as now used by this block
                                new_node = asm_node(conline.start_block,self.registers_used,conline.start_block.usageState,save_reg,conline.start_connector)
                                self.asm_nodes.append(new_node)
                                self.recursive_add_nodes(new_node,node)
                            else:
                                continue

                        elif conline.start_connector != OUTPUT and conline.start_connector != SPLITTER + 1 and conline.start_connector != SPLITTER + 2: #dont go up a path 
                            node.add_controls_to_asm() # leaving the current node so add its controls
                            node.add_registers_to_asm()        
                            
                            dict = self.add_dicts(self.main_names_dict,self.find_names(node.asm_string)) # count occuraces of names so that unique names can be created with replace_substrings
                            self.asm_string += self.replace_substrings(dict,node.asm_string)
                            self.directive_string += self.replace_substrings(dict,node.directive_string)
    
                            new_node = asm_node(conline.start_block,self.registers_used)   
                            self.asm_nodes.append(new_node)
                            if "Output" not in new_node.block.name:
                                self.recursive_add_nodes(new_node,node)
                            else:
                                self.asm_string += new_node.asm_string
                                break

    #-------------------------------------------generate_asm
    def generate_asm(self):
        self.asm_nodes = []
        self.asm_string = ""
        self.directive_string = ""
        self.main_names_dict = {}

        self.registers_used["r1"] = 0
        self.registers_used["r2"] = 0
        self.registers_used["r3"] = 0
        self.registers_used["r4"] = 0
        self.registers_used["r5"] = 0
        self.registers_used["r6"] = 0
        self.registers_used["r7"] = 0
        self.registers_used["r8"] = 0
        self.registers_used["r9"] = 0
        self.registers_used["r10"] = 0
        self.registers_used["r11"] = 0
        self.registers_used["r12"] = 0
        self.registers_used["r13"] = 0
        self.registers_used["r14"] = 0
        self.registers_used["r15"] = 0

        for block in blocks:#loop through blocks until a start block is found
            if block.conLines != []:
                if 'Input' in block.name or 'Splitter' in block.name: # start building the graph from the input   !!TODO!! signal generators can start a graph too
                    if 'Splitter' in block.name: #if a splitter it has to be used already to start a graph
                        if block.usageState == 0:
                            continue
                        elif block.usageState == 1:
                            block.usageState = 2
                            for reg in range(1, 15): #loop through registers r1-r15
                                if self.registers_used["r"+str(reg)] == block.name: # find register used by splitter previously
                                    input_node = asm_node(block,self.registers_used,block.usageState,reg)
                                    self.registers_used["r"+str(reg)] = 0
                                    self.asm_nodes.append(input_node) # add input node to list
                                    self.recursive_add_nodes(input_node) # start recursion  
                    else:
                        input_node = asm_node(block)    
                        self.asm_nodes.append(input_node) # add input node to list
                        self.recursive_add_nodes(input_node) # start recursion  

        for block in blocks:
            block.usageState = 0

        for node in self.asm_nodes:
            print(node.name)

        final_string = self.directive_string + self.asm_string 
        print(final_string)
        
        f = open("generated.fxc", 'w')
        f.write(final_string)
        f.close()    
        # os.system('FXCoreCmdAsm.exe -h ')
        
if __name__ == '__main__':
    FXCoreDesignerApp().run()