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


    def decode_phrase(self, ciphertext, only_wheel1 = False):
        current = 0
        result = ""
        clean_result = ""
        used_c_letters = ""
        for c in ciphertext:
            alberti = self.albertis[current]

            if c == ' ':
                result += ' '
            elif c in alberti.inner.letters:
                pt = alberti.decode(c)
                result += pt
                if not only_wheel1:
                    clean_result += pt
                    used_c_letters += c
                else:
                    if current == 0:
                        clean_result += pt
                        used_c_letters += c
                    else:
                        clean_result += '_'
                        used_c_letters += '_'
            elif c in '12':
                result += '*'
                current = int(c)-1
            elif c in alberti.outer.letters:
                result += '_'
                alberti.rotate_to(c)

        return result, clean_result, used_c_letters

def create_bike(outer, inner, offset):
    inner2=inner[offset:] + inner[:offset]
    front = Alberti(outer, inner)
    back = Alberti(outer, inner2)
    return Bike(front, back)

def part_b_decode(ciphertext):
    outer="ABCDEFGILMNOPQRSTVXZ1234"
    inner="gklnprtvz&xysomqihfdbace"
    offset = 9

    bike = create_bike(outer, inner, offset)

    return bike.decode_phrase(ciphertext)

def part_b():
    ciphertext_nl = "npzpv npmXo i&xbt zxAhg zihzg fhyym Mfdbc kct&e cck2o dlbes kApbh &&kgk oD&x1 kzggd rOxVg yax2& hhbD& xIdlx Iodti 1xyBv tt&Od haoeq hhni2 rtId& sSpff zScp1 chAnp XexbA yym2o f1fpm TkzfX &xEob p2acc aXddk 2cqqr Ixl1s gxPee tPaii Oooe2 btfTo aXzdE d&oz1 vocSa iC&lz 2bver hV&eb gLqry Lyry1 &xIxa kNzf2 o&kkh iGvxo Sakg1 hfLxe eOgk1 ibrTk Xg"
    print(part_b_decode(ciphertext_nl)[1]) 

    ciphertext_fr = "zpzpg npmX& xmtzh ebaxA iy&kp gvhqi pMqzq kveqe cakd2 s&eei looAo k&eei loDto iao1d kOihn ebhnV yh2bt oahiD &xIxl Ipbdf t1qyB &izno xOx2l ItftS lfpbc Sfy1i haoAn pXmtA zvtxp 2yp1g xTbik eXctb &Epg2 gfgXk qkv2h lrIth m1vty PsoPb iOih2 xlTdy x&aXq Ee&yr1 ahcSo dkCxc s2asV feLor Lkf1f lsIdy hlNla kg2yk hGtbS nrp1h fLdbO qbq1a bpThs Xdexm mx2tl fbcXq Akimzyk2ip xAl&D zx1zg OocVd m2hiD iIlIf"
    print(part_b_decode(ciphertext_fr)[1]) 


def calculate_score(text, frequencies):
    text = text.replace('_', '')
    return - l1_distance(normalize_frequencies(Counter(text)), frequencies)

def calculate_digram_score(text, digram_frequencies):
    text = text.replace('_', '')
    digrams = ["".join(pair) for pair in zip(text[:-2], text[1:])]
    return - l1_distance(normalize_frequencies(Counter(digrams)), digram_frequencies)

def normalize_frequencies(frequencies):
    total = sum(frequencies.values())

    result = dict()
    for c in frequencies:
        result[c] = frequencies[c] / total

    return result

def l1_distance(f1, f2):
    square_sum = 0
    for c in f1:
        dist = f1.get(c) - f2.get(c,0) 
        square_sum += dist * dist

    return math.sqrt(square_sum)

