import data
from itertools import permutations

periods = [-1, 1 ,4 ,2 ,5 ,6 ,16 ,4 ,11 ,3 ,28 ,8 ,12 ,18 ,8 ,10 ,23 ,20 ,52 ,6]

beroepen = [ l.strip() for l in open('beroepen.txt').readlines() ]

class Digrafid:
  def __init__(self, hgrid, vgrid, numbers, fraction, verbose=False):
      self.hgrid = hgrid
      self.vgrid = vgrid

      self.numbers = numbers
      self.fraction = fraction
      if verbose:
        print("XXX", hgrid, vgrid, numbers, fraction)

  def find_period(self):
      ciphertext = "de koekoek loopt rond in cirkeltjes"
      loop = False
      count = 0
      actual = ciphertext
      while True:
        count+=1
        actual = self.encode(actual)
        if actual[:20]==ciphertext[:20]:
          return count

  def decode(self, ciphertext):
      # doing this every time slows us down by factor +-2
      #period = self.find_period()
      period = periods[self.fraction]
      return self.encode_n(ciphertext, period-1)[:len(ciphertext)]
          

  def encode_n(self, ciphertext, count):
      result = ciphertext
      for i in range(count):
        result = self.encode(result)

      return result

  def encode(self, ciphertext):
      result = ""
      for i in range(0, len(ciphertext), 2 * self.fraction):
          chunk = ciphertext[i:i+2*self.fraction]
          chunk += 'x' * (2*self.fraction-len(chunk))
          cols = []
          nums = []
          rows = []
          for i in range(self.fraction):
            a,b = chunk[i*2:i*2+2]

            a_row, a_col = coords(a, self.hgrid)
            b_row, b_col = coords(b, self.vgrid)
            num = self.numbers[a_row][b_col]


            cols.append(a_col+1)
            nums.append(num)
            rows.append(b_row+1)

          mix = cols + nums + rows

          for i in range(self.fraction):
              a_col, num, b_row = mix[i*3:i*3+3]
              a_row, b_col = coords(num, self.numbers)

              newpair = self.hgrid[a_row][a_col-1] + self.vgrid[b_row-1][b_col]
              result += newpair
      return result
  

def hgrid(word, n = 0):
    alphabet='abcdefghijklmnopqrstuvwxyz'
    
    chars = ""
    for c in word:
      if c not in chars:
        chars += c
    chars += ' '
    for c in alphabet:
      if c not in chars:
        chars += c

    result = [chars[0:9], chars[9:18], chars[18:]]
    return grid_rotate(result, n)

def vgrid(word, n = 0):
    alphabet='abcdefghijklmnopqrstuvwxyz'

    chars = ""
    for c in word:
      if c not in chars:
        chars += c
    chars += ' '
    for c in alphabet:
      if c not in chars:
        chars += c

    result = []
    for i in range(0, 27, 3):
      result.append(chars[i:i+3])

    return grid_rotate(result, n)



