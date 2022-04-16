.cpu cortex-m0
.align 2
.text

.global setup, loop

setup: 
bl serial_begin
mov r0, #2
mov r1, #1
bl a_unittest 

mov r0, #2
push { r0 }
mov r0, #2
push { r0 }
bl ACKERMANN
pop { r0 }
bl print_num
push { r0 }

@ Start of function ACKERMANN at line 0
b ACKERMANN_end 
ACKERMANN:
mov r5, lr
mov r1, r3
mov r2, r4
pop { r3, r4 }
push { r5 }
push { r1, r2 }

@ Function body:
push { r3 }
mov r0, #0
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line2_b5a4ed3a
false_line2_21a94e2c:
mov r0, #0
true_line2_b5a4ed3a:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line3_692d454f
if_body_of_if_on_line3_692d454f:
push { r4 }
mov r0, #1
push { r0 }
pop { r0, r1 }
add r0, r1, r0
push { r0 }
b end_if_on_line3_692d454f
else_body_of_if_on_line3_692d454f:
push { r4 }
mov r0, #0
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line6_039c1d28
false_line6_7a046919:
mov r0, #0
true_line6_039c1d28:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line7_4d5a0cdc
if_body_of_if_on_line7_4d5a0cdc:
mov r0, #1
push { r0 }
push { r3 }
mov r0, #1
push { r0 }
pop { r0, r1 }
sub r0, r1, r0
push { r0 }
bl ACKERMANN
b end_if_on_line7_4d5a0cdc
else_body_of_if_on_line7_4d5a0cdc:
push { r4 }
mov r0, #1
push { r0 }
pop { r0, r1 }
sub r0, r1, r0
push { r0 }
push { r3 }
bl ACKERMANN
push { r3 }
mov r0, #1
push { r0 }
pop { r0, r1 }
sub r0, r1, r0
push { r0 }
bl ACKERMANN
end_if_on_line7_4d5a0cdc:
end_if_on_line3_692d454f:

@ Function end cleanup:
@ return value, assuming function solves:
pop { r6 }
pop { r3, r4 }
@ link register:
pop { r7 }
push { r6 }
mov pc, r7
ACKERMANN_end:
@ End of function ACKERMANN at line 0

loop: 
b loop
 
