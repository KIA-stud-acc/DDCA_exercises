  beq a0, a1, noGoToFunc
  auipc ra, 0x08000
  jalr  ra, ra, 0
noGoToFunc:
  nop

...
...
...
func:
