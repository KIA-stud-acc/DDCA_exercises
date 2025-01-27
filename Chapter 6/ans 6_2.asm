  addi a0, zero, 0x400
  addi a1, zero, 9
  slli t0, a1, 2
  add  a2, a0, t0
initArray:
  addi t0, zero, -2
  sw   t0, 0(a0)
  addi t0, zero, 3
  sw   t0, 4(a0)
  addi t0, zero, -1
  sw   t0, 8(a0)
  addi t0, zero, 5
  sw   t0, 12(a0)
  addi t0, zero, -10
  sw   t0, 16(a0)
  addi t0, zero, -2
  sw   t0, 20(a0)
  addi t0, zero, 5
  sw   t0, 24(a0)
  addi t0, zero, -1
  sw   t0, 28(a0)
  addi t0, zero, 15
  sw   t0, 32(a0)

maxSumSubArray:
  addi t0, zero, 0      #int start = 0;
  addi t1, zero, 0      #int end   = 0;
  addi t2, zero, 0      #int start_frame = 0;
  lw   t3, 0(a0)        #int max = a[0];
  addi t4, t3, 0        #int tmp = a[0];

  addi t5, zero, 1      #int i = 1;
for1:
  bge  t5, a1, doneFor1  #i<n;
  slli a7, t5, 2
  add  a7, a7, a0
  lw   a7, 0(a7)        #a[i]
  bge  zero, t4, else1  #if (tmp>0)
  add  t4, t4, a7       #tmp+a[i]
  j    doneIf1
else1:                  #else
  addi t4, a7, 0        #tmp = a[i];
  addi t2, t5, 0        #start_frame = i;

doneIf1:
  bge  t3, t4, doneIf2  #if (tmp>max)
  addi t3, t4, 0        #max = tmp;
  addi t0, t2, 0        #start = start_frame;
  addi t1, t5, 0        #end = i;

doneIf2:
  addi t5, t5, 1        #i++
  j    for1
doneFor1:
  slli t6, t0, 2
  sub  a2, a2, t6
for2:
  blt  t1, t0, doneFor2
  slli t6, t0, 2
  add  t4, t6, a0
  lw   t5, 0(t4)        #a[start]
  add  t4, t6, a2
  sw   t5, 0(t4)
  addi t0, t0, 1        #start++
  j    for2
doneFor2:
* ret





