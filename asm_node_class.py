from config import *


class control_node():
    def __init__(self,param_num, control_type,val):
        self.param_num = param_num
        self.control_type = control_type
        self.val = val


class asm_node():
    def remove_user_block(self):
        lines = self.asm_string.split('\n')
        start_index = None
        end_index = None
        for i, line in enumerate(lines):
            if "@USER START@" in line:
                start_index = i
            elif "@USER END@" in line:
                end_index = i
                del lines[start_index:end_index+1]
        return '\n'.join(lines)

    # def remove_asm_line(self, text, substr):
    #     lines = text.split('\n')
    #     for i, line in enumerate(lines):
    #         if substr in line:
    #             del lines[i]
    #             break
    #     return '\n'.join(lines)

    def unique_substrings(self, long_string, substring):
        substrings = long_string.split(' ')
        unique_substrings = set()
        for string in substrings:
            if substring in string:
                unique_substrings.add(string)
        return list(unique_substrings)

    def add_constant(self, control):
        # Split the long string into individual lines
        lines = self.asm_string.split("\n")
        # Loop over the lines and look for lines that contain the substring and value
        for i in range(len(lines)):
            if "PARAM" + str(control.param_num) in lines[i]:
                if  "@pot to acc32@" in lines[i]:
                    lines[i] = "wrdld     acc32, " + str(control.val) + "*32767 ;load constant into parameter register"
                else:
                    new_line = "wrdld     REPLACE_ME , " + str(control.val) + "*32767    ;load value 0.5 into parameter register"
                    start_index = lines[i].find('$REG')
                    end_index = lines[i].find('$', start_index + 1)
                    if start_index >= 0 and end_index > start_index:
                        substring = lines[i][start_index:end_index + 1]
                        lines[i] = new_line.replace("REPLACE_ME",substring)

        # Join the lines back together into a single string
        self.asm_string = "\n".join(lines)

    def swap_pots_with_constants(self):
        new_lines = []
        for line in self.asm_string.split("\n"):
            if  "@pot to acc32@" in line:  
                if "$PARAM" in line:
                    new_lines.append("wrdld     acc32 , 0.5*32767    ;load value 0.5 into parameter register")
                else:
                    new_lines.append(line)
            elif "$PARAM" in line:
                    new_line = "wrdld     REPLACE_ME , 0.5*32767    ;load value 0.5 into parameter register"
                    start_index = line.find('$REG')
                    end_index = line.find('$', start_index + 1)
                    if start_index >= 0 and end_index > start_index:
                        substring = line[start_index:end_index + 1]

                        new_line = new_line.replace("REPLACE_ME",substring)
                        new_lines.append(new_line)

            else:
                new_lines.append(line)
        self.asm_string = "\n".join(new_lines)

    def add_control(self,param_num, control_type,val = 0):
        new_control = control_node(param_num, control_type,val)
        self.controls.append(new_control)

    def swap_control_strings(self,search_string,start_string,param_num,new_string):
        pattern = "$" + search_string + str(param_num)  + "$"
        self.asm_string =  start_string.replace(pattern,new_string)

    def add_controls_to_asm(self):
        if self.controls != []:
            for control in self.controls:
                # print("control.val",control.val)
                # print("control.control_type", control.control_type)
                # print("control.param_num", control.param_num)

                if control.control_type == POT: #if using a potentiometer or expression input
                    if control.val == 0: # val is the potentiometer number, param_num is the number given to the parameter in the asm
                        self.swap_control_strings("PARAM", self.asm_string, control.param_num,"pot0_smth")
                    elif control.val == 1:
                        self.swap_control_strings("PARAM", self.asm_string, control.param_num,"pot1_smth")
                    elif control.val == 2:
                        self.swap_control_strings("PARAM", self.asm_string, control.param_num,"pot2_smth")
                    elif control.val == 3:
                        self.swap_control_strings("PARAM", self.asm_string, control.param_num,"pot3_smth")
                    elif control.val == 4:
                        self.swap_control_strings("PARAM", self.asm_string, control.param_num,"pot4_smth")
                    elif control.val == 5:  
                        self.swap_control_strings("PARAM", self.asm_string, control.param_num,"pot5_smth")

                elif control.control_type == CONSTANT: # if using a constant, val is the constant's value
                    self.add_constant(control)

                # elif control.control_type == TAP_OUT:
                #     self.swap_control_strings("TAP", self.asm_string, control.param_num,"tap_asm_string")
                
                # elif control.control_type == SWITCH_OUT:
                #     self.swap_control_strings("SWITCH", self.asm_string, control.param_num,"tap_asm_string")

                elif control.control_type == USER_BLOCK_IN:
                    if control.val == 0: # USER OUT 0  
                        self.swap_control_strings("USER", self.asm_string, control.param_num-USER_OUT_BASE,"user0")
                    elif control.val == 1: # USER OUT 1
                        self.swap_control_strings("USER", self.asm_string, control.param_num-USER_OUT_BASE,"user1") 
                    pass

        self.swap_pots_with_constants()
        self.asm_string = self.remove_user_block()

        # TODO remove unused tap tempo code function
        # TODO remove unused switch code function

    def add_registers_to_asm(self):
        substrings = self.unique_substrings(self.asm_string,"$REG")
        for substring in substrings:
            free_reg = self.get_free_register()
            free_reg = "r"+str(free_reg)
            self.registers_used[free_reg] = 1
            self.asm_string = self.asm_string.replace(substring,free_reg)

        if self.registers_used != {}:
            for key in self.registers_used:
                if self.registers_used[key] == 1:
                    self.registers_used[key] = 0

    def get_connector_name(self, connector):
        if connector == PARAM1:
            return self.param1
        if connector == PARAM2:
            return self.param2
        if connector == PARAM3:
            return self.param3      
        if connector == PARAM4:
            return self.param4
        if connector == PARAM5:
            return self.param5
        if connector == PARAM6:
            return self.param6
        if connector == USER0OUT:
            return self.user0
        if connector == USER1OUT:
            return self.user1
        if connector == TAP_IN:
            return self.tapTempo
        if connector == SW0_IN:
            return self.switch0
        if connector == SW1_IN:
            return self.switch1
        if connector == SW2_IN:
            return self.switch2
        if connector == SW3_IN:
            return self.switch3
        if connector == SW4_IN:
            return self.switch4
        else:
            return ""
    
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
        # elif self.registers_used["r15"] == 0:
        #     return 15
        return None
  
    def __init__(self,block,free_registers = {}, usage_state = 0, free_register = None, connector = 0,):
        
        self.name = block.name
        self.block = block
        self.controls = []
        self.usage_state = usage_state
        self.registers_used = free_registers

        if "Input" in self.name:
            self.directive_string = ""
            if "0" in self.name:
                self.asm_string = "\ncpy_cs    r0 , in0    ;Input 0\n"
            if "1" in self.name:
                self.asm_string = "\ncpy_cs    r0 , in1    ;Input 1\n"     
            if "2" in self.name:
                self.asm_string = "\ncpy_cs    r0 , in2    ;Input 2\n"
            if "3" in self.name:
                self.asm_string = "\ncpy_cs    r0 , in3    ;Input 3\n"

        elif "Output" in self.name:
            self.directive_string = ""
            if "0" in self.name:
                self.asm_string = "\ncpy_sc    out0 , r0    ;Output 0\n"
            if "1" in self.name:
                self.asm_string = "\ncpy_sc    out1 , r0    ;Output 1\n"
            if "2" in self.name:
                self.asm_string = "\ncpy_sc    out2 , r0    ;Output 2\n"
            if "3" in self.name:
                self.asm_string = "\ncpy_sc    out3 , r0    ;Output 3\n" 

        elif "User" in self.name:
            self.directive_string = ""
            # if "0" in self.name:
            #     self.asm_string = "\ncpy_sc    user0 , r0    ;User 0\n"
            # if "1" in self.name:
            #     self.asm_string = "\ncpy_sc    user1 , r0    ;User 1\n"

        elif "Pot" in self.name:
            pass

        elif "Switch" in self.name:
            pass
            
        elif "Constant" in self.name:
            pass
              
        elif "Tap Tempo" in self.name:
            pass
  
        elif "Mixer" in self.name:
            self.param1 = 'Input Level 1'
            self.param2 = 'Input Level 2'    
            self.asm_string = ""
            self.directive_string = ""
            if self.usage_state == 1:
                if free_register is not None:
                    self.asm_string =  "\ncpy_cc    " +"r"+str(free_register) +" , r0     ;mixer state 1\n" # save the input from r0 in the free register 
            elif self.usage_state == 2:
                free_register2 = self.get_free_register()
                self.free_register2 = free_register2
                self.asm_string +=     "\ncpy_cc    r" + str(free_register2) + " , r0     ;mixer state 2\n " # copy from previous block r0 output to free_register

            # cpy_cs    acc32 , $PARAM3$           ; dry level @pot to acc32@
            # multrr    acc32 , $REG_input$        ; multiply it

                if connector == MIXER + 1: # previous block using mixer input 1
                    self.asm_string +=  "cpy_cs    acc32 , $PARAM1$ ; in 1 level    ; @pot to acc32@ \n"  # multiply with input 1 level val and save in acc32
                    self.asm_string +=  "multrr    acc32 , r" + str(free_register2) + " \n"     # copy acc32 back to the spare register
                    self.asm_string +=  "cpy_cc    r" + str(free_register2) + " , acc32 \n" 

                    self.asm_string +=  "cpy_cs    acc32 , $PARAM2$ ; in 2 level    ; @pot to acc32@ \n"  # multiply with input 2 level val and save in acc32
                    self.asm_string +=  "multrr    acc32 , r" + str(free_register) + " \n"     # copy acc32 back to the spare register
                    self.asm_string +=  "cpy_cc    r" + str(free_register) + " , acc32 \n" 

                elif connector == MIXER + 2: # previous block using mixer input 2   
                    
                    self.asm_string +=  "cpy_cs    acc32 , $PARAM1$ ; in 1 level    ; @pot to acc32@ \n"  # multiply with input 1 level val and save in acc32
                    self.asm_string +=  "multrr    acc32 , r" + str(free_register) + " \n"     # copy acc32 back to the spare register
                    self.asm_string +=  "cpy_cc    r" + str(free_register) + " , acc32 \n" 

                    self.asm_string +=  "cpy_cs    acc32 , $PARAM2$ ; in 2 level    ; @pot to acc32@ \n"  # multiply with input 2 level val and save in acc32
                    self.asm_string +=  "multrr    acc32 , r" + str(free_register2) + " \n"     # copy acc32 back to the spare register
                    self.asm_string +=  "cpy_cc    r" + str(free_register2) + " , acc32 \n" 

                self.asm_string +=      "adds      r" + str(free_register)  + " , r" + str(free_register2) + "    ;perfom addition and save in acc32\n" #perform the weighted sum and save in acc32
                self.asm_string +=      "cpy_cc    r0 , acc32 \n"

        elif "Splitter" in self.name:
            self.asm_string = ""
            self.directive_string = ""
            if self.usage_state == 1:
                self.asm_string +=  "\ncpy_cc    r" + str(free_register)  + " , r0     ;splitter state 1\n" #copy acc32 from input to the free register
            if self.usage_state == 2:
                self.asm_string +=  "\ncpy_cc    r0 , r" + str(free_register)  + "     ;splitter state 2\n"#copy the spare register to acc32 for output

        elif "Envelope" in self.name:
            self.param1 = "Sensitivity"
            self.directive_string = ".equ env_coeff  0.0006 * (2^31 - 1)"
            self.asm_string = """; ##### Envelope follower #####
; adjust pot for sensitivity
cpy_cs    acc32 , $PARAM1$  @pot to acc32@
multri    acc32 , 0.8
addsi     acc32 , 0.2
cpy_cc    $REG_sens$ , acc32

wrdld     $REG_temp$ , env_coeff.u       ; load in lp coefficient
ori       $REG_temp$ , env_coeff.l
cpy_cc    $REG_temp$ , acc32             ; coeff in temp now
multrr    r0 , r0                  ; square the signal
subs      acc32 , $REG_envlp$            ; in - lp
multrr    acc32 , $REG_temp$             ; *K
adds      acc32 , $REG_envlp$            ; + lp
cpy_cc    $REG_envlp$ , acc32            ; save to lp
; square root
log2      acc32                    ; log2
sra       acc32 , 1                ; /2 to take square root
exp2      acc32                    ; and back to linear
multrr    $REG_sens$ , acc32
sls       acc32 , 2                 ; multiply by 4 to control SVF
cpy_cc    $REG_env$ , acc32              ; save to env
"""
            
        elif "Test" in self.name:
            self.param1 = 'pot0'
            self.param2 = 'pot1'
            self.param3 = 'pot2'
            self.param4 = 'pot3'
            self.param5 = 'pot4'
            self.param6 = 'pot5'
            self.tapTempo = 'tap input'
            self.user0 = 'led0'
            self.user1 = 'led1'
            self.switch0 = 'switch0'
            self.switch1 = 'switch1'
            self.switch2 = 'switch2'
            self.switch3 = 'switch3'
            self.switch4 = 'switch4'
            self.directive_string = ""
            self.asm_string = ""


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////  PITCH SHIFT  ///////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        elif "Pitch" in self.name:
            self.param1 = 'Pitch'
            self.param2 = 'Pitch Level'
            self.param3 = 'Dry Level'
            self.directive_string = """\n
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PITCH SHIFT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.equ      shiftbase  -1048576      ; shift of +1 octave
.mem      $pdelay$     4096          ; Define the delay block for the pitch delay
"""
            self.asm_string = """\n
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PITCH SHIFT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cpy_cs    $REG_temp$ , $PARAM1$      ; pitch shift amount
addsi     $REG_temp$ , -0.5          ; ranges -0.5 to 0.5 in acc32
wrdld     $REG_temp$ , shiftbase.u ; Put upper part of shiftbase into temp
multrr    acc32 , $REG_temp$         ; Multiply the adjusted param value by shiftbase
jgez      acc32 , $OK$               ; If positive jump over the multiply by 2
sls       acc32 , 1                  ; Do the multiply by shifting left 1 bit
$OK$:
cpy_sc    $ramp$_f , acc32            ; Write the result to the ramp0 frequency control

cpy_cc    $REG_input$ , r0           ; Read input
wrdel     $pdelay$ , $REG_input$     ; Write it to the delay

pitch     $rmp$|l4096 , $pdelay$      ; Do the shift, result will be in acc32 
cpy_cs    $REG_temp$ , $PARAM2$      ; pitch shift level
multrr    $REG_temp$ , acc32         ; multiply it
cpy_cc    $REG_temp$ , acc32         ; and save to temp

cpy_cs    acc32 , $PARAM3$           ; dry level @pot to acc32@
multrr    acc32 , $REG_input$        ; multiply it
adds      acc32 , $REG_temp$         ; add result of first shifter

cpy_cc    r0, acc32
"""

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////  DISTORTION  ///////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# pot0 = Input gain
# pot1 = Low-pass frequency control
# pot2 = Low-pass Q control
# pot3 = Output level
        elif "Distortion" in self.name:
            self.param1 = 'Gain'
            self.param2 = 'Low Pass Freq'
            self.param3 = 'Low Pass Q'
            self.param4 = 'Output Level'
            self.directive_string = ""
            self.asm_string = """\n
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DISTORTION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; gain
cpy_cc    $REG_temp$ , r0
cpy_cs    $REG_temp2$ , $PARAM1$ 
multrr    $REG_temp$ , $REG_temp2$ 
sls       acc32 , 4
adds      $REG_temp$ , acc32
cpy_cc    $REG_in$ , acc32

; adjust pot for f control
; kf needs to range from 0.086 to about 0.95 
cpy_cs    $REG_temp$ , $PARAM2$ 
multri    $REG_temp$ , 0.864       ; Coefficient is high end - low end
addsi     acc32 , 0.086            ; add in the low end
cpy_cc    $REG_kf$ , acc32

; adjust pot for Q control
; range from about 0.8 to 0.05 for damping
cpy_cs    acc32 , $PARAM3$         ; Read in pot @pot to acc32@
addsi     acc32 , -1.0             ; acc32 ranges -1 to 0
multri    acc32 , 0.75             ; acc32 ranges -0.75 to 0
neg       acc32                   ; acc32 ranges 0.75 to 0
addsi     acc32 , 0.05             ; acc32 ranges 0.8 to 0.05
cpy_cc    $REG_kq$ , acc32

; distortion
; 0.5*IN + 0.8*(IN-sgn(IN)*IN^2)
multrr    $REG_in$ , $REG_in$      ; IN^2
jgez      $REG_in$ , $jp$          ; if IN is positive jump
neg       acc32                   ; IN < 0 so negate it
$jp$:
subs      $REG_in$ , acc32         ; IN-sgn(IN)*IN^2
multri    acc32 , 0.8              ; 0.8*(IN-sgn(IN)*IN^2)
cpy_cc    $REG_temp$ , acc32       ; save to temp
sra       $REG_in$ , 1             ; 0.5*IN
adds      $REG_temp$ , acc32       ; 0.5*IN + 0.8*(IN-sgn(IN)*IN^2)

; now the SVF 
; first a LP FIR with a null at Fs/2 to help make the filter stable
; and allow a wider range of coefficients
; input in acc32
sra       acc32 , 1                ; in/2
cpy_cc    $REG_temp$ , acc32       ; save to temp
adds      acc32 , $REG_inlp$       ; in/2 + input LP
cpy_cc    $REG_in$ , acc32         ; save to in
cpy_cc    $REG_inlp$ , $REG_temp$  ; save in/2 to input LP
; now the svf
multrr    $REG_kf$ , $REG_bp$      ; Kf * BP
adds      $REG_lp$ , acc32         ; + LP
cpy_cc    $REG_lp$ , acc32         ; save to LP
multrr    $REG_kq$ , $REG_bp$      ; Kq * BP
adds      $REG_lp$ , acc32         ; LP + Kq * BP
subs      $REG_in$ , acc32         ; IN - (LP + Kq * BP)
cpy_cc    $REG_hp$ , acc32         ; save to HP
multrr    $REG_kf$ , $REG_hp$      ; Kf * HP
adds      $REG_bp$ , acc32         ; + BP
cpy_cc    $REG_bp$ , acc32         ; Save to BP

cpy_cs    $REG_temp$ , $PARAM4$    ; Adjust output level
multrr    $REG_temp$ , $REG_temp$ 
multrr    acc32 , $REG_lp$ 

cpy_cc    r0 , acc32               ; Send to output
""" 

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////// CHORUS  ///////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        elif "Chorus" in self.name:
            self.param1 = 'Rate'
            self.param2 = 'Depth'
            self.param3 = 'Level'
            self.tapTempo = 'tap input'
            self.user0 = 'led0'

            self.directive_string = """
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CHORUS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.equ    fs          48000 ; 
.equ    flow       .2 ; 
.equ    fhigh       10 ; 
.equ    pi        3.14159 
.equ    clow      (2^31 - 1) * (2*pi*flow)/fs
.equ    chigh     (2^31 - 1) * (2*pi*fhigh)/fs 
.equ    cdiff     chigh - clow
.mem    $delay$       1024
 """
            self.asm_string = """
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CHORUS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cpy_cs  $REG_temp$ , $PARAM1$       ; read in frequency control pot
wrdld   acc32 , cdiff.u           ; load difference between low and high frequency
ori     acc32 , cdiff.l
multrr  $REG_temp$ , acc32          ; pot0 * cdiff
cpy_cc  $REG_temp$ , acc32
wrdld   acc32 , clow.u            ; load low freq coeff
ori     acc32 , clow.l
adds    acc32 , $REG_temp$          ; add low freq
cpy_sc  $lfo$_f , acc32             ; write to lfo0 frequency control

cpy_cs  $REG_temp$ , $PARAM2$       ; read in depth control pot
wrdld   acc32 , 400
multrr  $REG_temp$ , acc32
cpy_cc  r15 , acc32

cpy_cs  $REG_temp$ , r0
wrdel   $delay$ , $REG_temp$ 

; voice 1
chr     $lfo$|sin $delay$+1400
cpy_cc  $REG_voice1$ , acc32

; voice 2
chr     $lfo$|cos $delay$+256
cpy_cc  $REG_voice2$ , acc32

; voice 3
chr     $lfo$|sin|neg $delay$+16
cpy_cc  $REG_voice3$ , acc32

; voice 4
chr     $lfo$|cos|neg $delay$+768

; sum the voices
adds    acc32 , $REG_voice3$ 
adds    acc32 , $REG_voice2$ 
adds    acc32 , $REG_voice1$ 

; get effects level pot and scale effect
cpy_cs  $REG_temp$ , $PARAM3$  
multrr  acc32 , $REG_temp$ 

; add in dry
cpy_cc  $REG_temp$ , r0
adds    acc32 , $REG_temp$ 

; write it to output
cpy_cc  r0 , acc32 

; @USER START@

; The PWM value becomes updated every 256 samples translating to a
; PWM frequency of 125Hz @32k with 8 bit resolution.
; While this is not exactly a high resolution PWM it might still
; good enough for generating basic control voltages in some applications.
; For driving the LEDs in this case it is perfectly enough.
cpy_cs    acc32 , samplecnt        ; Get the sample counter
andi      acc32 , 0xFF             ; Mask b[7:0]
jnz       acc32 , $doPWM$          ;

; Reload new PWM value from LFOx_s into "bright"
cpy_cs    temp , $lfo$_s            ; read in sin wave ranges -1.0 to +1.0 (well, almost)
sra       temp , 1                 ; /2 to +/- 1/2
addsi     acc32 , 0.5              ; ranges 0 to 1
sra       acc32 , 23               ; shift the PWM value in place
cpy_cc    $REG_bright$ , acc32           ; save it

$doPWM$:
; Performing the decrement prior to driving the LED makes sure
; that the LED can go completly off.
addi      $REG_bright$ , -1           ; subtract 1 from on time
cpy_cc    $REG_bright$ , acc32      ; Save updated "bright"
xor       acc32 , acc32            ; Clear acc32 for the LED off case
jneg      $REG_bright$ , $doLED$   ;
ori       acc32 , 1                ; Set acc32[0] for the LED on case

$doLED$:
set       $USER1$|0 , acc32           ; set the user output per the acc32 LSB
; @USER END@


"""


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# #////////////////////////////////////////  Through Zero Flanger  ////////////////////////////////////////////////////
# #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        elif "Thru0 Flanger" in self.name:
            self.param1 = 'Rate Out'
            self.param2 = 'Rate Back'
            self.param3 = 'Feedback'
            self.param4 = 'Level'
            self.param5 = 'Zero Point'
            self.tapTempo = 'Tap Input'

            self.directive_string = """
.equ      $maxdel$        8192  
.equ      $zp$            $maxdel$/32  
.equ      $sweep$         0x0100    
.mem      $delay$         $maxdel$  
.mem      $zp_del$        $zp$
    """
            self.asm_string = """
cpy_cs    $REG_p3$ , $PARAM4$           ; get level pot
cpy_cs    $REG_temp$ , r0               ; get input
wrdel     $zp_del$ , $REG_temp$            ; write input to dry delay line  
adds      $REG_temp$ , $REG_feedback$          ; add feedback to dry    
multrr    acc32 , $REG_p3$               ; adjust level
wrdel     $delay$ , acc32            ; write to flanger delay line


cpy_cs    acc32 , $PARAM5$             ; get zero point pot @raw pot@
wrdld     $REG_temp$ , $zp$                ; get length of zero point delay
multrr    acc32 , $REG_temp$             ; calculate length
multri    acc32 , 0.99             ; limit max value to allow for adding a small amount
wrdld     $REG_temp$ , 0x0004            ; add a small amount to not be 0  
add       $REG_temp$ , acc32    
cpy_cc    $REG_zero_point$ , acc32       ; zero point

xor       acc32 , acc32            ; clear acc32
ori       acc32 , 0x0010           ; load a minimum value into acc32 in case pot is 0
cpy_cc    $REG_temp$ , acc32             ; save it
cpy_cs    acc32 , $PARAM1$        ; read in pot0
multrr    acc32 , acc32
adds      acc32 , $REG_temp$             ; add the minimum value
cpy_cc    $REG_p0$ , acc32               ; save it
cpy_cs    acc32 , $PARAM2$         ; read in pot 1
multrr    acc32 , acc32
adds      acc32 , $REG_temp$             ; add the minimum value
cpy_cc    $REG_p1$ , acc32               ; save it
andi      flags , $TAP_LVL$           ; get the tap button state
jnz       acc32 , $isnzero$          ; if != 0 jump (pin has pull-up so pressed button is a 0)
xor       acc32 , acc32            ; clear acc
ori       acc32 , $sweep$            ; load in a small increment value
multrr    acc32 , $REG_p0$               ; multiply by out speed pot
adds      $REG_counter$ , acc32          ; add the increment to the counter
cpy_cc    $REG_counter$ , acc32          ; save it back but check it
wrdld     $REG_temp$ , $maxdel$            ; load the max delay line length
subs      $REG_temp$ , acc32             ; maxlength - counter value
jgez      acc32 , $ango$             ; if >=0 we are less than or equal to max so jump
cpy_cc    $REG_counter$ , $REG_temp$           ; if here counter > maxlength so load max length
jmp       $ango$                    ; jump over the decrement part

$isnzero$:
jz        $REG_counter$ , $ango$           ; if count is 0 jump to output
xor       acc32 , acc32            ; clear acc
ori       acc32 , $sweep$            ; load in a small increment value
multrr    acc32 , $REG_p1$               ; multiply by in speed pot
subs      $REG_counter$ , acc32          ; subtract the value
jgez      acc32 , $ldres$            ; if >= 0 jump
xor       acc32 , acc32            ; was <0 so load 0
$ldres$:
cpy_cc    $REG_counter$ , acc32          ; save to counter reg

$ango$:
interp    $REG_counter$ , $delay$          ; linear interp the values in the delay line
cpy_cc    $REG_temp$ , acc32             ; save to temp
interp    $REG_zero_point$ , $zp_del$      ; linear interp zero point sample    
subs      acc32 , $REG_temp$             ; subtract the value from the delay line so we can get a null at  
                                         ; the zero point if feedback is zero, more comb effect if no  

cpy_cc    r0 , acc32             ; write to the output  
cpy_cc    $REG_temp$ , acc32             ; copy to temp
cpy_cs    acc32 , $PARAM3$        ; get feedback level  
multri    acc32 , 0.8              ; limit fedback range    
multrr    $REG_temp$ , acc32             ; set feedback
cpy_cc    $REG_feedback$ , acc32         ; and save
    """
            
        elif "Flanger" in self.name:
            self.param1 = 'Rate Out'
            self.param2 = 'Rate Back'
            self.param3 = 'Feedback'
            self.param4 = 'Level'
            self.tapTempo = 'Tap Input'

            self.directive_string = """
.equ      $maxdel$        8192
.equ      $sweep$         0x0100
.mem      $delay$         $maxdel$
    """
            self.asm_string = """
cpy_cs    $REG_p3$ , $PARAM4$
cpy_cs    $REG_temp$ , r0
adds      $REG_temp$ , feedback
multrr    acc32 , $REG_p3$
wrdel     $delay$ , acc32
 
xor       acc32 , acc32            ; clear acc32
ori       acc32 , 0x0010           ; load a minimum value into acc32 in case pot is 0
cpy_cc    $REG_temp$ , acc32             ; save it
cpy_cs    acc32 , $PARAM1$        ; read in pot0
multrr    acc32 , acc32
adds      acc32 , $REG_temp$             ; add the minimum value
cpy_cc    $REG_p0$ , acc32               ; save it
cpy_cs    acc32 , $PARAM2$         ; read in pot 1
multrr    acc32 , acc32
adds      acc32 , $REG_temp$             ; add the minimum value
cpy_cc    $REG_p1$ , acc32               ; save it
andi      flags , $TAP_LVL$           ; get the tap button state
jnz       acc32 , $isnzero$          ; if != 0 jump (pin has pull-up so pressed button is a 0)
xor       acc32 , acc32            ; clear acc
ori       acc32 , $sweep$            ; load in a small increment value
multrr    acc32 , $REG_p0$               ; multiply by out speed pot
adds      $REG_counter$ , acc32          ; add the increment to the counter
cpy_cc    $REG_counter$ , acc32          ; save it back but check it
wrdld     $REG_temp$ , $maxdel$            ; load the max delay line length
subs      $REG_temp$ , acc32             ; maxlength - counter value
jgez      acc32 , $ango$             ; if >=0 we are less than or equal to max so jump
cpy_cc    $REG_counter$ , $REG_temp$           ; if here counter > maxlength so load max length
jmp       $ango$                    ; jump over the decrement part
$isnzero$:
jz        $REG_counter$ , $ango$           ; if count is 0 jump to output
xor       acc32 , acc32            ; clear acc
ori       acc32 , $sweep$            ; load in a small increment value
multrr    acc32 , $REG_p1$               ; multiply by in speed pot
subs      $REG_counter$ , acc32          ; subtract the value
jgez      acc32 , $ldres$            ; if >= 0 jump
xor       acc32 , acc32            ; was <0 so load 0
$ldres$:
cpy_cc    $REG_counter$ , acc32          ; save to counter reg

$ango$:
interp    $REG_counter$ , $delay$          ; linear interp the values in the delay line
;multrr   p3, acc32
cpy_cs    $REG_temp$ , r0               ; read in the input
adds      acc32 , $REG_temp$              ; add the value from the delay line
cpy_cc    r0 , acc32             ; write to the output
cpy_cs    $REG_temp$ , pot2_smth
multrr    $REG_temp$ , acc32
cpy_cc    $REG_feedback$, acc32
     """
            


