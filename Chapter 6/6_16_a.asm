#a0 - dst, a1 - src, s0 - i
strcpy:
  addi  sp, sp, -16
  sw    s0, 12(sp)

  addi  s0, zero, 0
DO:
  slli  t0, s0, 2
  add   t1, t0, a1
  lw    t2, 0(t1)
  add   t1, t0, a0
  sw    t2, 0(t1)
  addi  s0, s0, 1

  slli  t0, s0, 2
  add   t1, t0, a1
  lw    t2, 0(t1)
  bne   zero, t2, DO

  lw    s0, 12(sp)
  addi  sp, sp, 16
DONE:
