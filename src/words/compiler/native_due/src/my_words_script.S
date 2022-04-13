.cpu cortex-m0
.align 2
.text

.global setup, loop

setup: 
bl serial_begin
mov r0, #3
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
pop { r4, r5 }
push { lr }
bl blink_led
push { r4 }
mov r0, #0
push { r0 }
pop { r1, r2 }
mov r3, #1
cmp r2, r1
beq true_line2_d5debf32
false_line2_5358fdf6:
mov r3, #0
true_line2_d5debf32:
push { r3 }
pop { r3 }
cmp r3, #0
beq else_body_of_if_on_line3_2109a18b
if_body_of_if_on_line3_2109a18b:
push { r5 }
mov r0, #1
push { r0 }
pop { r0, r1 }
add r0, r0, r1
push { r0 }
b end_if_on_line3_2109a18b
else_body_of_if_on_line3_2109a18b:
push { r5 }
mov r0, #0
push { r0 }
pop { r1, r2 }
mov r3, #1
cmp r2, r1
beq true_line6_f979a256
false_line6_2d595c15:
mov r3, #0
true_line6_f979a256:
push { r3 }
pop { r3 }
cmp r3, #0
beq else_body_of_if_on_line7_7d9f457d
if_body_of_if_on_line7_7d9f457d:
mov r0, #1
push { r0 }
push { r4 }
mov r0, #1
push { r0 }
pop { r0, r1 }
sub r0, r0, r1
push { r0 }
bl ACKERMANN
b end_if_on_line7_7d9f457d
else_body_of_if_on_line7_7d9f457d:
push { r5 }
mov r0, #1
push { r0 }
pop { r0, r1 }
sub r0, r0, r1
push { r0 }
push { r4 }
bl ACKERMANN
push { r4 }
mov r0, #1
push { r0 }
pop { r0, r1 }
sub r0, r0, r1
push { r0 }
bl ACKERMANN
end_if_on_line7_7d9f457d:
end_if_on_line3_2109a18b:
@ Flip output and lr.
pop { r6 }
pop { r7 }
push { r6 }
mov pc, r7
ACKERMANN_end:
@ End of function ACKERMANN at line 0
loop: 
b loop
 
