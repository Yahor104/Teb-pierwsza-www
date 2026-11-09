format PE console

entry Start

include 'win32a.inc'

section '.data' data readable writable

        strA db 'Enter A: ', 0
        strB db 'Enter B: ', 0

        spaceStr db ' %d', 0

        resStr db '0', 0

        A dd ?
        B dd ?

section '.code' code readable executable

        Start:
                push strA
                call [printf]

                push A
                push spaceStr
                call [scanf]

                push strB
                call [printf]

                push B
                push spaceStr
                call [scanf]

                mov ecx, [A]
                add ecx, [B]

                push ecx
                push spaceStr
                call [printf]

                call [getch]
                push 0
                call [ExitProcess]

section '.idata' import data readable

        library kernel, 'kernel32.dll',\
               msvcrt, 'msvcrt.dll'

        import kernel,\
               ExitProcess, 'ExitProcess'

        import msvcrt,\
               printf, 'printf',\
               scanf, 'scanf',\
               getch, '_getch'