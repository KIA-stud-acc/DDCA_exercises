    bge a1, a0, L1  #проверка условия h>=g
    addi a0, a0, 1  #инкремент g
    j DONE          #переход к концу условия
L1:                 #метка для "Если"
    addi a1, a1, -1 #декремент h
DONE:               #метка конца условия