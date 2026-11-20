
// Make the Computer Draw a Box
// K = 20
// Width = 16 pixels
// Height = 20 pixels
// Starting row = 20

(LOOP)
    @KBD
    D=M
    @DRAW
    D;JGT

    @ERASE
    0;JMP

(DRAW)
    @17024
    D=A
    @addr
    M=D

    @20
    D=A
    @count
    M=D

(DRAWLOOP)
    @addr
    A=M
    M=-1

    @32
    D=A
    @addr
    M=D+M

    @count
    MD=M-1
    @DRAWLOOP
    D;JGT

    @LOOP
    0;JMP

(ERASE)
    @17024
    D=A
    @addr
    M=D

    @20
    D=A
    @count
    M=D

(ERASELOOP)
    @addr
    A=M
    M=0

    @32
    D=A
    @addr
    M=D+M

    @count
    MD=M-1
    @ERASELOOP
    D;JGT

    @LOOP
    0;JMP