# #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# #/////////////////////////////////////////////  LOOPER  ///////////////////////////////////////////////////////////////
# #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if "Looper" in self.name:
            self.directive_string = """
; sw0    - 0: play back recording forward
;          1: playback in reverse
; tap    - press to record, release to play
;
; If user holds tap longer than max recording time then program forces to playback state

; status - 0 : Playback
;          1 : Record
;          2 : We are in a forced playback state but not first time
;          3 : Forced playback state, first time

.creg    $REG_status$    0
.creg    $REG_ptr$       0
.creg    $REG_length$    0x100          ; Any value > 0 can be used as a default
"""
            self.asm_string = """\n\n
; first check for a forced playback state where user recorded longer than
; the 32K samples, special state as we need to ignore certain things
andi     $REG_status$ , 0x0002           ; are we in a forced playback state?
jz       acc32 , normal            ; no so either a record or playback
andi     $REG_status$ , 0x0001           ; first time in forced playback?
jz       acc32 , force_more        ; if not then check other force issues
andi     $REG_status$ , 0x0002           ; change status to forced but not first time
cpy_cc   $REG_status$ , acc32
xor      acc32 , acc32             ; clear acc32
cpy_cc   $REG_ptr$ , acc32               ; reset the pointer
jmp      pb                       ; jump to playback
force_more:
andi     flags , $TAP_LVL$            ; get the tap button state
jz       acc32 , pb                ; if == 0 jump as user is still pushing it (pin has pull-up so pressed button is a 0)
xor      acc32 , acc32             ; if here user has released it, clear acc32
cpy_cc   $REG_status$ , acc32            ; set status to playback, do not reset ptr as that should have been done on the first pass
jmp      pb

normal:
andi     flags , $TAP_LVL$            ; get the tap button state
jnz      acc32 , playback          ; if != 0 jump (pin has pull-up so pressed button is a 0)
andi     $REG_status$ , 0x0001           ; tap button pushed (is 0), was the last state record?
jnz      acc32 , record            ; yes, continue recording
xor      acc32 , acc32             ; nope, so starting a new recording
cpy_cc   $REG_ptr$ , acc32               ; reset pointer
cpy_cc   $REG_length$ , acc32            ; and length count
jmp      record                   ; and record

playback:
; Playback
andi     $REG_status$ , 0x0001           ; was the last state record?
jz       acc32 , pb                ; no, continue playback
xor      acc32 , acc32             ; yes it was
cpy_cc   $REG_ptr$ , acc32               ; reset pointer
cpy_cc   $REG_status$ , acc32            ; set status to playback
pb:
rddirx   acc32 , $REG_ptr$               ; read from current pointer position
cpy_cs   $REG_temp$ , r0                ; get the input
adds     acc32 , $REG_temp$              ; add them
cpy_sc   r0 , acc32              ; write to output

; read switch
cpy_cs   acc32 , switch
andi     acc32 , $SW1$
jz       acc32 , forward           ; if switch 0 is 0 then forward playback
jz       $REG_ptr$ , $ptr_zero$            ; playing back backwards, if ptr is zero we need to reset it
subs     $REG_ptr$ , acc32               ; since the lsb was left set in the above andi we can just subtract
cpy_cc   $REG_ptr$ , acc32               ; copy updated pointer
jmp      $over$                     ; and jump past rest
$ptr_zero$:
subs     $REG_length$ , acc32            ; pointer was zero, need to rest to end
cpy_cc   $REG_ptr$ , acc32               ; which was easy as the lsb was set in acc32 already
jmp      $over$                     ; so just subtract it from the length, save it and jump

forward:
xor      acc32 , acc32             ; clear the acc32
ori      acc32 , 0x0001            ; set lsb
add      $REG_ptr$ , acc32               ; add to current ptr
cpy_cc   $REG_ptr$ , acc32               ; save it
subs     $REG_ptr$ , $REG_length$              ; ptr - length
jnz      acc32 , $over$              ; if !=0 then not at end jump over the rest
xor      acc32 , acc32             ; if 0 then load 0 into acc32
cpy_cc   $REG_ptr$ , acc32               ; copy to ptr
jmp      $over$                     ; jump to end

record:
; read input and write to delay
xor      acc32 , acc32             ; set status to record
ori      acc32 , 0x0001
cpy_cc   $REG_status$ , acc32
cpy_cs   $REG_temp$ , r0                ; read input
wrdirx   $REG_ptr$ , $REG_temp$                ; write to delay
cpy_cc   r0 , $REG_temp$               ; send to out

xor      acc32 , acc32             ; clear acc32
ori      acc32 , 0x0001            ; set lsb
add      $REG_ptr$ , acc32               ; add to current ptr
cpy_cc   $REG_ptr$ , acc32               ; save it
cpy_cc   $REG_length$ , acc32            ; and save to length
xori     $REG_length$ , 0x8000           ; XOR length with 0x8000
jnz      acc32 , $over$              ; if not 0 then not at max count
ori      acc32 , 0x0003            ; passed the end, forced playback
cpy_cc   $REG_status$ , acc32

$over$:
@USER start@
cpy_cs    acc32 , samplecnt        ; Get the sample counter
andi      acc32 , 0xFF             ; Mask b[7:0]
jnz       acc32 , $doPWM0$           ;

sr        $REG_ptr$ , 8 
cpy_cc    $REG_bright$ , acc32           ; save it

$doPWM0$:
; Performing the decrement prior to driving the LED makes sure
; that the LED can go completly off.
addi      $REG_bright$ , -1              ; subtract 1 from on count
cpy_cc    $REG_bright$ , acc32           ; Save updated "bright"
xor       acc32 , acc32            ; Clear acc32 for the LED off case
jneg      $REG_bright$ , $doLED0$          ;
ori       acc32 , 1                ; Set acc32[0] for the LED on case

$doLED0$:
set       user0|0 , acc32           ; set the usr0 output per the acc32 LSB

; PWM usr1
cpy_cs    acc32 , samplecnt        ; Get the sample counter
andi      acc32 , 0xFF             ; Mask b[7:0]
jnz       acc32 , $doPWM1$           ;

sr        $REG_length$ , 8
cpy_cc    $REG_bright2$ , acc32          ; save it

$doPWM1$:
; Performing the decrement prior to driving the LED makes sure
; that the LED can go completly off.
addi      $REG_bright2$ , -1             ; subtract 1 from on count
cpy_cc    $REG_bright2$ , acc32          ; Save updated "bright"
xor       acc32 , acc32            ; Clear acc32 for the LED off case
jneg      $REG_bright2$ , $doLED1$         ;
ori       acc32 , 1                ; Set acc32[0] for the LED on case

$doLED1$:
set       $USER1$|0 , acc32           ; set the usr0 output per the acc32 LSB
@USER END@
"""



