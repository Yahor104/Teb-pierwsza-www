format PE console

entry Start

include 'win32a.inc'

section '.data' data readable writable

        spaceStr db '%d', 0

        input dd ?
        deadStr db 'There was a trap. You died!', 0
        startStr db 'You found yourself stuck in a maze. What would you do?', 10
        goStr db 'You can go left(1), straight(2), right(3): ', 0

section '.code' code readable executable

        Dead:
                push deadStr
                call [printf]
                call [getch]
                push 0
                call [ExitProcess]

        Start:
                push startStr
                call [printf]
                push goStr

                push input
                push spaceStr
                call [scanf]

                mov ecx, [input]
                push ecx
                push spaceStr
                call [printf]

                cmp ecx, 50
                jne Dead

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