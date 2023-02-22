MIXER = 20
SPLITTER = 30

class control_node():
    def __init__(self,param_num, control_type,val):
        self.param_num = param_num
        self.control_type = control_type
        self.val = val

class asm_node():
    def swap_param_strings(self,searchString,startString,paramNum,newString):
        pattern = "$" + searchString + str(paramNum)  + "$"
        self.asm_string =  startString.replace(pattern,newString)

    def unique_substrings(self, long_string, substring):
        substrings = long_string.split(' ')
        unique_substrings = set()
        for string in substrings:
            if substring in string:
                unique_substrings.add(string)
        return list(unique_substrings)

    def add_control(self,param_num, control_type,val):
        temp_control = control_node(param_num, control_type,val)
        self.controls.append(temp_control)

    def swap_pots_with_constants(self):
        new_lines = []
        for line in self.asm_string.split("\n"):
            if "$PARAM" in line:
                new_lines.append("wrdld     $REG_temp$, 0.5*32767    ;load value 0.5 into parameter register")
            else:
                new_lines.append(line)
        self.asm_string = "\n".join(new_lines)

    def add_controls_to_asm(self):
        if self.controls != []:
            for control in self.controls:
                if control.control_type == 1: #if using a potentiometer or expression input
                    if control.val == 0:#val is the potentiometer number, param_num is the number given to the parameter in the asm
                        self.swap_param_strings("PARAM", self.asm_string, control.param_num,"ptrg_pot0_smth")
                    elif control.val == 1:
                        self.swap_param_strings("PARAM", self.asm_string, control.param_num,"ptrg_pot1_smth")
                    elif control.val == 2:
                        self.swap_param_strings("PARAM", self.asm_string, control.param_num,"ptrg_pot2_smth")
                    elif control.val == 3:
                        self.swap_param_strings("PARAM", self.asm_string, control.param_num,"ptrg_pot3_smth")
                    elif control.val == 4:
                        self.swap_param_strings("PARAM", self.asm_string, control.param_num,"ptrg_pot4_smth")
                    elif control.val == 5:  
                        self.swap_param_strings("PARAM", self.asm_string, control.param_num,"ptrg_pot5_smth")
                else: #if using a constant, val is the constant's value
                    pass
        self.swap_pots_with_constants()

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
        if connector == 1:
            return self.connector1
        if connector == 2:
            return self.connector2
        if connector == 3:
            return self.connector3      
        if connector == 4:
            return self.connector4
        if connector == 5:
            return self.connector5
        if connector == 6:
            return self.connector6

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

    def __init__(self,block,free_registers = {}, usage_state = 0, free_register = None, connector = 0,):
        
        self.name = block.name
        self.block = block
        self.controls = []
        self.usage_state = usage_state
        self.registers_used = free_registers

        if "Input" in self.name:
            self.directive_string = ""
            if "0" in self.name:
                self.asm_string = "\ncpy_cs    r0, in0;       Input 0\n"
            if "1" in self.name:
                self.asm_string = "\ncpy_cs    r0, in1;       Input 1\n"     
            if "2" in self.name:
                self.asm_string = "\ncpy_cs    r0, in2;       Input 2\n"
            if "3" in self.name:
                self.asm_string = "\ncpy_cs    r0, in3;       Input 3\n"

        if "Output" in self.name:
            self.directive_string = ""
            if "0" in self.name:
                self.asm_string = "\ncpy_sc    out0, r0;      Output 0\n"
            if "1" in self.name:
                self.asm_string = "\ncpy_sc    out1, r0;      Output 1\n"
            if "2" in self.name:
                self.asm_string = "\ncpy_sc    out2, r0;      Output 21\n"
            if "3" in self.name:
                self.asm_string = "\ncpy_sc    out3, r0;      Output 3\n"

        if "Pot" in self.name:
            self.connector1 = ""
            pass

        if "Switch" in self.name:
            self.connector1 = ""
            pass
            
        if "Constant" in self.name:
            self.connector1 = ""
            pass
              
        if "Tap Tempo" in self.name:
            self.connector1 = ""
            pass
  
        if "Mixer" in self.name:
            self.connector1 = 'Input Level 1'
            self.connector2 = 'Input Level 2'    
            self.asm_string = ""
            if self.usage_state == 1:
                if free_register is not None:
                    self.asm_string =  "\ncpy_cc    " +"r"+str(free_register) +", acc32     ;mixer state 1\n" # save the input from acc32 in the free register 
            elif self.usage_state == 2:
                free_register2 = self.get_free_register()
                self.asm_string +=     "\ncpy_cc    r" + str(free_register2) + ", acc32     ;mixer state 2\n" # copy from previous block acc32 output to free_register

                if connector == MIXER + 1: # previous block using mixer input 1
                    self.asm_string +=  "multrr    r" + str(free_register2) + ", $PARAM1$; in 1 level\n"  # multiply with input 1 level val and save in acc32
                    self.asm_string +=  "cpy_cc    r" + str(free_register2) + ", acc32\n"     # copy acc32 back to the spare register
                    self.asm_string +=  "multrr    r" + str(free_register)  + ", $PARAM2$; in 2 level\n"  # multiply with input 2 level val and save in acc32
                    self.asm_string +=  "cpy_cc    r" + str(free_register)  + ", acc32\n"     # copy acc32 back to the spare register  
                elif connector == MIXER + 2: # previous block using mixer input 2   
                    self.asm_string +=  "multrr    r" + str(free_register)  + ", $PARAM1$\n"  # multiply with input 1 level val and save in acc32
                    self.asm_string +=  "cpy_cc    r" + str(free_register)  + ", acc32\n"     # copy acc32 back to the spare register
                    self.asm_string +=  "multrr    r" + str(free_register2) + ", $PARAM2$\n"  # multiply with input 2 level val and save in acc32
                    self.asm_string +=  "cpy_cc    r" + str(free_register2) + ", acc32\n"     # copy acc32 back to the spare register  
                self.asm_string +=      "adds      r" + str(free_register)  + ", r" + str(free_register2) + "\n" #perform the weighted sum and save in acc32


        if "Splitter" in self.name:
            self.asm_string = ""
            if self.usage_state == 1:
                self.asm_string +=  "\ncpy_cc    r" + str(free_register)  + ", acc32     ;splitter state 1\n" #copy acc32 from input to the free register
            if self.usage_state == 2:
                self.asm_string +=  "\ncpy_cc    acc32, r" + str(free_register)  + "     ;splitter state 2\n"#copy the spare register to acc32 for output



