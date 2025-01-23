import numpy as np
import warnings
import argparse

warnings.filterwarnings("ignore", r'overflow encountered in scalar add', category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
"""
TODO:
-Hz simulation
-условные остановки
-внеочередное исполнение комманд
-memory simulation
-more instructions
-more flags in manual mode (such as num formats, reg name formats, memory slice)
-possibly here will be marks of every stack alloc
-possibly rewrite all instructions as functions for more convinient pseudo-instractions
-ctrl+x
"""

def max_prefix_number(string:str, default_value:int)->int:
  ret = ""
  for i in string:
    if i.isdigit():
      ret+=i
    else:
      break
  if ret:
    return int(ret)
  return default_value

def sign_ext(num, const_len = 12):
  if num//(2**(const_len-1))==1:
    return num + np.uint32(-2**const_len)
  else:
    return num
  
def num_finder(str_num:str, const_len:int = 12)->int:
  try:
    ret = np.uint32(int(str_num, 10))
  except ValueError:
    try:
      ret = np.uint32(int(str_num, 2))
    except ValueError:
      try:
        ret = np.uint32(int(str_num, 8))
      except ValueError:
        try:
          ret = np.uint32(int(str_num, 16))
        except ValueError:
          raise ValueError("incorrect number format")
  return np.uint32(ret%(2**const_len))

def rv_simulator(code_file: str, start_address: int = 0, sp: int = 4294967292, mode: str = "default") -> None: 
  '''
  code_file:      path to the assembler code file
  start_address:  address of the first instuction in the assembler program
  sp:             address of the top of the stack
  mode:           
  "default" - after each operation both stack and registers will be printed automatically
  "manual"  - each operation only after input (o, s, r and combinations) 
  "file"    - as default, but output in file "report.txt"
  "debug"   - auto, dont ptinting state of stack and registers, stop after mark "*" in the beginning of the string, after waits for manual directions
  ""
  '''
  registers = [np.uint32(0)]*32
  registers[14] = np.uint32(int("0xFFFFFFFF",16))     #for testing purposes
  PC = [start_address]
  registers[2] = sp
  stack = []
  simbol_table = dict()
  debug_marks = dict()
  code = parse_assembler_and_find_all_marks(code_file, start_address, simbol_table, debug_marks)
  if mode == "debug":  
    flags = 'o'
    ops = -1
  elif mode == "default" or mode == "file":
    flags = 'ors'
    ops = -1
  else:
    flags = ''
    ops = 0
  if mode == "file":
    file = open("report.txt", "w")
  else:
    file = None
  while (PC[0]-start_address)/4 < len(code):
    if mode == "debug" and debug_marks.get(PC[0]):
      ops = 0
    instruction = code[(PC[0]-start_address)>>2]
    
    if (mode == "manual" or mode == "debug") and ops == 0:
      flags = input(">>>")
      if 'o' in flags:
        if flags[flags.index('o')+1:flags.index('o')+2] == '+':
          ops = -1
        else:
          ops = max_prefix_number(flags[flags.index('o')+1:], 1)
        
    if 'o' in flags:
      print_instruction(PC[0], instruction, file, simbol_table)
      if (res := do_some_operation(instruction, registers, stack, simbol_table, PC, sp)) == True:
        if ((sp - registers[2]) >> 2) - len(stack) > 0:
          for i in range((((sp - registers[2]) >> 2) - len(stack))):
            stack = stack + [[None, None]]
        else:
          stack = stack[:((sp - registers[2]) >> 2)]
      elif res == "stop":
        break
      else:
          raise ValueError("there is not such instruction")
      ops-=1
      
    if 'r' in flags:
        print_registers(registers, max_prefix_number(flags[flags.index('r')+1:], 8), file)

    if 's' in flags:  
      print_stack(stack, sp, file)
    print("-"*50, '\n', file = file)
  print('!'*20,'\n',"Program is ended\n",'!'*20, sep='',file=file)
  try:
    file.close()
  except AttributeError:
    pass

name_of_registers = {"zero":0,  "x0":  0,
                       "ra":  1,  "x1":  1,
                       "sp":  2,  "x2":  2,
                       "gp":  3,  "x3":  3,
                       "tp":  4,  "x4":  4,
                       "t0":  5,  "x5":  5,
                       "t1":  6,  "x6":  6,
                       "t2":  7,  "x7":  7,
                       "s0":  8,  "x8":  8,  "fp": 8,
                       "s1":  9,  "x9":  9,
                       "a0":  10, "x10": 10,
                       "a1":  11, "x11": 11,
                       "a2":  12, "x12": 12,
                       "a3":  13, "x13": 13,
                       "a4":  14, "x14": 14,
                       "a5":  15, "x15": 15,
                       "a6":  16, "x16": 16,
                       "a7":  17, "x17": 17,
                       "s2":  18, "x18": 18,
                       "s3":  19, "x19": 19,
                       "s4":  20, "x20": 20,
                       "s5":  21, "x21": 21,
                       "s6":  22, "x22": 22,
                       "s7":  23, "x23": 23,
                       "s8":  24, "x24": 24,
                       "s9":  25, "x25": 25,
                       "s10": 26, "x26": 26,
                       "s11": 27, "x27": 27,
                       "t3":  28, "x28": 28,
                       "t4":  29, "x29": 29,
                       "t5":  30, "x30": 30,
                       "t6":  31, "x31": 31
                      }

def do_some_operation(instruction: str, registers: list, stack: list, simbol_table: dict, pc, start_pos_stack) -> bool|str:
  
  operation = instruction.split(" ", 1)[0]
  try:
    operands = [i.strip() for i in instruction.split(' ', 1)[1].split(',')]
  except IndexError:
    operands = None

  match operation:
    case "addi":
      registers[name_of_registers[operands[0]]] = np.uint32(registers[name_of_registers[operands[1]]] + sign_ext(num_finder(operands[2])))
    case "add":
      registers[name_of_registers[operands[0]]] = registers[name_of_registers[operands[1]]] + registers[name_of_registers[operands[2]]]
    case "jal":
      if len(operands) == 1:
        registers[name_of_registers["ra"]] = pc[0] + 4 
        pc[0] = simbol_table[operands[0]]-4 #мне было делать адресацию относительно счётчика комманд
      else:
        registers[name_of_registers[operands[0]]] = pc[0] + 4
        pc[0] = simbol_table[operands[1]]-4
    case "j":
      registers[name_of_registers["x0"]] = pc[0] + 4 #я понимаю, что это необязательно прописывать, но почему бы и нет?
      pc[0] = simbol_table[operands[0]]-4
    case "sw": #здесь будет только урезанная версия, пригодная только для работы со стеком
      op_reg = operands[1].split('(')[1][:-1]
      op_imm = operands[1].split('(')[0]
      stack[((start_pos_stack - (num_finder(op_imm,16) + registers[name_of_registers[op_reg]]))>>2)-1][0] = operands[0]
      stack[((start_pos_stack - (num_finder(op_imm,16) + registers[name_of_registers[op_reg]]))>>2)-1][1] = registers[name_of_registers[operands[0]]]
    case "lw": #аналогично sw
      op_reg = operands[1].split('(')[1][:-1]
      op_imm = operands[1].split('(')[0]
      registers[name_of_registers[operands[0]]] = stack[((start_pos_stack - (num_finder(op_imm,16) + registers[name_of_registers[op_reg]]))>>2)-1][1]
    case "jalr":
      if len(operands) == 1:
        registers[name_of_registers["ra"]] = pc[0] + 4 
        pc[0] = registers[name_of_registers[operands[0]]]-4
      else:
        registers[name_of_registers[operands[0]]] = pc[0] + 4
        pc[0] = registers[name_of_registers[operands[1]]] + num_finder(operands[2],16)-4
    case "jr":
      registers[name_of_registers["zero"]] = pc[0] + 4 
      pc[0] = registers[name_of_registers[operands[0]]]-4
    case "bne":
      if (registers[name_of_registers[operands[0]]] != registers[name_of_registers[operands[1]]]):
        pc[0] = simbol_table[operands[2]]-4
    case "nop":
      pass
    case "ret":
      return "stop"
    case _: 
      return False
    
  registers[0] = 0
  pc[0] += 4
  return True

def parse_assembler_and_find_all_marks(code_file: str, start_address: int, simbol_table: dict, debug_marks:dict) -> None:
  tmp_pc = start_address
  code = []
  with open(code_file, "r") as asm_file:
    while instruction := asm_file.readline():
      if instruction.split('#', 1)[0].strip():
        if ':' in instruction.split('#', 1)[0].strip():
          simbol_table[instruction[:instruction.index(':')]] = tmp_pc
        if instruction.split('#', 1)[0].strip()[-1] != ':':
          if instruction[:-1].split('#', 1)[0].split(':', 1)[-1].strip()[0] == '*':
            debug_marks[tmp_pc] = True
            code.append(instruction[:-1].split('#', 1)[0].split(':', 1)[-1][1:].strip())
          else:
            code.append(instruction[:-1].split('#', 1)[0].split(':', 1)[-1].strip())
          tmp_pc += 4
  return code

def print_stack(stack, start_address, file):
  print("stack:", file=file)
  for i in range(len(stack)):
    print('+--------------+', file=file)
    try:
      print('|'+f"{f'{stack[i][0]} ' f'{hex(stack[i][1])}':<14}"+f"|{hex(start_address-i*4)}", file=file)
    except TypeError:
      print('|'+f'{"-----":^14}'+f"|{hex(start_address-i*4)}", file=file)
  if len(stack)>0:
    print('+--------------+\n', file=file)
  else:
    print("stack is empty\n", file=file)

def print_registers(regs, col, file):
  if col > 32:
    col = 32
  if col < 1:
    col = 1
  print("registers:", file=file)
  for i in range(0, len(regs), col):
    print('+--------------'*col, '+', sep = '', file=file)
    for u in range(col):
      if i+u<32:
        print('|'+f"{'x'f'{i+u}':<4}" + f'{hex(np.uint32(regs[i+u])):<10}', end = '', file=file)
      else:
        print('|'+f"{'':14}", end = '', file=file)
    print('|', file=file)
  print('+--------------'*col,"+\n", sep = '', file=file)

def print_instruction(address, instruction, file, simbol_table:dict):
  print(f"{hex(address)}\t", end = ' ', file=file)
  operation = instruction.split(" ", 1)[0]
  try:
    operands = [i.strip() for i in instruction.split(' ', 1)[1].split(',')]
  except IndexError:
    operands = []
  print(operation, ", ".join(operands), file=file, end=' ')
  if operands:
    tmp = simbol_table.get(operands[-1], -1)
    if tmp != -1:
      print(f"({hex(tmp)})", file=file, end = '')
  print('\n', file=file)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("file", nargs=1)
  parser.add_argument("-m", "--mode", default="default")
  parser.add_argument("-s", "--start_address", default=0, type=int)
  args = parser.parse_args()

  rv_simulator(args.file[0], args.start_address, mode = args.mode)