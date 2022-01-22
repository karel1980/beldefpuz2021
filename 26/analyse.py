
from collections import Counter

def read_patterns():
  return [l.strip() for l in open('26.txt').readlines()]


def create_ciphertext(patterns):
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ#'

    idx = 0

    pattern_map = dict()

    for p in patterns:
        if p not in pattern_map:
            pattern_map[p] = ALPHABET[idx]
            idx += 1

    result = ""
    for p in patterns:
        result += pattern_map[p]

    return result

def analyse_ciphertext(ct):
    frequency = Counter(ct)

    digrams = [ "".join(p) for p in zip(ct[:-1],ct[1:]) ]
    digram_frequency = Counter(digrams)

    print("frequency", frequency)
    print("bigram", digram_frequency)

def analyse_patterns(patterns):
    ct = create_ciphertext(patterns)
    print("ciphertext", ct)
    analyse_ciphertext(ct)

def main():
    patterns = read_patterns()
    analyse_patterns(patterns)

    print()
    # same analysis, ignoring the gray region (4 bit letters -> only 16 letters used?)
    patterns = [p[0]+ p[2:] for p in patterns]
    analyse_patterns(patterns)


if __name__=="__main__":
    main()
    #analyse_ciphertext("the quick brown fox jumps over the lazy dog")