# #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# #/////////////////////////////////////////////  DELAY  ///////////////////////////////////////////////////////////////
# #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        if "Delay" in self.name:
            self.param1 = 'Delay Time'
            self.param2 = 'Feedback'
            self.param3 = 'LP Filter'
            self.tapTempo = 'Tap Input'
            self.switch0 = " Division Bit 0"
            self.switch1 = " Division Bit 1"
            self.user0 = "Delay Time Blink"
            self.user1 = "Pot or Tap Mode"

            self.directive_string = """
.rn       temp      r0
.rn       temp1     r1
.rn       calc_delay       r2     ; final calculated delay after any divisions for 1/8th, etc
.rn       lp_con    r3            ; low-pass control register
.rn       lp        r4            ; lp filter
.rn       old_pot   r5            ; old pot time
.rn       act_count r6            ; holds active delay count from tap tempo
.rn       potnot_tap       r7     ; 0 means pot, 1 means tap tempo
.rn       blink_time       r8     ; blink time
.rn       user0_state      r9     ; user0 state
.rn       old_delay r10           ; old delay count

.equ      delay_len 32767

; Define the delay line
.mem      delay     delay_len

; pot smoothing
.sreg     pot0_k    12

; preset MAXTEMPO to the delay line length, time out should be
; equal to or shorter than the delay length
.sreg     MAXTEMPO  delay_len

; since TAPTEMPO and TAPSTKRLD are calculated and we expect
; equations to resolve to values between -1.0 and +0.99...
; we inform the assembler we really want to use integer results
; by appending ".i" to the .sreg directive

; preset the starting TAPTEMPO value to half the delay
.sreg.i   TAPTEMPO  delay_len/2

; set the "sticky" time to 1/2 the max delay time
; careful to not make this too short else every button
; press can look sticky
.sreg.i   TAPSTKRLD delay_len/2

; set debounce time, must be shorter than the sticky time
.sreg.i   TAPDBRLD  delay_len/128

; Initialize potnot_tap to 0 to select POT at startup
.creg     potnot_tap     0

; set user0 led state
.creg     user0_state    0x1

; set multiply factors into mregs, don't need to set 0
.mreg     mr1       0.5           ; 1/8 note
.mreg     mr2       0.3333333     ; triplet
.mreg     mr3       0.25          ; 1/16 note
"""

            self.asm_string = """

; set LP pot control range
cpy_cs    $REG_temp$, pot2_smth
multri    $REG_temp$, 0.75
addsi     acc32, 0.25
cpy_cc    lp_con, acc32

; write a 0 to the delay head in case user sets pot to 0
xor       acc32, acc32            ; clear acc32
wrdel     delay, acc32            ; write 0 to head of delay

; are we "sticky"?
andi      flags, TapStky          ; check bit 4 for a sticky event
jz        acc32, next             ; if not sticky jump past rest
andi      flags, TB2nTB1          ; isolate the tap button and check if it is tap 1 or 2
jnz       acc32, next             ; if set then tap 2 sticky event so jump over rest
andi      potnot_tap, 0x0000      ; if here we got a tap 1 sticky so clear potnot_tap to use POT
cpy_cc    potnot_tap, acc32
jmp       no_tap                  ; jump to delay code

next:
; decide POT or tap
; Do we have a new TAP count?
andi      flags, newTT            ; New tap tempo?
jz        acc32, no_tap           ; if no new tap make no change
ori       potnot_tap, 0x0001      ; set the lsb to indicate we now use tt
cpy_cc    potnot_tap, acc32       ; save it
cpy_cs    act_count, taptempo     ; get the tap count into act_count
sl        act_count, 16           ; shift to 31:16
cpy_cc    act_count, acc32
jmp       $do_delay$

; if here no new tap but decide if we need to update count from the POT
; we need a little hystersis on the POT because even with smoothing it can
; time to settle and the LSB to stop moving. While we can not hear this
; the difference in value looks like a change to the LED flashing routine
; so only update value if it changes by more than 0.01
no_tap:
andi      potnot_tap, 0x0001      ; if lsb is 1 then we are in tap mode, no pot update
jnz       acc32, $do_delay$         ; not 0 so using tap count from above
cpy_cs    $REG_temp$, pot0_smth         ; read in the pot value to temp1
wrdld     $REG_temp1$, delay!           ; get length of the delay into temp[31:16]
multrr    $REG_temp$, $REG_temp1$             ; multiply for final length
cpy_cc    act_count, acc32        ; save delay time which has the integer portion in [31:16] and the interpolation coeff in [15:0]


$do_delay$:
; act_count holds the delay time so check if switches set to divide count
cpy_cc    calc_delay, act_count   ; copy full count into calc_delay
cpy_cs    $REG_temp$, switch            ; get switch states
andi      $REG_temp$, $SW1$|$SW2$           ; keep two switch states
jz        acc32, $go_delay$         ; if switches 0 then no divider and jump over rest
cpy_cmx   $REG_temp$, acc32             ; else use the switches as a pointer to mregs to get divisor
multrr    calc_delay, $REG_temp$        ; multiply by it
cpy_cc    calc_delay, acc32       ; and move to temp1

$go_delay$:
interp    calc_delay, delay       ; linearly interpolate the result from the delay line

; Add the dry signal to the delayed signal
cpy_cs    $REG_temp$, r0
adds      $REG_temp$, acc32

; Output it
cpy_cc    r0, acc32

; multiply by feedback
cpy_cs    $REG_temp$, pot1
multrr    acc32, $REG_temp$

; lp filter it
subs      acc32, lp
multrr    acc32, lp_con
adds      acc32, lp
cpy_cc    lp, acc32

; write to delay line
wrdel     delay, acc32

@USER START@
; flash LED at delay rate 50% duty cycle
; old delay time - current delay time to see if it has changed
sr        calc_delay, 16          ; put calculated delay value into acc32[15:0]
cpy_cc    calc_delay, acc32       ; save back
xor       acc32, acc32            ; clear acc32
ori       acc32, 1024             ; load 1024 into acc32[15:0]
cpy_cc    $REG_temp$, acc32             ; save in temp
subs      old_delay, calc_delay   ; subtract current calculated delay from old one
abs       acc32                   ; absolute value
subs      acc32, $REG_temp$             ; difference minus 1024
jneg      acc32, same             ; if negative then difference less than 1024 so jump over saving new value
; new value, set LED and update the time
ori       user0_state, 0x1        ; turn on LED
cpy_cc    user0_state, acc32      ; save current state
cpy_cc    old_delay, calc_delay   ; over write the old delay time
sr        calc_delay, 1           ; /2 for 50% duty cycle
cpy_cc    blink_time, acc32       ; copy to the blink time

same:
xor       acc32, acc32            ; clear acc32
ori       acc32, 1                ; set the LSB
subs      blink_time, acc32       ; subtract it
cpy_cc    blink_time, acc32       ; copy result to blink_time
jnz       acc32,not_zero          ; if not 0 jump over the rest
cpy_cc    old_delay, calc_delay   ; timed out, get the latest count
sr        old_delay, 1            ; load count/2 back in
cpy_cc    blink_time, acc32       ; copy to timer counter
xori      user0_state, 0x1        ; flip user0 state
cpy_cc    user0_state, acc32
not_zero:
set       user0|0, user0_state     ; bit 0 of user0_state is sent to user0 output

set       user1|0, potnot_tap      ; bit 0 of potnot_tap is sent to user1 output
@USER END@   
"""

