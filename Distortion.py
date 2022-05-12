class DistortionBlock():
    def __init__(self, gain_pot,freq_pot,q_pot, vol_pot, **kwargs): 
        super(DistortionBlock, self).__init__(**kwargs)
        self.gain_pot = gain_pot
        self.freq_pot = freq_pot
        self.q_pot = q_pot
        self.vol_pot = vol_pot
        self.reg_string = ""
        self.code_string = """
                            ;***************************** gain
                            cpy_cs    reg_temp1, reg_pot1_smth
                            multrr    reg_input1, reg_temp1
                            sls       acc32, 4
                            adds      reg_input1, acc32
                            cpy_cc    reg_temp1, acc32 ; reg_temp1 was 'in'

                            ;***************************** distortion
                            ; 0.5*IN + 0.8*(IN-sgn(IN)*IN^2)
                            multrr    reg_temp1, reg_temp1      ; IN^2
                            jgez      reg_temp1, jp1           ; if IN is positive jump
                            neg       acc32                   ; IN < 0 so negate it
                            jp1:
                            subs      reg_temp1, acc32           ; IN-sgn(IN)*IN^2
                            multri    acc32, 0.8              ; 0.8*(IN-sgn(IN)*IN^2)
                            cpy_cc    reg_temp2, acc32             ; save to temp
                            sra       reg_input1, 1                   ; 0.5*IN
                            adds      reg_temp2, acc32             ; 0.5*IN + 0.8*(IN-sgn(IN)*IN^2)

                          
                          
                            ;***************************** output level
                            cpy_cs    reg_temp2, reg_pot2_smth
                            multrr    reg_temp2, reg_temp2
                            multrr    reg_out1, reg_temp1

                            cpy_sc    reg_out1, acc32             
                            """


