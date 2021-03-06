
def create_keygrid(keyword, size, alphabet):
    line = ""
    for c in keyword + alphabet:
      if c not in line:
        line += c

    result = []
    for i in range(0, len(alphabet), size):
        result.append(line[i:i+size])

    return result

def playfair_encode(keygrid, plaintext):
    return playfair(keygrid, plaintext, True)

def playfair_decode(keygrid, ciphertext):
    return playfair(keygrid, ciphertext, False)

def playfair(keygrid, text, encode=True):
    result = ""
    if len(text)%2==1:
      text += "X"
    text = text.upper()

    for idx in range(0, len(text), 2):
      a=text[idx]
      b=text[idx+1]

      a_coords = coords(keygrid, a)
      b_coords = coords(keygrid, b)

      pair_swapped = pair_encode(keygrid, a_coords, b_coords) if encode else pair_decode(keygrid, a_coords, b_coords)
      result += pair_swapped

    return result

def pair_encode(grid, a, b):
    arow, acol = a
    brow, bcol = b
    
    if arow == brow:
        w = len(grid[arow])
        return grid[arow][(acol+1)%w] + grid[arow][(bcol+1)%w]

    if acol == bcol:
        h = len(grid)
        return grid[(arow+1)%h][acol] + grid[(brow+1)%h][bcol]

    return grid[arow][bcol] + grid[brow][acol]


def pair_decode(grid, a, b):
    arow, acol = a
    brow, bcol = b
    
    if arow == brow:
        w = len(grid[arow])
        return grid[arow][(acol+w-1)%w] + grid[arow][(bcol+w-1)%w]

    if acol == bcol:
        h = len(grid)
        return grid[(arow+h-1)%h][acol] + grid[(brow+h-1)%h][bcol]

    return grid[arow][bcol] + grid[brow][acol]

def coords(keygrid, c):
    for row in range(len(keygrid)):
        for col in range(len(keygrid)):
            if keygrid[row][col] == c:
                return (row,col)

    raise Exception("char %s not found in keygrid", c)


def decode(phrase, line):
    # TODO alphabet variations: no J, space at start, after z or after numbers, 0 at end of numbers
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    grid = create_keygrid(phrase, 6, alphabet)
    return(playfair_decode(grid, line))

lines_NL = [
    "RZBWDM",
    "PTI9P1CM",
    "2P2W6A1Q",
    "WKWBK1SP",
    "SX1LKG1K",
    #"SX1KKG1W",
]
phrase_NL = "OLYMPISCHESPELEN1920"

lines_FR = [
    "WUETRJ",
    "ZUM4LXDX",
    "OUZYM9KS",
    "UOURRMDK",
    "PGUG4MVL",
    "8SL9JUXU"
]
phrase_FR = "JEUXOLYMPIQUES1920"

def decode_nl():
    ciphertexts=["RZBWDM",
        "2P2W6A1Q",
        "PTI9P1CM",
        "WKWBK1SP",
        "PTI9P1CM",
        "SX1LKG1K"]

    print("")
    print("NEDERLANDS")
    for c in ciphertexts:
        print(decode(phrase_NL, c).replace('X',''))


def main():
    decode_nl()

if __name__=="__main__":
    main()