# #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# #/////////////////////////////////////////////  PHASER  ///////////////////////////////////////////////////////////////
# #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ;
# ; Phase shifter from AN-5
# ; Mono in/out
# ;
# ; S1:S0 select 2,4,6 or 8 stages
# ; POT0 : rate
# ; POT1 : sweep range
# ; POT2 : resonance (feedback)
# ; POT3 : depth (mix)
# ; mr0 - mr7 are the AP delays
# ; mr8 - mr11 hold the result from each 2 stages for later selection

# .rn       temp      r0            ; Temporary register
# .rn       feedback  r1            ; Holds feedback
# .rn       kcoeff    r2            ; K coefficient for all-pass filters
# .rn       input     r3            ; Input from in0
# .rn       count     r4            ; Window for the PWM
# .rn       bright    r5            ; Number of states in count the LED is on, i.e. PWM width

# .equ      lfomax    2058874       ; LFO max about 5Hz at 32K, see an-3 for equations
# .equ      maxfb     0.875         ; Max feedback level
# .equ      rangebase -0.45*32767   ; We want the K for the APs to range from about -0.5 to -0.95
#                                   ; but the "wrld" instruction want an unsigned 16-bit value so we
#                                   ; play a trick with the assembler, we calculate the 16-bit signed
#                                   ; number but use the ".l" extension when we use the value in wrdld
#                                   ; as adding .l forces the assembler to treat the number as an
#                                   ; integer and mask off the lower 16-bits as an unsigned number

