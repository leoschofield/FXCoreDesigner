@echo off
"C:\Program Files (x86)\Experimental Noize\FXCore Assembler\FXCoreCmdAsm.exe" %1 %2 %3 %4
if %errorlevel% EQU 0 (echo. & echo NO ERRORS ) Else ( echo. & echo ERROR FAILED &color CF )
pause