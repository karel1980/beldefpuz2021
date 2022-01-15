import sys

def encode(word):
    word = word.upper()
    alphabet = 'ABCDEFGIKLMNOPQRSTUVXYZ'

    result = ''
    used = ''
    for c in word:
        if c in used:
            result += alphabet[used.find(c)]
        else:
            newchar = alphabet[len(used)]
            used += c
            result += newchar

    return result

wordlist_filename = 'wordlist.txt'

def main():
    words = [ (l.strip(),encode(l.strip())) for l in open(wordlist_filename).readlines() ]

    word = sys.argv[1]
    eword = encode(word)

    for w in words:
        if w[1] == eword:
            print(w[0])
            
if __name__=="__main__":
    main()
