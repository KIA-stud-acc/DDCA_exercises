 # код на языке ассемблера RISC-V
 # f: a0 = a, a1 = b, s4 = j;
test:  
       addi x14, x14, 0xffe
       nop
       addi a0, zero, 5    # a = 5
       addi a1, zero, 3    # b = 3
       jal  f              # вызов f(5, 3)

loop:  ret        # вечный цикл
f:     addi sp, sp, -16    # создать фрейм в стеке
       
       lw  a1, 0xC(sp)  
       lw a1, 0xC(sp) 
       sw   a0, 0xC(sp)    # сохранить a0
       sw   a1, 0x8(sp)    # сохранить a1
       sw   ra, 0x4(sp)    # сохранить ra
*      sw   s4, 0x0(sp)    # сохранить s4
       addi s4, a0, 0      # j = a
       addi a0, a1, 0      # поместить b как аргумент для g()
       jal  g              # вызов g
       lw   t0, 0xC(sp)    # восстановить: a в t0
       add  a0, a0, t0     # a0 = g(b) + a
       add  a0, a0, s4     # a0 = (g(b) + a) + j
       lw   s4, 0x0(sp)    # восстановить регистры
       lw   ra, 0x4(sp)
       addi sp, sp, 16
       jr   ra             # возврат в точку вызова
g:*    addi sp, sp, -8     # создать фрейм в стеке
       sw   ra, 4(sp)      # сохранить регистры
       sw   s4, 0(sp)
       addi s4, zero, 3    # k = 3
       bne  a0, zero, else # если (x != 0), перейти к метке else
       addi a0, zero, 0    # возвращаемое значение 0
       j    done           # очистка и возврат
else:  addi a0, a0, -1     # уменьшить x на 1
       jal  g              # вызов g(x − 1)
       add  a0, s4, a0     # возвращаемое значение k + g(x − 1)
done:  lw   s4, 0(sp)      # восстановить регистры
       lw   ra, 4(sp)
       addi sp, sp, 8
       jr   ra             # возврат в точку вызова