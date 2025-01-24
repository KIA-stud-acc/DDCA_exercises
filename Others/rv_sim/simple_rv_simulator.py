import numpy as np
import warnings
import argparse
import rv_instructions
from extras import max_prefix_number, num_finder
import random 

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
  registers     = [np.uint32(0)]*32
  registers[14] = np.uint32(int("0xFFFFFFFF",16))     #for testing purposes
  PC            = [start_address]
  registers[2]  = sp
  memory        = dict()
  simbol_table  = dict()
  debug_marks   = dict()
  code          = parse_assembler_and_find_all_marks(code_file, start_address, simbol_table, debug_marks)

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
      if (res := do_some_operation(instruction, registers, memory, simbol_table, PC)) == True:
        pass
      elif res == "stop":
        break
      else:
          raise ValueError("there is not such instruction")
      ops-=1
      
    if 'r' in flags:
        print_registers(registers, max_prefix_number(flags[flags.index('r')+1:], 8), file)

    if 's' in flags:  
      print_stack(memory, registers[2], sp, file)
    print("-"*50, '\n', file = file)
  print('!'*20,'\n',"Program is ended\n",'!'*20, sep='',file=file)
  try:
    file.close()
  except AttributeError:
    pass


def do_some_operation(instruction: str, registers: list, memory: dict, simbol_table: dict, pc) -> bool|str:
  
  operation = instruction.split(" ", 1)[0]

  if operation == "ret":
    return "stop"
  
  try:
    operands = [i.strip() for i in instruction.split(' ', 1)[1].split(',')]
  except IndexError:
    operands = None
  try:
    getattr(rv_instructions, operation)(operands, registers, memory, simbol_table, pc)
  except AttributeError:
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




def print_stack(memory, sp, start_address, file):

  print("stack:", file=file)
  for i in range(start_address-4, sp-4, -4):
    print('+--------------+', file=file)

    if memory.get(i, False):
      pass
    else:
      memory[i] = ["??", np.uint32(random.randint(0, 4_294_967_295))]

    print('|'+f"{f'{memory[i][0]} ' f'{hex(memory[i][1])}':<14}"+f"|{hex(i)}", file=file)

  if sp != start_address:
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
  parser.add_argument("-s", "--start_address", default=0, type=str)
  args = parser.parse_args()
  rv_simulator(args.file[0], num_finder(args.start_address, 32), mode = args.mode)