  addi a0, zero, 6
setArray:
  addi sp, sp, -64    #выделение памяти в стеке
  sw   ra, 60(sp)
  sw   s4, 56(sp)     #сохранение оберегаемого регистра
  addi s4, zero, 0    #инициализация переменной i нулём
  addi t1, zero, 10   #временная переменная для проверки условия цикла
forSetArray:
  bge  s4, t1, doneSetArray #условие цикла
  sw   t1, 52(sp)     #сохранение необерегаемых регистров перед вызовом функции
  sw   a0, 48(sp)
  addi a1, s4, 0      #задание второго аргумента функции(первый уже есть)
  call compare        #вызов функции
  slli t1, s4, 2      #вычисление адреса элемента массива
  add  t1, t1, sp     
  sw   a0, 0(t1)      #сохранение вычиленного функцией знаения в массив
  addi s4, s4, 1      #i++
  lw   t1, 52(sp)     #восстановление необерегаемых регистров после вызова функции
  lw   a0, 48(sp)
  j    forSetArray    #переход к началу цикла
doneSetArray:
  lw   s4, 56(sp)     #восстановление сберегаемых регистров
  lw   ra, 60(sp)
  addi sp, sp, 64     #освобождение стека
  ret

compare:
  addi sp, sp, -16    #выделение памяти в стеке
  sw   ra, 12(sp)     #сохранение оберегаемого регистра
  call subf           #вызов функции
  blt  zero, a0, elseCompare  #проверка условия
  addi a0, zero, 1    #return 1
  j    doneCompare
elseCompare:
  addi a0, zero, 0    #else return 0
doneCompare:
  lw   ra, 12(sp)     #восстановление сберегаемых регистров
  addi sp, sp, 16     #освобождение стека
  jr   ra             #возврат из функции

subf:
  sub  a0, a0, a1     #return a-b
  jr   ra     

