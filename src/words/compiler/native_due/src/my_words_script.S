.cpu cortex-m0
.align 2
.text

.global setup, loop

setup: 
bl serial_begin
mov r0, #2
mov r1, #1
bl a_unittest 

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
blt true_line2_477804cb
false_line2_3900d4d8:
mov r0, #0
true_line2_477804cb:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line3_a2820d54
if_body_of_if_on_line3_a2820d54:
mov r0, #0
push { r0 }
mov r0, #1
push { r0 }
pop { r0, r1 }
sub r0, r1, r0
push { r0 }
b end_if_on_line3_a2820d54
else_body_of_if_on_line3_a2820d54:
push { r3 }
mov r0, #0
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line6_0cb7f72c
false_line6_cf763167:
mov r0, #0
true_line6_0cb7f72c:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line7_974b0436
if_body_of_if_on_line7_974b0436:
mov r0, #0
push { r0 }
b end_if_on_line7_974b0436
else_body_of_if_on_line7_974b0436:
push { r3 }
mov r0, #1
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line10_2ced932a
false_line10_bf169317:
mov r0, #0
true_line10_2ced932a:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line11_e3020836
if_body_of_if_on_line11_e3020836:
mov r0, #1
push { r0 }
b end_if_on_line11_e3020836
else_body_of_if_on_line11_e3020836:
push { r3 }
mov r0, #2
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line14_5db8c426
false_line14_10d94161:
mov r0, #0
true_line14_5db8c426:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line15_a50f90c9
if_body_of_if_on_line15_a50f90c9:
mov r0, #1
push { r0 }
b end_if_on_line15_a50f90c9
else_body_of_if_on_line15_a50f90c9:
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
end_if_on_line15_a50f90c9:
end_if_on_line11_e3020836:
end_if_on_line7_974b0436:
end_if_on_line3_a2820d54:

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
 