def part_c():
    #frequencies = normalize_frequencies(Counter(part_b_decode()[1]))
    frequencies = dutch_frequencies()
    digram_frequencies = dutch_digram_frequencies()

    outer="ABCDEFGILMNOPQRSTVXZ1234"

    ciphertext = "npzpv npmXo i&xbt zxAhg zihzg fhyym Mfdbc kct&e cck2o dlbes kApbh &&kgk oD&x1 kzggd rOxVg yax2& hhbD& xIdlx Iodti 1xyBv tt&Od haoeq hhni2 rtId& sSpff zScp1 chAnp XexbA yym2o f1fpm TkzfX &xEob p2acc aXddk 2cqqr Ixl1s gxPee tPaii Oooe2 btfTo aXzdE d&oz1 vocSa iC&lz 2bver hV&eb gLqry Lyry1 &xIxa kNzf2 o&kkh iGvxo Sakg1 hfLxe eOgk1 ibrTk Xg"
    #ciphertext = "rsslm yaDgh Og&pb hpmas oRhbv ivpAx zmar2 nrNbb tDnbf lO&b1 imrPp eemlm rIkmk &lx2q okqfi zoiEf syi&q Tbldg Rkcmn b1hg& pIzml MsbbA lmya2 frRcA lnTme mriXt y1vmO bgNg& iDsmh dOqgl RdvpA qm2cm yyrxN m&D&t taOqo cs1gy ParkI hg&p2 qokdE r&lTb lhRky vd1&l"
    inner_letters="gklnprtvz&xysomqihfdbace"

    # initialize inner using keyword
    #keyword="xenrygeorge"
    #inner = ""
    #for c in keyword + inner_letters:
    #    if c not in inner:
    #        inner += c

    # random initial inner
    inner_list = list(inner_letters)
    random.shuffle(inner_list)
    inner = "".join(inner_list)

    #for offset in range(len(inner)):
    def scorefn(text):
        return calculate_score(text, frequencies)
        #return calculate_digram_score(text, digram_frequencies)

    print(optimize_initial_inner(ciphertext, outer, inner, 9, scorefn, True))

    #for offset in range(len(inner)):
    #    print(optimize_initial_inner(ciphertext, outer, inner, offset, scorefn, True))

def random_swap(inner):
    i1 = random.randint(0, len(inner)-1)
    i2 = random.randint(0, len(inner)-1)

    l = list(inner)
    l[i1],l[i2] = l[i2],l[i1]

    return "".join(l)

def optimize_initial_inner(ciphertext, outer, inner, offset, scorefn, verbose = False):
    bike = create_bike(outer, inner, offset)
    plain = bike.decode_phrase(ciphertext, False)[1]
    score = -10000000000
    remaining_improvement_attempts = 10000
    while True:
        if remaining_improvement_attempts == 0:
            print("no more improvement attempts")
            break
        new_inner = random_swap(inner)
        new_bike = create_bike(outer, new_inner, offset)
        new_plain = new_bike.decode_phrase(ciphertext, False)[1]
        new_score = scorefn(new_plain)
        #print(score,new_score, new_inner, new_plain)

        if new_score > score:
            print("Improved score:", new_score, "with remaining attempts: ", remaining_improvement_attempts)
            print(new_inner, new_plain)

            inner = new_inner
            bike = new_bike
            plain = new_plain
            score = new_score
            remaining_improvement_attempts = 10000
        else:
            remaining_improvement_attempts -= 1

    print("Best for offset %s:"%(offset), inner, plain)
    return inner, plain


