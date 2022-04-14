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
mov r1, r3
pop { r3 }
push { r5 }
push { r1 }

@ Function body:
push { r3 }
mov r0, #0
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
blt true_line2_496bba12
false_line2_464a0669:
mov r0, #0
true_line2_496bba12:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line3_d2ac7e80
if_body_of_if_on_line3_d2ac7e80:
mov r0, #0
push { r0 }
mov r0, #1
push { r0 }
pop { r0, r1 }
sub r0, r1, r0
push { r0 }
b end_if_on_line3_d2ac7e80
else_body_of_if_on_line3_d2ac7e80:
push { r3 }
mov r0, #0
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line6_1d312c24
false_line6_6c02750b:
mov r0, #0
true_line6_1d312c24:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line7_d6c27de3
if_body_of_if_on_line7_d6c27de3:
mov r0, #0
push { r0 }
b end_if_on_line7_d6c27de3
else_body_of_if_on_line7_d6c27de3:
push { r3 }
mov r0, #1
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line10_5afdc7ab
false_line10_ff0ab482:
mov r0, #0
true_line10_5afdc7ab:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line11_4ff0df76
if_body_of_if_on_line11_4ff0df76:
mov r0, #1
push { r0 }
b end_if_on_line11_4ff0df76
else_body_of_if_on_line11_4ff0df76:
push { r3 }
mov r0, #2
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line14_6fa14bfc
false_line14_65c45751:
mov r0, #0
true_line14_6fa14bfc:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line15_3485e10b
if_body_of_if_on_line15_3485e10b:
mov r0, #1
push { r0 }
b end_if_on_line15_3485e10b
else_body_of_if_on_line15_3485e10b:
push { r3 }
mov r0, #1
push { r0 }
pop { r0, r1 }
sub r0, r1, r0
push { r0 }
bl FIBONACCI
push { r3 }
mov r0, #2
push { r0 }
pop { r0, r1 }
sub r0, r1, r0
push { r0 }
bl FIBONACCI
pop { r0, r1 }
add r0, r1, r0
push { r0 }
end_if_on_line15_3485e10b:
end_if_on_line11_4ff0df76:
end_if_on_line7_d6c27de3:
end_if_on_line3_d2ac7e80:

@ Function end cleanup:
@ return value, assuming function solves:
pop { r6 }
pop { r3 }
@ link register:
pop { r7 }
push { r6 }
mov pc, r7
FIBONACCI_end:
@ End of function FIBONACCI at line 0

loop: 
b loop
 
