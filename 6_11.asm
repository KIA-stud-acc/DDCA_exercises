#s0 - i, t1 - array1, t2 - array2
    addi s0, zero, 0      #инициализация i нулём
    addi t0, zero, 100    #временная переменная для проверки условия цикла
FOR:                      #метка цикла
    bge   s0, t0, DONEFOR #проверка условия цикла
    slli  t5, s0, 2
    add   t3, t2, t5      #временная переменная для хранения адреса array2[i]
    lw    t4, 0(t3)       #считывание значения array2[i] из памяти во временную переменную
    add   t3, t1, t5      #временная переменная для хранения адреса array1[i]
    sw    t4, 0(t3)       #сохранение значения временной переменной в памяти по адресу array1[i]
    addi  s0, s0, 1       #инкремент i
    j     FOR             #переход к началу цикла
DONEFOR:                  #метка конца цикла