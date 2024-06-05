import plyplus

with open("calc.g") as grm:
  parser = plyplus.Grammar(grm)
  parser.parse("-((1 + (3 * 2)) + (2 + 3) - (5 / -4))")
  # parser.parse("((1 + (3 * 2)) + (2 + 3) - (5 / 4))")
  # parser.parse("4")
  parser.parse("-+4")
