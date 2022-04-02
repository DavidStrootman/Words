.cpu cortex-m0
.bss 
.byte 0
test:
.byte 0
.global setup, loop

setup: 
mov r4, lr
mov pc, r4
loop: 
mov pc, lr

