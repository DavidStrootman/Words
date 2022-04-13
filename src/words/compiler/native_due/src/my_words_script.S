.cpu cortex-m0
.align 2
.text

.global setup, loop

setup: 
bl serial_begin
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
pop { r3, r4 }
push { r5 }
push { r3, r4 }
push { r3 }
mov r0, #0
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line2_2b72d160
false_line2_8fb91504:
mov r0, #0
true_line2_2b72d160:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line3_d37bf7f7
if_body_of_if_on_line3_d37bf7f7:
push { r4 }
mov r0, #1
push { r0 }
pop { r0, r1 }
add r0, r1, r0
push { r0 }
b end_if_on_line3_d37bf7f7
else_body_of_if_on_line3_d37bf7f7:
push { r4 }
mov r0, #0
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line6_f86776b8
false_line6_4e192073:
mov r0, #0
true_line6_f86776b8:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line7_e90d3edb
if_body_of_if_on_line7_e90d3edb:
mov r0, #1
push { r0 }
push { r3 }
mov r0, #1
push { r0 }
pop { r0, r1 }
sub r0, r1, r0
push { r0 }
bl ACKERMANN
b end_if_on_line7_e90d3edb
else_body_of_if_on_line7_e90d3edb:
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
end_if_on_line7_e90d3edb:
end_if_on_line3_d37bf7f7:
@ r6 holds return, r7 holds lr
pop { r6 }
pop { r3, r4 }
pop { r7 }
push { r6 }
mov pc, r7
ACKERMANN_end:
@ End of function ACKERMANN at line 0
loop: 
b loop
 
