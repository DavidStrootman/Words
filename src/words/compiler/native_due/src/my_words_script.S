.cpu cortex-m0
.align 2
.text

.global setup, loop

setup: 
bl serial_begin
mov r0, #3
push { r0 }
bl FIBONACCI
pop { r0 }
bl print_num
push { r0 }
mov r0, #4
push { r0 }
bl FIBONACCI
pop { r0 }
bl print_num
push { r0 }
mov r0, #5
push { r0 }
bl FIBONACCI
pop { r0 }
bl print_num
push { r0 }
mov r0, #10
push { r0 }
bl FIBONACCI
pop { r0 }
bl print_num
push { r0 }

@ Start of function FIBONACCI at line 0
b FIBONACCI_end 
FIBONACCI:
mov r5, lr
mov r8, r3
pop { r3 }
push { r5 }
mov r0, r8
push { r0 }
push { r3 }
mov r0, #0
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
blt true_line2_d5c4bdd9
false_line2_c14ed9ac:
mov r0, #0
true_line2_d5c4bdd9:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line3_56773126
if_body_of_if_on_line3_56773126:
mov r0, #0
push { r0 }
mov r0, #1
push { r0 }
pop { r0, r1 }
sub r1, r1, r0
push { r1 }
b end_if_on_line3_56773126
else_body_of_if_on_line3_56773126:
push { r3 }
mov r0, #0
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line6_35d67a51
false_line6_781de5c3:
mov r0, #0
true_line6_35d67a51:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line7_fe359b4a
if_body_of_if_on_line7_fe359b4a:
mov r0, #0
push { r0 }
b end_if_on_line7_fe359b4a
else_body_of_if_on_line7_fe359b4a:
push { r3 }
mov r0, #1
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line10_b98342fd
false_line10_f41899ec:
mov r0, #0
true_line10_b98342fd:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line11_21b0d6bf
if_body_of_if_on_line11_21b0d6bf:
mov r0, #1
push { r0 }
b end_if_on_line11_21b0d6bf
else_body_of_if_on_line11_21b0d6bf:
push { r3 }
mov r0, #2
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line14_3ee9148b
false_line14_1e1bd443:
mov r0, #0
true_line14_3ee9148b:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line15_02a12eb7
if_body_of_if_on_line15_02a12eb7:
mov r0, #1
push { r0 }
b end_if_on_line15_02a12eb7
else_body_of_if_on_line15_02a12eb7:
push { r3 }
mov r0, #1
push { r0 }
pop { r0, r1 }
sub r1, r1, r0
push { r1 }
bl FIBONACCI
push { r3 }
mov r0, #2
push { r0 }
pop { r0, r1 }
sub r1, r1, r0
push { r1 }
bl FIBONACCI
pop { r0, r1 }
add r1, r1, r0
push { r1 }
end_if_on_line15_02a12eb7:
end_if_on_line11_21b0d6bf:
end_if_on_line7_fe359b4a:
end_if_on_line3_56773126:
@ r6 holds return, r7 holds lr
pop { r6 }
pop { r3 }
pop { r7 }
push { r6 }
mov pc, r7
FIBONACCI_end:
@ End of function FIBONACCI at line 0
loop: 
b loop
 