#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////  PITCH SHIFT  ///////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if "Pitch" in self.name:
            self.connector1 = 'Pitch'
            self.connector2 = 'Level'
            self.connector3 = 'Dry Level'
            self.directive_string = """\n
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PITCH SHIFT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.equ      $EQU_shiftbase$    -1048576   ; shift of +1 octave
.mem      $MEM_pdelay$    4096          ; Define the delay block for the pitch delay
"""
            self.asm_string = """\n
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PITCH SHIFT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cpy_cs    $REG_temp$ , $PARAM1$    ; read in pot0
addsi     $REG_temp$ , -0.5        ; ranges -0.5 to 0.5 in acc32
wrdld     $REG_temp$ , $EQU_shiftbase$.u ; Put upper part of shiftbase into temp
multrr    acc32, $REG_temp$       ; Multiply the adjusted POT0 value by shiftbase
jgez      acc32, OK               ; If positive jump over the multiply by 2
sls       acc32, 1                ; Do the multiply by shifting left 1 bit
OK:
cpy_sc    ramp0_f, acc32          ; Write the result to the ramp0 frequency control

cpy_cc    $REG_input$ ,r0        ; Read channel 0 input
wrdel     $MEM_pdelay$, $REG_input$     ; Write it to the delay

pitch     rmp0|l4096, $MEM_pdelay$      ; Do the shift, result will be in ACC32
cpy_cs    $REG_temp$ , $PARAM2$    ; level from pot 1
multrr    $REG_temp$ , acc32       ; multiply it
cpy_cc    $REG_temp$ , acc32       ; and save to temp

cpy_cs    acc32, $PARAM3$         ; level from pot 2 for dry
multrr    r0, $REG_input$      ; multiply it
adds      r0, $REG_temp$       ; add result of first shifter
"""

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////  DISTORTION  ///////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# pot0 = Input gain
# pot1 = Low-pass frequency control
# pot2 = Low-pass Q control
# pot3 = Output level
        if "Distortion" in self.name:
            self.connector1 = 'Gain'
            self.connector2 = 'Low Pass Freq'
            self.connector3 = 'Low Pass Q'
            self.connector4 = 'Output Level'
            self.directive_string = """\n
.rn       temp      r0
.rn       temp2     r1
.rn       in        r2
.rn       inlp      r3
.rn       hp        r4
.rn       bp        r5
.rn       lp        r6
.rn       kf        r7
.rn       kq        r8\n
"""
            self.asm_string = """\n\n
; gain
cpy_cs    temp, in0
cpy_cs    temp, $PARAM1$
multrr    temp, temp2
sls       acc32, 4
adds      temp, acc32
cpy_cc    tmprg_in, acc32

; adjust pot1 for f control
; kf needs to range from 0.086 to about 0.95 
cpy_cs    tmprg_temp, $PARAM2$
multri    tmprg_temp, 0.864             ; Coefficient is high end - low end
addsi     acc32, 0.086            ; add in the low end
cpy_cc    tmprg_kf, acc32

; adjust pot2 for Q control
; range from about 0.8 to 0.05 for damping
cpy_cs    acc32, $PARAM3$        ; Read in pot1
addsi     acc32, -1.0             ; acc32 ranges -1 to 0
multri    acc32, 0.75             ; acc32 ranges -0.75 to 0
neg       acc32                   ; acc32 ranges 0.75 to 0
addsi     acc32, 0.05             ; acc32 ranges 0.8 to 0.05
cpy_cc    tmprg_kq, acc32

; distortion
; 0.5*IN + 0.8*(IN-sgn(IN)*IN^2)
multrr    tmprg_in, tmprg_in                  ; IN^2
jgez      tmprg_in, jp1                 ; if IN is positive jump
neg       acc32                   ; IN < 0 so negate it
jp1:
subs      tmprg_in, acc32               ; IN-sgn(IN)*IN^2
multri    acc32, 0.8              ; 0.8*(IN-sgn(IN)*IN^2)
cpy_cc    tmprg_temp, acc32             ; save to temp
sra       tmprg_in, 1                   ; 0.5*IN
adds      tmprg_temp, acc32             ; 0.5*IN + 0.8*(IN-sgn(IN)*IN^2)

; now the SVF 
; first a LP FIR with a null at Fs/2 to help make the filter stable
; and allow a wider range of coefficients
; input in acc32
sra       acc32, 1                ; in/2
cpy_cc    tmprg_temp, acc32             ; save to temp
adds      acc32, tmprg_inlp             ; in/2 + input LP
cpy_cc    tmprg_in, acc32               ; save to in
cpy_cc    tmprg_inlp, tmprg_temp              ; save in/2 to input LP
; now the svf
multrr    tmprg_kf, tmprg_bp                  ; Kf * BP
adds      tmprg_lp, acc32               ; + LP
cpy_cc    tmprg_lp, acc32               ; save to LP
multrr    tmprg_kq, tmprg_bp                  ; Kq * BP
adds      tmprg_lp, acc32               ; LP + Kq * BP
subs      tmprg_in, acc32               ; IN - (LP + Kq * BP)
cpy_cc    tmprg_hp, acc32               ; save to HP
multrr    tmprg_kf, tmprg_hp                  ; Kf * HP
adds      tmprg_bp, acc32               ; + BP
cpy_cc    tmprg_bp, acc32               ; Save to BP

cpy_cs    tmprg_temp, $PARAM4$         ; Adjust output level
multrr    tmprg_temp, tmprg_temp
multrr    acc32, lp""" 


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////  LOOPER  ///////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if "Looper" in self.name:
            self.directive_string = """
; sw0    - 0: play back recording forward
;          1: playback in reverse
; tap    - press to record, release to play
;
; If user holds tap longer than max recording time then program forces to playback state

.rn      temp      r0
.rn      ptr       r1
.rn      status    r2
.rn      xfade     r3
.rn      length    r4
.rn      bright    r5
.rn      bright2   r6


; status - 0 : Playback
;          1 : Record
;          2 : We are in a forced playback state but not first time
;          3 : Forced playback state, first time

.creg    status    0
.creg    ptr       0
.creg    length    0x100          ; Any value > 0 can be used as a default
"""
            self.asm_string = """\n\n
; first check for a forced playback state where user recorded longer than
; the 32K samples, special state as we need to ignore certain things
andi     status, 0x0002           ; are we in a forced playback state?
jz       acc32, normal            ; no so either a record or playback
andi     status, 0x0001           ; first time in forced playback?
jz       acc32, force_more        ; if not then check other force issues
andi     status, 0x0002           ; change status to forced but not first time
cpy_cc   status, acc32
xor      acc32, acc32             ; clear acc32
cpy_cc   ptr, acc32               ; reset the pointer
jmp      pb                       ; jump to playback
force_more:
andi     flags, taplvl            ; get the tap button state
jz       acc32, pb                ; if == 0 jump as user is still pushing it (pin has pull-up so pressed button is a 0)
xor      acc32, acc32             ; if here user has released it, clear acc32
cpy_cc   status, acc32            ; set status to playback, do not reset ptr as that should have been done on the first pass
jmp      pb


normal:
andi     flags, taplvl            ; get the tap button state
jnz      acc32, playback          ; if != 0 jump (pin has pull-up so pressed button is a 0)
andi     status, 0x0001           ; tap button pushed (is 0), was the last state record?
jnz      acc32, record            ; yes, continue recording
xor      acc32, acc32             ; nope, so starting a new recording
cpy_cc   ptr, acc32               ; reset pointer
cpy_cc   length, acc32            ; and length count
jmp      record                   ; and record

playback:
; Playback
andi     status, 0x0001           ; was the last state record?
jz       acc32, pb                ; no, continue playback
xor      acc32, acc32             ; yes it was
cpy_cc   ptr, acc32               ; reset pointer
cpy_cc   status, acc32            ; set status to playback
pb:
rddirx   acc32, ptr               ; read from current pointer position
cpy_cs   temp, in0                ; get the dry
adds     acc32, temp              ; add them
cpy_sc   out0, acc32              ; write to output
cpy_sc   out1, acc32              ; and to other output
; read sw0
cpy_cs   acc32, switch
andi     acc32, sw0
jz       acc32, forward           ; if switch 0 is 0 then forward playback
jz       ptr, ptr_zero            ; playing back backwards, if ptr is zero we need to reset it
subs     ptr, acc32               ; since the lsb was left set in the above andi we can just subtract
cpy_cc   ptr, acc32               ; copy updated pointer
jmp      over                     ; and jump past rest
ptr_zero:
subs     length, acc32            ; pointer was zero, need to rest to end
cpy_cc   ptr, acc32               ; which was easy as the lsb was set in acc32 already
jmp      over                     ; so just subtract it from the length, save it and jump

forward:
xor      acc32, acc32             ; clear the acc32
ori      acc32, 0x0001            ; set lsb
add      ptr, acc32               ; add to current ptr
cpy_cc   ptr, acc32               ; save it
subs     ptr, length              ; ptr - length
jnz      acc32, over              ; if !=0 then not at end jump over the rest
xor      acc32, acc32             ; if 0 then load 0 into acc32
cpy_cc   ptr, acc32               ; copy to ptr
jmp      over                     ; jump to end

record:
; read input and write to delay
xor      acc32, acc32             ; set status to record
ori      acc32, 0x0001
cpy_cc   status, acc32
cpy_cs   temp, in0                ; read input 0
wrdirx   ptr, temp                ; write to delay
cpy_sc   out0, temp               ; and to out0
cpy_sc   out1, temp               ; and to out1
xor      acc32, acc32             ; clear acc32
ori      acc32, 0x0001            ; set lsb
add      ptr, acc32               ; add to current ptr
cpy_cc   ptr, acc32               ; save it
cpy_cc   length, acc32            ; and save to length
xori     length, 0x8000           ; XOR length with 0x8000
jnz      acc32, over              ; if not 0 then not at max count
ori      acc32, 0x0003            ; passed the end, forced playback
cpy_cc   status, acc32


over:
cpy_cs    acc32, samplecnt        ; Get the sample counter
andi      acc32, 0xFF             ; Mask b[7:0]
jnz       acc32, doPWM0           ;

sr        ptr, 8
cpy_cc    bright, acc32           ; save it

doPWM0:
; Performing the decrement prior to driving the LED makes sure
; that the LED can go completly off.
addi      bright, -1              ; subtract 1 from on count
cpy_cc    bright, acc32           ; Save updated "bright"
xor       acc32, acc32            ; Clear acc32 for the LED off case
jneg      bright, doLED0          ;
ori       acc32, 1                ; Set acc32[0] for the LED on case

doLED0:
set       user0|0, acc32           ; set the usr0 output per the acc32 LSB

; PWM usr1
cpy_cs    acc32, samplecnt        ; Get the sample counter
andi      acc32, 0xFF             ; Mask b[7:0]
jnz       acc32, doPWM1           ;

sr        length, 8
cpy_cc    bright2, acc32          ; save it

doPWM1:
; Performing the decrement prior to driving the LED makes sure
; that the LED can go completly off.
addi      bright2, -1             ; subtract 1 from on count
cpy_cc    bright2, acc32          ; Save updated "bright"
xor       acc32, acc32            ; Clear acc32 for the LED off case
jneg      bright2, doLED1         ;
ori       acc32, 1                ; Set acc32[0] for the LED on case

doLED1:
set       user1|0, acc32           ; set the usr0 output per the acc32 LSB"""

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////// CHORUS  ///////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if "Chorus" in self.name:
            self.directive_string = """; Chorus - Mono in/out
; pot0 = rate
; pot1 = depth
; pot2 = level
; pot3 = 
; pot4 = 
; pot5 =  

.equ    fs          48000
.equ    flow        .2
.equ    fhigh       10
.equ    pi          3.14159
.equ    clow        (2^31 - 1) * (2*pi*flow)/fs
.equ    chigh       (2^31 - 1) * (2*pi*fhigh)/fs
.equ    cdiff       chigh - clow

.mem    delay       1024

.rn     temp        r0
.rn     voice1      r1
.rn     voice2      r2
.rn     voice3      r3
.rn     bright      r4 """

            self.asm_string = """
cpy_cs  temp, pot0_smth           ; read in frequency control pot
wrdld   acc32, cdiff.u            ; load difference between low and high frequency
ori     acc32, cdiff.l
multrr  temp, acc32               ; pot0 * cdiff
cpy_cc  temp, acc32
wrdld   acc32, clow.u             ; load low freq coeff
ori     acc32, clow.l
adds    acc32, temp               ; add low freq
cpy_sc  lfo0_f, acc32             ; write to lfo0 frequency control

cpy_cs  temp, pot1_smth           ; read in depth control pot
wrdld   acc32, 400
multrr  temp, acc32
cpy_cc  r15, acc32

cpy_cs  temp, in0
wrdel   delay, temp

; voice 1
chr     lfo0|sin delay+1400
cpy_cc  voice1, acc32

; voice 2
chr     lfo0|cos delay+256
cpy_cc  voice2, acc32

; voice 3
chr     lfo0|sin|neg delay+16
cpy_cc  voice3, acc32

; voice 4
chr     lfo0|cos|neg delay+768

; sum the voices
adds    acc32, voice3
adds    acc32, voice2
adds    acc32, voice1

; get effects level pot and scale effect
cpy_cs  temp, pot2_smth
multrr  acc32, temp

; add in dry
cpy_cs  temp, in0
adds    acc32, temp

; write it
cpy_sc  out0, acc32
cpy_sc  out1, acc32


; The PWM value becomes updated every 256 samples translating to a
; PWM frequency of 125Hz @32k with 8 bit resolution.
; While this is not exactly a high resolution PWM it might still
; good enough for generating basic control voltages in some applications.
; For driving the LEDs in this case it is perfectly enough.
cpy_cs    acc32, samplecnt        ; Get the sample counter
andi      acc32, 0xFF             ; Mask b[7:0]
jnz       acc32, doPWM            ;

; Reload new PWM value from LFO0_s into "bright"
cpy_cs    temp, lfo0_s            ; read in sin wave ranges -1.0 to +1.0 (well, almost)
sra       temp, 1                 ; /2 to +/- 1/2
addsi     acc32, 0.5              ; ranges 0 to 1
sra       acc32, 23               ; shift the PWM value in place
cpy_cc    bright, acc32           ; save it

doPWM:
; Performing the decrement prior to driving the LED makes sure
; that the LED can go completly off.
addi      bright, -1              ; suntract 1 from on time
cpy_cc    bright, acc32           ; Save updated "bright"
xor       acc32, acc32            ; Clear acc32 for the LED off case
jneg      bright, doLED           ;
ori       acc32, 1                ; Set acc32[0] for the LED on case

doLED:
set       user0|0, acc32           ; set the usr1 output per the acc32 LSB"""