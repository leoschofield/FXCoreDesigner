#============================================================================================================================================================================
#============================================================================================================================================================================
#============================================================================================================================================================================
class asm_node():
    def swap_strings(self,searchString,startString,paramNum,newString):
        createdString = ""
        p_before =  startString.partition("$"+searchString)[0] #input string before first find string
        p_after =  startString.partition("$"+searchString)[2] #input string after first find string
        stringParam = p_after.partition("$")[0] # search for number before second $
        p_after2 = p_after.partition("$")[2] # rest of string after second $
        if stringParam != "":
            if int(stringParam)==paramNum:    # !!TODO!! error here if 2 or more control params used - fix change recursion tactic which finds the "PARAM2,3,4 etc as this is truncating the ASM string, which is then saved, next time a conenctor is added to that node the bad things happen"
                createdString = p_before + newString + p_after2
            else:
                self.swap_strings(searchString,p_after2,paramNum,newString)#recursion to find correct searchString if its not the one found
        else: #got to the end of the string so start over
            self.swap_strings(searchString,self.asm_string,paramNum,newString)#recursion with initial string
        if createdString != "":
            self.asm_string = createdString

    def add_control(self,paramNum, controlType,val):
        if controlType == 1: #if using a potentiometer or expression input
            if val == 1:#val is the potentiometer number (1 here == pot0 on the dev board)
                self.swap_strings("PARAM", self.asm_string, paramNum,"ptrg_pot0_smth")
            elif val == 2:
                self.swap_strings("PARAM", self.asm_string, paramNum,"ptrg_pot1_smth")
            elif val == 3:
                self.swap_strings("PARAM", self.asm_string, paramNum,"ptrg_pot2_smth")
            elif val == 4:  
                self.swap_strings("PARAM", self.asm_string, paramNum,"ptrg_pot3_smth")
            elif val == 5:
                self.swap_strings("PARAM", self.asm_string, paramNum,"ptrg_pot4_smth")
            elif val == 6:  
                self.swap_strings("PARAM", self.asm_string, paramNum,"ptrg_pot5_smth")
        else: #if using a constant, val is the constant's value
            pass

    def __init__(self,name,ser_position,par_position):
        self.name = name
        self.controls = []
        self.ser_position = ser_position
        self.par_position = par_position
        if "Input" in self.name:
            self.directive_string = ""
            if "1" in self.name:
                self.asm_string = "cpy_cs    acc32, in0\n"
            if "2" in self.name:
                self.asm_string = "cpy_cs    acc32, in1\n"     
            if "3" in self.name:
                self.asm_string = "cpy_cs    acc32, in2\n"
            if "4" in self.name:
                self.asm_string = "cpy_cs    acc32, in3\n"

        if "Output" in self.name:
            self.directive_string = ""
            if "1" in self.name:
                self.asm_string = "cpy_cs    out0, acc32\n"
            if "2" in self.name:
                self.asm_string = "cpy_cs    out1, acc32\n"
            if "3" in self.name:
                self.asm_string = "cpy_cs    out2, acc32\n"
            if "4" in self.name:
                self.asm_string = "cpy_cs    out3, acc32\n"

        if "Pot" in self.name:
            pass

        if "Switch" in self.name:
            pass
            
        if "Constant" in self.name:
            pass
  
        if "Mixer" in self.name:
            pass

        if "Splitter" in self.name:
            pass

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if "Pitch" in self.name:
            self.directive_string = """.equ      shiftbase    -1048576   ; shift of +1 octave

.rn       temp      r0            ; temp reg
.rn       input     r1            ; input

; Define the delay block for the pitch delay
.mem      pdelay    4096"""

            self.asm_string = """; single pitch shift mono in/out based on default program double pitch shifter
;PARAM1 pot0 = shifter 0 
;PARAM2 pot1 = level
;PARAM3 pot2 = dry level
cpy_cs    tmprg_temp, $PARAM1$        ; read in - pot0 ptrg_pot0_smth
addsi     tmprg_temp, -0.5              ; ranges -0.5 to 0.5 in acc32
wrdld     tmprg_temp,shiftbase.u        ; Put upper part of shiftbase into temp
multrr    acc32, tmprg_temp             ; Multiply the adjusted POT0 value by shiftbase
jgez      acc32, OK               ; If positive jump over the multiply by 2
sls       acc32, 1                ; Do the multiply by shifting left 1 bit
OK:
cpy_sc    ramp0_f, acc32          ; Write the result to the ramp0 frequency control

cpy_cs    tmprg_input, in0 ; Read channel 0 input
wrdel     pdelay, tmprg_input           ; Write it to the delay

pitch     rmp0|l4096, pdelay      ; Do the shift, result will be in ACC32
cpy_cs    tmprg_temp,  $PARAM2$         ; level from pot 1 ptrg_pot1_smth
multrr    tmprg_temp, acc32             ; multiply it
cpy_cc    tmprg_temp, acc32             ; and save to temp

cpy_cs    acc32, $PARAM3$               ; level from pot 2 for dry ptrg_pot2_smth
multrr    acc32, tmprg_input            ; multiply it
adds      acc32, tmprg_temp             ; add result of first shifter""" 


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if "Distortion" in self.name:
            directive_string = """
; pot0 = Input gain
; pot1 = Low-pass frequency control
; pot2 = Low-pass Q control
; pot3 = Output level

.rn       temp      r0
.rn       temp2     r1
.rn       in        r2
.rn       inlp      r3
.rn       hp        r4
.rn       bp        r5
.rn       lp        r6
.rn       kf        r7
.rn       kq        r8
"""
            self.asm_string = """
; gain
cpy_cs    tmprg_temp, in0
cpy_cs    tmprg_temp2, ptrg_pot0_smth
multrr    tmprg_temp, tmprg_temp2
sls       acc32, 4
adds      tmprg_temp, acc32
cpy_cc    tmprg_in, acc32

; adjust pot1 for f control
; kf needs to range from 0.086 to about 0.95 
cpy_cs    tmprg_temp, ptrg_pot1_smth
multri    tmprg_temp, 0.864             ; Coefficient is high end - low end
addsi     acc32, 0.086            ; add in the low end
cpy_cc    tmprg_kf, acc32

; adjust pot2 for Q control
; range from about 0.8 to 0.05 for damping
cpy_cs    acc32, ptrg_pot2_smth        ; Read in pot1
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

cpy_cs    tmprg_temp, ptrg_pot3_smth         ; Adjust output level
multrr    tmprg_temp, tmprg_temp
multrr    acc32, lp""" 


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if "Looper" in self.name:
            directive_string = """
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
    asm_string = """; first check for a forced playback state where user recorded longer than
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