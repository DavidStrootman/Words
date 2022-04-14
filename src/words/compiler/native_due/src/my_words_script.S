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
blt true_line2_4a2ba0c1
false_line2_bb360f8b:
mov r0, #0
true_line2_4a2ba0c1:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line3_f68ff6ce
if_body_of_if_on_line3_f68ff6ce:
mov r0, #0
push { r0 }
mov r0, #1
push { r0 }
pop { r0, r1 }
sub r0, r1, r0
push { r0 }
b end_if_on_line3_f68ff6ce
else_body_of_if_on_line3_f68ff6ce:
push { r3 }
mov r0, #0
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line6_aca35591
false_line6_dd36eb83:
mov r0, #0
true_line6_aca35591:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line7_826c27f4
if_body_of_if_on_line7_826c27f4:
mov r0, #0
push { r0 }
b end_if_on_line7_826c27f4
else_body_of_if_on_line7_826c27f4:
push { r3 }
mov r0, #1
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line10_75804a18
false_line10_41a864d7:
mov r0, #0
true_line10_75804a18:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line11_d2999534
if_body_of_if_on_line11_d2999534:
mov r0, #1
push { r0 }
b end_if_on_line11_d2999534
else_body_of_if_on_line11_d2999534:
push { r3 }
mov r0, #2
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
beq true_line14_cd4a08f3
false_line14_1fd6a47c:
mov r0, #0
true_line14_cd4a08f3:
push { r0 }
pop { r0 }
cmp r0, #0
beq else_body_of_if_on_line15_a2537d49
if_body_of_if_on_line15_a2537d49:
mov r0, #1
push { r0 }
b end_if_on_line15_a2537d49
else_body_of_if_on_line15_a2537d49:
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
end_if_on_line15_a2537d49:
end_if_on_line11_d2999534:
end_if_on_line7_826c27f4:
end_if_on_line3_f68ff6ce:

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
 
