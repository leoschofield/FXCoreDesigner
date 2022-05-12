class Input1Block():
    def __init__(self, **kwargs): 
        super(Input1Block, self).__init__(**kwargs)

        self.reg_string = ".rn       signal1      **REGISTER**"
        self.code_string = "cpy_cs    signal1, in0"


class Input2Block():
    def __init__(self, **kwargs): 
        super(Input2Block, self).__init__(**kwargs)

        self.reg_string = ".rn       signal2      **REGISTER**"
        self.code_string = "cpy_cs    signal2, in1"


class Input3Block():
    def __init__(self, **kwargs): 
        super(Input3Block, self).__init__(**kwargs)

        self.reg_string = ".rn       signal3      **REGISTER**"
        self.code_string = "cpy_cs    signal3, in2"


class Input4Block():
    def __init__(self, **kwargs): 
        super(Input4Block, self).__init__(**kwargs)

        self.reg_string = ".rn       signal4      **REGISTER**"
        self.code_string = "cpy_cs    signal4, in4"