def coords(value,grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == value:
                return row, col

    raise Exception("value %s not found in grid %s"%(value,grid))
    


def block_rotate(ciphertext, n = 1):
    if n == 0:
        return ciphertext
    if n > 1:
        return block_rotate(block_rotate(ciphertext, 1), n-1)

    lines = [ciphertext[i:i+9] for i in range(0,81,9)]

    result = ""
    for col in range(0,9):
        for row in range(8, -1, -1):
            result += lines[row][col]

    return result


def grid_rotate(grid, n = 1):
    if n == 0:
        return grid
    if n > 1:
        return grid_rotate(grid_rotate(grid, 1), n - 1)

    h,w = len(grid),len(grid[0])

    result = []
    for col in range(w):
      result.append("")

    for col in range(w):
      for row in range(h-1,-1,-1):
        result[col] += grid[row][col]
      
    return result

def num_rotate(grid, n = 1):
    if n == 0:
        return grid
    if n > 1:
        return num_rotate(num_rotate(grid, 1), n - 1)

    h, w = len(grid), len(grid[0])

    result = []
    for col in range(w):
      result.append([])

    for col in range(w):
      for row in range(h-1,-1,-1):
        result[col].append(grid[row][col])


    return result


def find_periods():
    grid1 = hgrid("bloemkool")
    grid2 = vgrid("komkommertijd")
    numbers = [[1,2,3],[4,5,6],[7,8,9]]

    for f in range(1,20):
        d = Digrafid(grid1, grid2, numbers, f, False)
        print(f, d.find_period())

def solveA():
    grid1 = vgrid("kleermaker", 1)
    grid2 = hgrid("groenteboer", 1)
    print(len(data.TEXT_A))
    ciphertext = block_rotate(data.TEXT_A, 1)

    for fraction in (4,5,8,10,):
        perm = permutations([2,3,4,5,6,7,8,9])
        for p in perm:
            numbers = [[1,p[0],p[1]], [p[2],p[3],p[4]], [p[5],p[6],p[7]]]

            d = Digrafid(grid1, grid2, numbers, fraction, False)

            print(fraction,  numbers, d.decode(ciphertext))

def solveB():
    grid1 = hgrid("schoenmaker", 0)
    grid2 = vgrid(data.VKEY_B, 0)
    numbers = num_rotate(data.NUMBERS_2, 0)
    ciphertext = block_rotate(data.TEXT_B, 0)

    for fraction in range(10, 11):
        d = Digrafid(grid1, grid2, numbers, fraction, False)
        print("schoenmaker", fraction, d.decode(ciphertext))

def solveC():
    grid1 = vgrid(data.VKEY_B, 1)
    grid2 = hgrid(data.HKEY_C, 1)
    numbers = num_rotate(data.NUMBERS_2, 1)
    ciphertext = block_rotate(data.TEXT_C, 1)

    d = Digrafid(grid1, grid2, numbers, 5)
    print(d.decode(ciphertext))

def solveD():
    d = Digrafid(hgrid(data.HKEY_D), vgrid(data.VKEY_C), data.NUMBERS_3, 4)
    print(d.decode(data.TEXT_D))

def solveF():
    grid1 = vgrid(data.VKEY_E, 3)
    numbers = num_rotate(data.NUMBERS_5, 3)
    ciphertext = block_rotate(data.TEXT_F, 3)

    print("fff", ciphertext)

    for beroep in beroepen[5:]:
        for fraction in range(1, 20):
            grid2 = hgrid(beroep, 3)
            d = Digrafid(grid1, grid2, numbers, fraction, True)
            print(beroep, fraction, d.decode(ciphertext))

def solveG():
    grid1 = hgrid(data.HKEY_G, 2)
    grid2 = vgrid(data.VKEY_E, 2)
    numbers = num_rotate(data.NUMBERS_5, 2)
    ciphertext = block_rotate(data.TEXT_G, 2)

    d = Digrafid(grid1, grid2, numbers, 8)
    print(d.decode(ciphertext))

def solveH():
    grid1 = vgrid("sudoku", 3)
    grid2 = hgrid("coudenbergh", 3)
    numbers = num_rotate(data.NUMBERS_6, 3)
    ciphertext = block_rotate(data.TEXT_H, 3)

    d = Digrafid(grid1, grid2, numbers, 10)
    print(d.decode(ciphertext))

def try_all_fractions(grid1, grid2, numbers, ciphertext):
    for f in range(1,40):
        d = Digrafid(grid1, grid2, numbers, f, False)
        print(f, d.decode(ciphertext))

def main():
    #find_periods()

    # Rechtsboven (done)
    #solveD()
    #solveC()
    #solveG()
    #solveH()
    
    # Te proberen met 'schoenmaker' als onbekende sleutel?
    #solveB()
    #solveA()
    solveF()

if __name__=="__main__":
    main()
