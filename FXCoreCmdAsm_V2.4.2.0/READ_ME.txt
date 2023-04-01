FXCore Command Line Assembler V2.4.X 22 Feb 2023
NOTE: Only FXCoreCmdAsm.exe was updated, if you have already installed V2.2/3.X
just copy FXCoreCmdAsm.exe over the old one

The FXCore command line assembler provides the assembly, download and programming
functions and allows the user to use an external editor of their
choice and add commands to call it from their desired editor.

Starting with V2.0 we no longer use the FT260 specific dll and use the
HIDSharp dll, this is an open source library released under the
Apache open source license. 

We will be using the free Notepad++ editor and explain how to install the
assembler and configure Notepad++ to use it.

Unzip the archive into a directory and follow the below instructions.


Part A: Installing the command line assembler.

1. If you have installed a previous version of the command line assembler 
please jump to 2 below. 
If you have not already installed the assembler then 
create the directory path: 

C:\Program Files (x86)\Experimental Noize\FXCore Assembler

Note the spaces in the path.

2. Copy the files FXCoreCmdAsm.exe, assemble.cmd and HidSharp.dll into the
"C:\Program Files (x86)\Experimental Noize\FXCore Assembler" directory.
NOTE: The assemble.cmd file has not changed from prior versions so you
can skip copying this file if you have one from a previous install or you
have customized it. 
FXCoreCmdAsm.exe is the actual assembler, help can be seen by using the "-h"
parameter from the command line like:
FXCoreCmdAsm.exe -h
The assemble.cmd file is a small shell script called from Notepad++


Part B: Install/Configure Notepad++ 
NOTE: There have been no changes to the UDL file so if you have already
done this with a prior version there is no need to redo this or to
recreate the run commands.

1. If you have Notepad++ installed already please jump to 2 below.
Get Notepad++ from: https://notepad-plus-plus.org/downloads/

Get the installer package and run it with all the defaults.

2. If Notepad++ is open, please close it. We now need to set up the 
FXCore assembly language in Notepad++ so it will do syntax highlighting.
Copy the file FXCoreAsmUDL.xml into:
C:\Users\your_user_name\AppData\Roaming\Notepad++\userDefineLangs
replacing "your_user_name" with your username on your computer.

3. Start Notepad++, if this was a new install close the change log file
it will open. 
On the main menu select: Run -> Run...
This will open a small pop-up "The Program to Run", in the field paste 
in the following including all quotes:

"C:\Program Files (x86)\Experimental Noize\FXCore Assembler\assemble.cmd" -a "$(FULL_CURRENT_PATH)"

Press "Save..." and in the new pop-up enter:

Assemble FXCore

And press "OK", this will return you to the first pop-up. Clear the 
field and enter:

"C:\Program Files (x86)\Experimental Noize\FXCore Assembler\assemble.cmd" -r "$(FULL_CURRENT_PATH)"

Press "Save..." and in the new pop-up enter:

Run FXCore 0x30

And press "OK", this will return you to the first pop-up. Clear the 
field and enter:

notepad++ "$(CURRENT_DIRECTORY)\$(NAME_PART).lst"

Press "Save..." and in the new pop-up enter:

View FXCore Program Listing

And press "OK", this will return you to the first pop-up. This time 
press Cancel.

Load an FXCore program, the syntax highlighting should be automatic as
the .fxc extension of the file tells Notepad++ what langiage it is. If 
it does not then you can manually select the language from 
Language -> FXCore Assembler in the main menu.

Now if you look at the Run main menu you will see 3 new commands:
Assemble FXCore
Run FXCore 0x30
View FXCore Program Listing

Once the .fxc file is loaded, select Run-> Assemble FXCore
A terminal window will pop up and show the result of assembly. If there
are any errors select Run->View FXCore Program Listing to open the 
listing file in Notepad++

If you want to do a run from ram then select Run->Run FXCore 0x30
and it will load the program into a connected FXCore Dev board and
run the program. It assumes the I2C address is set to 0x30 for the
FXCore. 

Now you have Notepad++ configured for FXCore syntax highlighting
and basic operation of the dev board. You can add additional commands
to do things like program specific locations in the FXCore, generate
HEX and C header files, etc. just like the GUI version. 