# ; First set up the rate pot
# cpy_cs    temp, pot0_smth         ; read POT0 into temp
# multrr    temp, temp              ; square it so more control at lower range, result in acc32
# wrdld     temp, lfomax.u          ; since wrdld uses just a 16-bit value use upper 16 bits, we could
#                                   ; load the full 32-bit number but the max lfo speed is not critical
#                                   ; in this program so losing the lower 16-bits is not an issue
# multrr    acc32, temp             ; multiply pot by max range
# cpy_sc    lfo0_f, acc32           ; write it to LFO0 frequency control

# ; get the sin wave range -0.45 to -0.95 save in kcoeff
# ; NOTE: Phasers want a positive feed forward and negative feed back
# ; so make K negative as apma inverts in the feedback path and apmb does not
# cpy_cs    temp, lfo0_s            ; read in sin wave ranges -1.0 to +1.0 (well, almost)
# sra       temp, 2                 ; divide by 4 via right shift so ranges +/- 0.25
# addsi     acc32, -0.25            ; now ranges 0 to -0.5
# cpy_cs    temp, pot1_smth         ; get the range pot
# multrr    temp, acc32             ; scale, result in acc32
# wrdld     temp, rangebase.l       ; load in the base of -0.45 that we force the assembler to treat as unsigned
# adds      temp, acc32             ; add base so range can go from -0.45 to -0.95
# cpy_cc    kcoeff, acc32           ; save K in kcoeff for the APs

