  addi a0, zero, 2
  addi a1, zero, 4

f:
  addi sp, sp, -16
  sw   ra, 12(sp)
  sw   s4, 8(sp)
  addi s4, a1, 2
  bne  a0, zero, fElse
  addi s4, zero, 10
  j    fCondDone
fElse:
  sw   a0, 4(sp)
  sw   a1, 0(sp)
  addi a0, a0, -1
  addi a1, a1, 1
  call f
  addi t1, a0, 0
  lw   a0, 4(sp)
  lw   a1, 0(sp)
  mul  t2, a0, a0
  add  s4, s4, t2
  add  s4, s4, t1
fCondDone:
  mul  a0, s4, a1
  lw   ra, 12(sp)
  lw   s4, 8(sp)
  addi sp, sp, 16
  jr   ra



