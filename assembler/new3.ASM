format PE console

entry Start

include 'win32a.inc'

section '.data' data readable writable

        spaceStr db '%d', 0

        input dd ?
        deadStr db 'There was a trap. You died!', 0
        startStr db 'You found yourself stuck in a maze. What would you do?', 10
        go1Str db 'You can go left(1), straight(2), right(3): ', 0
        go2Str db 'You are at the next room.', 10
        winStr db 'You found exit. Congratulations!!', 0

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
                push go1Str

                push input
                push spaceStr
                call [scanf]

                ;mov ecx, [input]
                ;push ecx
                ;push spaceStr
                ;call [printf]

                cmp [input], 2
                jne Dead

                push go2Str
                call [printf]
                push go1Str


                push input
                push spaceStr
                call [scanf]

                cmp [input], 2
                jne Dead

                push go2Str
                call [printf]
                push go1Str


                push input
                push spaceStr
                call [scanf]

                cmp [input], 1
                jne Dead

                push go2Str
                call [printf]
                push go1Str


                push input
                push spaceStr
                call [scanf]

                cmp [input], 3
                jne Dead

                push winStr
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