# ; get source and add feedback
# cpy_cs    input, in0              ; read from channel 0, put in input as we will want it later and working from core
#                                   ; registers is faster than mregs
# adds      input, feedback         ; add feedback from feedback

# ; shift 6 bits down to avoid clipping APs, recover at end.
# sra       acc32, 6                ; divide by 64 for headroom

# ; Do the 8 all passes saving the result every 2 APs for later selection
# apma      kcoeff, mr0             ; AP 1
# apmb      kcoeff, mr0

# apma      kcoeff, mr1             ; AP 2
# apmb      kcoeff, mr1

# cpy_mc    mr8, acc32              ; Save result for 2 stages

# apma      kcoeff, mr2             ; AP 3
# apmb      kcoeff, mr2

# apma      kcoeff, mr3             ; AP 4
# apmb      kcoeff, mr3

# cpy_mc    mr9, acc32              ; Save result for 4 stages

# apma      kcoeff, mr4             ; AP 5
# apmb      kcoeff, mr4

# apma      kcoeff, mr5             ; AP 6
# apmb      kcoeff, mr5

# cpy_mc    mr10, acc32             ; Save result for 6 stages

# apma      kcoeff, mr6             ; AP 7
# apmb      kcoeff, mr6

# apma      kcoeff, mr7             ; AP 8
# apmb      kcoeff, mr7

