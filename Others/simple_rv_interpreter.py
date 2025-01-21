
def rv_interpreter(code_file: str, start_address: int = 0, sp: int = 4294967292, mode: str = "default") -> None: 
  '''
  code_file:      path to the assembler code file
  start_address:  address of the first instuction in the assembler program
  sp:             address of the top of the stack
  mode:           
  "default" - after each operation both stack and registers will be printed automatically
  "manual"  - each operation only after input (o, s, r and combinations) 
  ""
  ""
  '''
  registers = [0]*32
  PC = [start_address]
  registers[2] = sp
  stack = []
  simbol_table = dict()
  code = parse_assembler_and_find_all_marks(code_file, start_address, simbol_table)

  while (PC[0]-start_address)/4 < len(code):
    instruction = code[(PC[0]-start_address)>>2]
    print_instruction(PC[0], instruction)
    if (res := do_some_operation(instruction, registers, stack, simbol_table, PC, sp)) == True:
      if ((sp - registers[2]) >> 2) - len(stack) > 0:
        stack = stack + (((sp - registers[2]) >> 2) - len(stack))*[None]
      else:
        stack = stack[:((sp - registers[2]) >> 2)]
      print(registers, stack, sep = '\n')
    elif res == "stop":
      break
    else:
      raise ValueError("there is not such instruction")
  print("Program is ended")



def do_some_operation(instruction: str, registers: list, stack: list, simbol_table: dict, pc, start_pos_stack) -> bool|str:
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
  operation = instruction.split(" ", 1)[0]
  try:
    operands = [i.strip() for i in instruction.split(' ', 1)[1].split(',')]
  except IndexError:
    operands = None
  match operation:
    case "addi":
      registers[name_of_registers[operands[0]]] = registers[name_of_registers[operands[1]]] + int(operands[2])
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
      stack[((start_pos_stack - (int(op_imm,16) + registers[name_of_registers[op_reg]]))>>2)-1] = registers[name_of_registers[operands[0]]]
    case "lw": #аналогично sw
      op_reg = operands[1].split('(')[1][:-1]
      op_imm = operands[1].split('(')[0]
      registers[name_of_registers[operands[0]]] = stack[((start_pos_stack - (int(op_imm,16) + registers[name_of_registers[op_reg]]))>>2)-1]
    case "jalr":
      if len(operands) == 1:
        registers[name_of_registers["ra"]] = pc[0] + 4 
        pc[0] = registers[name_of_registers[operands[0]]]-4
      else:
        registers[name_of_registers[operands[0]]] = pc[0] + 4
        pc[0] = registers[name_of_registers[operands[1]]] + int(operands[2],16)-4
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


def  parse_assembler_and_find_all_marks(code_file: str, start_address: int, simbol_table: dict) -> None:
  tmp_pc = start_address
  code = []
  with open(code_file, "r") as asm_file:
    while instruction := asm_file.readline():
      if instruction.split('#', 1)[0].strip():
        code.append(instruction[:-1].split('#', 1)[0].split(':', 1)[-1].strip())
        #print(f"{hex(tmp_pc)}\t{instruction[:-1].split('#', 1)[0]}") #print assembler code with addresses of the instructions in ram
        if ':' in instruction:
          simbol_table[instruction[:instruction.index(':')]] = tmp_pc
        tmp_pc += 4
  return code

def print_stack():
  pass

def print_registers():
  pass

def print_instruction(address, instruction):
  print(f"{hex(address)}\t", end = ' ')
  operation = instruction.split(" ", 1)[0]
  try:
    operands = [i.strip() for i in instruction.split(' ', 1)[1].split(',')]
  except IndexError:
    operands = []
  print(operation, ", ".join(operands))

rv_interpreter("6_21.asm", 32768)