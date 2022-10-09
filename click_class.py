from kivy.uix.widget import Widget
from block_class import Block
from config import blocks

TRUE = 1
FALSE = 0

DRAGGING = 1
NOT_DRAGGING = 0

SELECTED = 1 
RELEASED = 0

DONT_ASSIGN_LINE = 0
ASSIGN_LINE = 1

MOVING = 1
STILL = 0

DRAG_MODE0 = 0
DRAG_MODE1 = 1

class Click(Widget):
    #-------------------------------------------
    def assign_block(self,name,inputNode,outputNode,nParams):
        with self.canvas:
            nameCounter = 0
            create_block = 0
            temp = name + " " + str(nameCounter)

            if blocks == []:
                block = Block(temp,nameCounter,inputNode,outputNode,nParams)   
                blocks.append(block)
            else:
                while create_block == 0:
                    for block in blocks:
                        temp = name + " " + str(nameCounter)
                        if temp[:-1] == block.label.text[:-1]: #if block names match
                            for block in blocks: #now check for block names and number matches
                                temp = name + " " + str(nameCounter)
                                if temp == block.name:
                                    nameCounter = nameCounter + 1
                                    if name == 'Input' or name == 'Output' or name == 'Switch':
                                        if nameCounter > 4:
                                            return
                                    if name == 'Pot':
                                        if nameCounter > 6:
                                            return       
                                    if name == 'Tap Tempo':
                                        if nameCounter > 1:
                                            return   
                            create_block = 1
                        else:
                            create_block = 1
                temp = name + " " + str(nameCounter)
                block = Block(temp,nameCounter,inputNode,outputNode,nParams)
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
                block.move_block(touch)
                # if block.conLines != []: 
                #     for conLine in block.conLines:
                #         if conLine.dragging == DRAGGING:
                #             conLine.drag_line(touch,DRAG_MODE0)

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
                                if newConnector != 0:                                             # ...yes!
                                    if newConnector is not None:   #here only allow line to stop dragging if inside a valid connector, which depends on the start connector
                                        if((conLine.start_connector == 10 or conLine.start_connector == 31 or conLine.start_connector == 32) and (newConnector == 11 or newConnector == 21 or newConnector == 22)) or \
                                            ((conLine.start_connector == 11 or conLine.start_connector == 21 or conLine.start_connector == 22) and (newConnector == 10 or newConnector == 31 or newConnector == 32)) or \
                                            (conLine.start_connector <=6 and newConnector == 1 and (block2.inputExists == 0)) or\
                                            (conLine.start_connector == 1 and (block1.inputExists == 0) and newConnector <=6):
                                                if block2.conLines != []: # block2 has lines?
                                                    for conLine2 in block2.conLines:
                                                        if conLine2.start_block.name == block2.name: #only check the connections that start on block 2
                                                            if conLine2.start_connector == newConnector:
                                                                return #found line that is connected here so break out so cursor keeps hold of line
                                                        elif conLine2.end_block.name == block2.name:#...or end on block 2 
                                                            if conLine2.end_connector == newConnector:
                                                                return #found line that is connected here so break out so that cursor keeps hold of line              
                                                    conLine.dragging = NOT_DRAGGING
                                                    conLine.end_block=block2
                                                    conLine.end_connector = newConnector
                                                    conLine.name += (" " + block2.name + " " + str(conLine.end_connector))
                                                    block2.conLines.append(conLine)# add the newly connected line to the list of lines    
                                                else: #block 2 has no lines            
                                                    conLine.dragging = NOT_DRAGGING
                                                    conLine.end_block=block2
                                                    conLine.end_connector = newConnector
                                                    conLine.name += (" " + block2.name + " " + str(conLine.end_connector))
                                                    block2.conLines.append(conLine)# add the newly connected line to the list of lines
                                                    break       