from pyparsing import Word, alphas, delimitedList, Literal

prod = Word( "ABCDEFGHIJKLMNOPQRSTUVWXYZ" ) + "->" + delimitedList(Word( alphas ), '|')             
p1_list =["S -> AA | AS | b",
     "A -> SA | AS | a"]

class grammar:
  def __init__(self):
    self.V = []
    self.T = []
    self.P = []
  def load(self,p):  
    self.P.extend(p)
    self.parse()
  def parse(self):
    for p in self.P:
      self.add_variable(p[0])         
      for rh in list(p[1]):
        if rh.isupper():
          self.add_variable(rh)
        else:
          self.add_terminal(rh)
  def add_variable(self, v):  
    try:
      i = self.V.index(v)
    except ValueError:
      self.V.append(v)

  def add_terminal(self, t):  
    try:
      i = self.T.index(t)
    except ValueError:
      self.T.append(t)
            
  def print(self):
    print("P:",self.P)
    print("V:",self.V)
    print("T:",self.T)
    
  def printT(self):
    return self.T
  def printP(self):
    return self.P
  def printV(self):
    return self.V

class production:
  def __init__(self,prod_tokens):
    self.prod_tokens = prod_tokens
    self.LHS = None
    self.RHS = None
    self.production_list = []
  def parse_rhs(self,rhs):
    for i in rhs:
      self.production_list.append((self.LHS,i))
  def parse(self):
    if self.check(self.prod_tokens):       
      self.LHS = self.prod_tokens.pop(0)
      self.prod_tokens.pop(0)
      self.RHS = self.prod_tokens
      self.parse_rhs(self.RHS)
  def check(self,p):
      if len(p) > 2:
          if len(p[0]) == 1:
              if p[1] == '->':
                  return True
      return False
  def print(self):
    for p in self.production_list:
      print("LHS",p[0],"->",p[1])
  def get(self):
    return self.production_list

productions = []

for p in p1_list:
  productions.append(production(prod.parseString(p)))

G = grammar()

for p in productions:
  p.parse()
  G.load(p.get())

G.print()

class algoritmo:
  def Inicio(self):
    sair = False
    while not sair:
      resultado = self.Leitura()
      if resultado == "sair":
        sair = True
        print("saindo")

  def Leitura(self):
    palavra = input("digite uma palavra ou 'sair' para finalizar o programa\n")

    if palavra == "sair":
      return "sair"
      
    self.VerificaPalavra(palavra)

  def VerificaPalavra(self,palavra):
    for letra in palavra:
      if not G.printT().__contains__(letra):
        erro = "A letra " + letra + " não contem no alfabeto"
        return print(erro)  

    self.ExecutaAlg(palavra)

  def ExecutaAlg(self,palavra):
    print("executa algoritmo.." + palavra)        
    matrix = [["null" for i in range(len(palavra) + 1)] for i in range(len(palavra) + 1)]
    rows = len(palavra)
    #print(matrix)
    
    #Preenche a legenda da matrix
    for x in range(0, rows):
      matrix[0][x + 1] = palavra[x]

      matrixaux = []
    
    #print(matrix)

    #Preenchendo a primeira
    for r in range(0, rows):
      for p in G.P:
        if p[1] == matrix[0][r + 1]:
          matrixaux.append(p[0])      
          #matrix[rows - 1][r] = p[0]
      matrix[1][r + 1] = matrixaux
      matrixaux = []

    #print(matrix)

    for s in range(2, rows + 1):
      for r in range(1, rows - s + 2):
        for k in range(1, s):
          for x in range(0, len(matrix[k][r])):
            for x1 in range(0, len(matrix[(s-k)][(r+k)])):
              for p in G.P:
                 if str(matrix[k][r][x]) + str(matrix[(s-k)][(r+k)][x1]) == p[1]:
                   matrixaux.append(p[0])
                   #matrix[rows - s][r-1] = p[0]

              if matrix[s][r] == 'null' and len(matrixaux) > 0:
                matrix[s][r] = matrixaux

              if not matrix[s][r] == 'null' and len(matrixaux) >= len(matrix[s][r]):
                matrix[s][r] = matrixaux

              #if len(matrixaux) >= matrix[s][r] and not (matrix[s][r] == 'null'):
              #  matrix[s][r] = matrixaux
              matrixaux = []
      
    #print(matrix)

    if matrix[rows][1].__contains__('S'):
      print("A gramatica aceita essa palavra")
    else:
      print("A gramatica não aceita essa palavra")

A = algoritmo()

A.Inicio()
