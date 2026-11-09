format PE console

entry Start

include 'win32a.inc'

section '.data' data readable writable

        num dd 0
        spaceStr db ' %d'

section '.code' code readable executable

        Start:
                mov ecx, [num]
                push ecx
                push spaceStr
                call [printf]

                add [num], 1

                call [getch]
                jmp Start

section '.idata' import data readable

        library kernel, 'kernel32.dll',\
                msvcrt, 'msvcrt.dll'

        import kernel,\
               ExitProcess, 'ExitProcess'

        import msvcrt,\
               printf, 'printf',\
               getch, '_getch'