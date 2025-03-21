find42:                   #метка функции
  addi t0, zero, 0        #инициализация i нулём
  addi t1, zero, 42       #инициализация временной переменной для проверки условия
FOR:                      #метка начала цикла
  bge   t0, a1, DONEFOR   #проверка условия цикла
  slli  t2, t0, 2         #умножение номера элемента на 4 для правильной адресации слов
  add   t2, t2, a0        #вычисление адреса array[i]
  lw    t3, 0(t2)         #считывание значения array[i] из памяти во врменную переменную
  bne   t3, t1, L1        #проверка равно ли значение array[i] 42-м
  addi  a0, t0, 0         #если да, то записать в регистр с возвращаемым значением индекс этого элемента
  ret                     #возврат из функции
L1:                       #метка для кода после условия
  addi  t0, t0, 1         #инкремент i
  j     FOR               #переход к началу цикла
DONEFOR:                  #метка конца цикла
  addi a0, zero, -1       #если цикл закончился, а элемент равный 42-м не нашёлся, то записать в регстр с возвращаемым значением -1
  ret                     #возврат из функции