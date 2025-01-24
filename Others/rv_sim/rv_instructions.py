from extras import name_of_registers, sign_ext, num_finder
import numpy as np
import random

def addi(operands: list, registers: list, memory: dict, simbol_table: dict, pc) -> None:
  registers[name_of_registers[operands[0]]] = np.uint32(registers[name_of_registers[operands[1]]] + sign_ext(num_finder(operands[2])))

def add(operands: list, registers: list, memory: dict, simbol_table: dict, pc) -> None:
  registers[name_of_registers[operands[0]]] = registers[name_of_registers[operands[1]]] + registers[name_of_registers[operands[2]]]

def jal(operands: list, registers: list, memory: dict, simbol_table: dict, pc) -> None:
  if len(operands) == 1:
    registers[name_of_registers["ra"]] = pc[0] + 4 
    pc[0] = simbol_table[operands[0]]-4 #мне было делать адресацию относительно счётчика комманд
  else:
    registers[name_of_registers[operands[0]]] = pc[0] + 4
    pc[0] = simbol_table[operands[1]]-4

def j(operands: list, registers: list, memory: dict, simbol_table: dict, pc) -> None:
  registers[name_of_registers["x0"]] = pc[0] + 4 #я понимаю, что это необязательно прописывать, но почему бы и нет?
  pc[0] = simbol_table[operands[0]]-4




def sw(operands: list, registers: list, memory: dict, simbol_table: dict, pc) -> None:
  op_reg = operands[1].split('(')[1][:-1]
  op_imm = operands[1].split('(')[0]
  memory[num_finder(num_finder(op_imm) + registers[name_of_registers[op_reg]], 32)] = ["", 0] #либо создаю, если не было, либо зануляю без эффекта
  memory[num_finder(num_finder(op_imm) + registers[name_of_registers[op_reg]], 32)][0] = operands[0]
  memory[num_finder(num_finder(op_imm) + registers[name_of_registers[op_reg]], 32)][1] = registers[name_of_registers[operands[0]]]




def lw(operands: list, registers: list, memory: dict, simbol_table: dict, pc) -> None:
  op_reg = operands[1].split('(')[1][:-1]
  op_imm = operands[1].split('(')[0]
  if memory.get(num_finder(num_finder(op_imm) + registers[name_of_registers[op_reg]], 32), False):
    pass
  else:
    memory[num_finder(num_finder(op_imm) + registers[name_of_registers[op_reg]], 32)] = ["??", np.uint32(random.randint(0, 4_294_967_295))]
  registers[name_of_registers[operands[0]]] = memory[num_finder(num_finder(op_imm) + registers[name_of_registers[op_reg]], 32)][1]

def jalr(operands: list, registers: list, memory: dict, simbol_table: dict, pc) -> None:
  if len(operands) == 1:
    registers[name_of_registers["ra"]] = pc[0] + 4 
    pc[0] = registers[name_of_registers[operands[0]]]-4
  else:
    registers[name_of_registers[operands[0]]] = pc[0] + 4
    pc[0] = registers[name_of_registers[operands[1]]] + num_finder(operands[2])-4

def jr(operands: list, registers: list, memory: dict, simbol_table: dict, pc) -> None:
  registers[name_of_registers["zero"]] = pc[0] + 4 
  pc[0] = registers[name_of_registers[operands[0]]]-4

def bne(operands: list, registers: list, memory: dict, simbol_table: dict, pc) -> None:
  if (registers[name_of_registers[operands[0]]] != registers[name_of_registers[operands[1]]]):
    pc[0] = simbol_table[operands[2]]-4

def beq(operands: list, registers: list, memory: dict, simbol_table: dict, pc) -> None:
  if (registers[name_of_registers[operands[0]]] == registers[name_of_registers[operands[1]]]):
    pc[0] = simbol_table[operands[2]]-4
  
def blt(operands: list, registers: list, memory: dict, simbol_table: dict, pc) -> None:
  if (registers[name_of_registers[operands[0]]] < registers[name_of_registers[operands[1]]]):
    pc[0] = simbol_table[operands[2]]-4

def bge(operands: list, registers: list, memory: dict, simbol_table: dict, pc) -> None:
  if (registers[name_of_registers[operands[0]]] >= registers[name_of_registers[operands[1]]]):
    pc[0] = simbol_table[operands[2]]-4

def nop(operands: list, registers: list, memory: dict, simbol_table: dict, pc) -> None:
  pass