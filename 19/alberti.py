import random
import math
from collections import Counter 

starts = [l.strip().upper() for l in open('valid_starts.txt').readlines()]

class Wheel:
    def __init__(self, letters):
        self.letters = letters

    def rotate(self, letter):
        if letter not in self.letters:
            raise Exception("Letter %s not in wheel %s:", letter, self.letters)

        idx = self.letters.find(letter)
        self.letters = self.letters[idx:] + self.letters[:idx]

class Alberti:
    def __init__(self, outer, inner):
        self.outer = Wheel(outer)
        self.inner = Wheel(inner)

    def decode(self, letter):
        if letter not in self.inner.letters:
            raise Exception("Cannot decode: %s not present in inner wheel %s"%(letter, self.inner.letters))

        idx = self.inner.letters.find(letter)
        result = self.outer.letters[idx]

        return result

    def rotate_to(self, letter):
        self.outer.rotate(letter)

class Bike:
    def __init__(self, front, back):
        self.albertis = [front, back]


    def decode_phrase(self, ciphertext):
        current = 0
        result = ""
        clean_result = ""
        for c in ciphertext:
            alberti = self.albertis[current]

            if c == ' ':
                result += ' '
            elif c in alberti.inner.letters:
                pt = alberti.decode(c)
                result += pt
                clean_result += pt
            elif c in '12':
                result += '*'
                current = int(c)-1
            elif c in alberti.outer.letters:
                result += '_'
                alberti.rotate_to(c)

        return result, clean_result

def create_bike(outer, inner, offset):
    inner2=inner[offset:] + inner[:offset]
    front = Alberti(outer, inner)
    back = Alberti(outer, inner2)
    return Bike(front, back)

def part_b_decode():
    outer="ABCDEFGILMNOPQRSTVXZ1234"
    inner="gklnprtvz&xysomqihfdbace"
    offset = 9

    bike = create_bike(outer, inner, offset)
    ciphertext = "npzpv npmXo i&xbt zxAhg zihzg fhyym Mfdbc kct&e cck2o dlbes kApbh &&kgk oD&x1 kzggd rOxVg yax2& hhbD& xIdlx Iodti 1xyBv tt&Od haoeq hhni2 rtId& sSpff zScp1 chAnp XexbA yym2o f1fpm TkzfX &xEob p2acc aXddk 2cqqr Ixl1s gxPee tPaii Oooe2 btfTo aXzdE d&oz1 vocSa iC&lz 2bver hV&eb gLqry Lyry1 &xIxa kNzf2 o&kkh iGvxo Sakg1 hfLxe eOgk1 ibrTk Xg"

    return bike.decode_phrase(ciphertext)

def part_b():
    print(part_b_decode()[1]) 

def calculate_score(text, frequencies):
    return - l1_distance(frequencies, normalize_frequencies(Counter(text)))

def normalize_frequencies(frequencies):
    total = sum(frequencies.values())

    result = dict()
    for c in frequencies:
        result[c] = frequencies[c] / total

    return result

def l1_distance(f1, f2):
    chars = set(f1.keys()).union(set(f2.keys()))

    square_sum = 0
    for c in chars:
        dist = f1.get(c,0) - f2.get(c,0) 
        square_sum += dist * dist

    return math.sqrt(square_sum)

def part_c():
    #frequencies = normalize_frequencies(Counter(part_b_decode()[1]))
    frequencies = dutch_frequencies()

    outer="ABCDEFGILMNOPQRSTVXZ1234"
    ciphertext = "rsslm yaDgh Og&pb hpmas oRhbv ivpAx zmar2 nrNbb tDnbf lO&b1 imrPp eemlm rIkmk &lx2q okqfi zoiEf syi&q Tbldg Rkcmn b1hg& pIzml MsbbA lmya2 frRcA lnTme mriXt y1vmO bgNg& iDsmh dOqgl RdvpA qm2cm yyrxN m&D&t taOqo cs1gy ParkI hg&p2 qokdE r&lTb lhRky vd1&l"
    inner_letters="gklnprtvz&xysomqihfdbace"

    # initialize inner using keyword
    keyword="xenrygeorge"
    inner = ""
    for c in keyword + inner_letters:
        if c not in inner:
            inner += c

    # random initial inner
    #inner_list = list(inner_letters)
    #random.shuffle(inner_list)
    #inner = "".join(inner_list)

    for offset in range(len(inner)):
        print(optimize_initial_inner(ciphertext, outer, inner, offset, frequencies, True))

def optimize_initial_inner(ciphertext, outer, inner, offset, frequencies, verbose = False):
    #print("initial inner:", inner)
    best_score = -10000000000 
    best = inner
    best_text = 'initial'
    
    for i in range(100_000):
        bike = create_bike(outer, inner, offset)

        plain = bike.decode_phrase(ciphertext)
        score = calculate_score(plain[1], frequencies)
        if score > best_score:
            best_score = score
            best = inner
            best_text = plain[1]
            if verbose:
                if plain[1][:4] in starts:
                    print(i, best, plain[1])
        else:
            i1 = random.randint(0, len(inner)-1)
            i2 = random.randint(0, len(inner)-1)
  
            l = list(inner)
            l[i1],l[i2] = l[i2],l[i1]
            inner = "".join(l)
    return best, best_text


def main():
    #part_b()
    part_c()

def dutch_frequencies():
    return dict(
      e = 0.1891, n = 0.1003, a = 0.749, t = 0.679, i = 0.650, r = 0.641, o = 0.606, d = 0.593,
      s = 0.373, l = 0.357, g = 0.340, v = 0.285, h = 0.238, k = 0.225, m = 0.221, u = 0.199,
      b = 0.158, p = 0.157, w = 0.152, j = 0.146, z = 0.139, c = 0.124, f = 0.081, x = 0.0040,
      y = 0.0035, q = 0.0009,)

if __name__=="__main__":
    main()
