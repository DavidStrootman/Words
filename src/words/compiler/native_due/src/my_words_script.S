.cpu cortex-m0
.align 2
.text

.global setup, loop

setup: 
bl serial_begin
mov r0, #2
mov r1, #1
bl a_unittest 

mov r0, #14
push { r0 }
bl loopy
pop { r0 }
bl print_num
push { r0 }

@ Start of function loopy at line 0
b loopy_end 
loopy:
mov r5, lr
mov r1, r3
pop { r3 }
push { r5 }
push { r1 }

@ Function body:
mov r0, #0
push { r0 }
while_predicate_on_line3_dd58d6ef:
pop { r0 }
push { r0 }
push { r0 }
mov r0, #10
push { r0 }
pop { r1, r2 }
mov r0, #1
cmp r2, r1
blt true_line4_54e782b9
false_line4_a1369138:
mov r0, #0
true_line4_54e782b9:
push { r0 }
pop { r0 }
cmp r0, #0
beq end_while_on_line3_dd58d6ef
while_body_on_line3_dd58d6ef:
mov r0, #1
push { r0 }
pop { r0, r1 }
add r0, r1, r0
push { r0 }
b while_predicate_on_line3_dd58d6ef
end_while_on_line3_dd58d6ef:

@ Function end cleanup:
@ return value, assuming function solves:
pop { r6 }
pop { r3 }
@ link register:
pop { r7 }
push { r6 }
mov pc, r7
loopy_end:
@ End of function loopy at line 0

loop: 
b loop
 