# cpy_mc    mr11, acc32             ; Save result for 8 stages


# ; Look at the switches and select the number of stages accordingly
# cpy_cs    temp, switch            ; read in the switch sfr
# andi      temp, sw0|sw1           ; only keep S0 and S1
# cpy_cc    temp, acc32             ; save them
# andi      acc32, 0                ; clear acc32
# ori       acc32, 0x0008           ; put 8 into acc32
# add       acc32, temp             ; add the switchs to acc32 so ranges 8 to 11 which happens
#                                   ; to be the MRs used to save the AP results
# cpy_cmx   temp, acc32             ; use acc32 as the pointer to the mreg to read

# sls       temp, 6                 ; multiply by 64 to recover from the initial shift, result in acc32

# ; use POT3 for mix level, full CCW is all dry (in0), full CW is full phase shifter output (fpo)
# subs      acc32, input            ; acc32 = fpo - in0
# cpy_cs    temp, pot3_smth         ; POT3 placed in temp
# multrr    temp, acc32             ; acc32 = acc32 * POT3 = POT3*(fpo - in0)
# adds      acc32, input            ; acc32 = acc32 + in0 = POT3*(fpo - in0) + in0

# ; write to output
# cpy_sc    out0, acc32             ; output it!
# cpy_sC    out1, acc32

