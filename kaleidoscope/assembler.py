import plyplus;

regNames = {
  'x0': 0, 
  'zero': 0,
  'x1': 1,
  'ra': 1,
  'x2': 2
}

class HVisitor(plyplus.STransformer):
  def regname(self, expr):
    val = expr.tail[0]
    regNum = regNames[val]
    regBin = format(int(regNum),'05b')
    print(regBin, end='-')
  
  def instr(self, expr):
    inst =  expr.tail[0]
    f3 = "!!!!!"
    f7="!!!!!"
    print(inst)
    if (inst == "add"):
      f3 = '000'
      f7 = '0000000'
    
    print('0110011-', end = "")
    print(f3+"-", end = "")
    print(f7+"-", end = "")
    
  def extinst(self, expr):
    print(expr)
    
  def imm(self, expr):
    val = expr.tail[0]
    print("sextend(" + val +")", end='')

  def inst(self, expr):
    print(expr.tail[0], end="\n")

with open("riscv.g") as grm:
  parser = plyplus.Grammar(grm)
  t = parser.parse('''
               add zero, x0, ra
               addi x0, x2, +100
               lw x0, 100(x0)
               mv x2, x1
               ''')
  t.to_png_with_pydot(r"tree.png")
  
  v = HVisitor()
  v.transform(t)