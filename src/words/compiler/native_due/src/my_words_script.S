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
blt true_line2_d23cbdd6
false_line2_ec34894d:
mov r0, #0
true_line2_d23cbdd6:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line3_30004883
if_body_of_if_on_line3_30004883:
mov r0, #0
push { r0 }
mov r0, #1
push { r0 }
pop { r0, r1 }
sub r1, r1, r0
push { r1 }
b end_if_on_line3_30004883
else_body_of_if_on_line3_30004883:
push { r3 }
mov r0, #0
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line6_08e934b9
false_line6_1d0cc3a8:
mov r0, #0
true_line6_08e934b9:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line7_7319c0f4
if_body_of_if_on_line7_7319c0f4:
mov r0, #0
push { r0 }
b end_if_on_line7_7319c0f4
else_body_of_if_on_line7_7319c0f4:
push { r3 }
mov r0, #1
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line10_a81d3663
false_line10_190d0f00:
mov r0, #0
true_line10_a81d3663:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line11_4369da5c
if_body_of_if_on_line11_4369da5c:
mov r0, #1
push { r0 }
b end_if_on_line11_4369da5c
else_body_of_if_on_line11_4369da5c:
push { r3 }
mov r0, #2
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line14_5257d35a
false_line14_a2ce6843:
mov r0, #0
true_line14_5257d35a:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line15_73674a76
if_body_of_if_on_line15_73674a76:
mov r0, #1
push { r0 }
b end_if_on_line15_73674a76
else_body_of_if_on_line15_73674a76:
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
end_if_on_line15_73674a76:
end_if_on_line11_4369da5c:
end_if_on_line7_7319c0f4:
end_if_on_line3_30004883:

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
 