def part_c_interactive():
    #frequencies = normalize_frequencies(Counter(part_b_decode()[1]))
    frequencies = dutch_frequencies()

    outer="ABCDEFGILMNOPQRSTVXZ1234"
    ciphertext = "npzpv npmXo i&xbt zxAhg zihzg fhyym Mfdbc kct&e cck2o dlbes kApbh &&kgk oD&x1 kzggd rOxVg yax2& hhbD& xIdlx Iodti 1xyBv tt&Od haoeq hhni2 rtId& sSpff zScp1 chAnp XexbA yym2o f1fpm TkzfX &xEob p2acc aXddk 2cqqr Ixl1s gxPee tPaii Oooe2 btfTo aXzdE d&oz1 vocSa iC&lz 2bver hV&eb gLqry Lyry1 &xIxa kNzf2 o&kkh iGvxo Sakg1 hfLxe eOgk1 ibrTk Xg"

    #ciphertext = "rsslm yaDgh Og&pb hpmas oRhbv ivpAx zmar2 nrNbb tDnbf lO&b1 imrPp eemlm rIkmk &lx2q okqfi zoiEf syi&q Tbldg Rkcmn b1hg& pIzml MsbbA lmya2 frRcA lnTme mriXt y1vmO bgNg& iDsmh dOqgl RdvpA qm2cm yyrxN m&D&t taOqo cs1gy ParkI hg&p2 qokdE r&lTb lhRky vd1&l"
    inner_letters="gklnprtvz&xysomqihfdbace"

    # initialize inner using keyword
    #keyword="xenrygeorge"
    keyword = "nacvmpfdsxytqrgkelo&ihzb"
    inner = ""
    for c in keyword + inner_letters:
        if c not in inner:
            inner += c

    while True:
        bike = create_bike(outer, inner, 0)
        decoded = bike.decode_phrase(ciphertext, True)
        print(outer, decoded[2])
        print(inner, decoded[1])

        stats = []
        actual_frequencies = normalize_frequencies(Counter(decoded[1].lower()))
        for c in inner:
            p = bike.albertis[0].decode(c)
            stats.append((c,p,actual_frequencies.get(p.lower(), 0)))

        for line in sorted(stats, key = lambda x: -x[2]):
            print(line)

        cmd = input("swap? ").strip()
        if len(cmd) == 2:
            l1, l2 = cmd
            if l1 in inner and l2 in inner:
                print("swapping inner ", l1, l2)
                print(inner)
                inner = inner.replace(l1, '@').replace(l2, l1).replace('@', l2)
                print(inner)
            elif l1 in outer and l2 in outer:
                l1 = inner[outer.find(l1)]
                l2 = inner[outer.find(l2)]
                inner = inner.replace(l1, '@').replace(l2, l1).replace('@', l2)
        else:
            print("nope")


def analyse_c_ciphertext():
    ciphertext = "rsslm yaDgh Og&pb hpmas oRhbv ivpAx zmar2 nrNbb tDnbf lO&b1 imrPp eemlm rIkmk &lx2q okqfi zoiEf syi&q Tbldg Rkcmn b1hg& pIzml MsbbA lmya2 frRcA lnTme mriXt y1vmO bgNg& iDsmh dOqgl RdvpA qm2cm yyrxN m&D&t taOqo cs1gy ParkI hg&p2 qokdE r&lTb lhRky vd1&l"

    current = (1,'A')
    
    for c in ciphertext:
        if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            current = (current[0], c)
        if c in "12":
            current = (c, current[1])
        else:
            print("%s%s"%(current[0], current[1]))
            

def main():
    #part_b()
    #analyse_c_ciphertext()
    part_c_interactive()
    #part_c()

def dutch_frequencies():
    return dict(
      e = 0.1891, n = 0.1003, a = 0.749, t = 0.679, i = 0.650, r = 0.641, o = 0.606, d = 0.593,
      s = 0.373, l = 0.357, g = 0.340, v = 0.285, h = 0.238, k = 0.225, m = 0.221, u = 0.199,
      b = 0.158, p = 0.157, w = 0.152, j = 0.146, z = 0.139, c = 0.124, f = 0.081, x = 0.0040,
      y = 0.0035, q = 0.0009,)


def dutch_digram_frequencies():
  return dict(
      AA = 0.0166, AL = 0.0095, AN = 0.0205, AR = 0.0117, AT = 0.0089, BE = 0.0080, CX = 0.0118, DA = 0.0087, DE = 0.0328, EE = 0.0209,
      EL = 0.0147, EN = 0.0608, ER = 0.0297, ET = 0.0203, GE = 0.0196, IE = 0.0139, II = 0.0169, IN = 0.0146, LE = 0.0104, ME = 0.0096,
      ND = 0.0103, NG = 0.0078, OE = 0.0098, ON = 0.0082, OO = 0.0106, OR = 0.0093, RE = 0.0093, ST = 0.0105, TE = 0.0193, VA = 0.0156,
      VE = 0.0101, XE = 0.0232, ZE = 0.0077,
  )

if __name__=="__main__":
    main()
