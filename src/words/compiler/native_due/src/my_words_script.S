.cpu cortex-m0
.bss 
.byte 0
test:
.byte 0
.global setup, loop

setup: 
b ACKERMANN_end
ACKERMANN:
pop {r4, r5}
push {r4}
mov r0, #0
push {r0}
pop {r0, r1}
mov r0, #1
beq true_line2_17e49d19
false_line2_c3d63403:
mov r0, #0
true_line2_17e49d19:
push {r0}
ACKERMANN_end:
mov r0, #4
push {r0}
mov r0, #3
push {r0}
b ACKERMANN
loop: 