# ; adjust feedback level
# cpy_cs    r1, pot2_smth           ; Read POT2
# multrr    acc32, r1               ; Multiply the output by the feedback
# wrdld     temp, maxfb*32768       ; We defined maxfb above as a decimal but need it to be unsigned 16-bit for wrdld
# multrr    acc32, temp             ; Multiply by limit
# cpy_cc    feedback, acc32         ; save it in feedback for next time


# ; The PWM value becomes updated every 256 samples translating to a
# ; PWM frequency of 125Hz @32k with 8 bit resolution.
# ; While this is not exactly a high resolution PWM it might still
# ; good enough for generating basic control voltages in some applications.
# ; For driving the LEDs in this case it is perfectly enough.
# cpy_cs    acc32, samplecnt        ; Get the sample counter
# andi      acc32, 0xFF             ; Mask b[7:0]
# jnz       acc32, doPWM            ;

# ; Reload new PWM value from LFO0_s into "bright"
# cpy_cs    temp, lfo0_s            ; read in sin wave ranges -1.0 to +1.0 (well, almost)
# sra       temp, 1                 ; /2 to +/- 1/2
# addsi     acc32, 0.5              ; ranges 0 to 1
# sra       acc32, 23               ; shift the PWM value in place
# cpy_cc    bright, acc32           ; save it

# doPWM:
# ; Performing the decrement prior to driving the LED makes sure
# ; that the LED can go completly off.
# addi      bright, -1              ; subtract 1 from on count
# cpy_cc    bright, acc32           ; Save updated "bright"
# xor       acc32, acc32            ; Clear acc32 for the LED off case
# jneg      bright, doLED           ;
# ori       acc32, 1                ; Set acc32[0] for the LED on case

# doLED:
# set       user0|0, acc32          ; set the usr1 output per the acc32 LSB
