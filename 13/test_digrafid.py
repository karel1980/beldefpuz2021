
from nose.tools import assert_equal
from digrafid import Digrafid, block_rotate, hgrid, vgrid, grid_rotate, num_rotate

def test_encode_rechtsboven_rechtsboven():
    d = Digrafid(hgrid("digraf"), vgrid("fractionering"), [[1,2,3],[4,5,6],[7,8,9]], 4)

    ciphertext = "qpdeknerdcntg dwhdgasefexenyagibedeoghd zfuafokuipbdekgm p jjogddklhifrctrsjatgo"
    actual = ciphertext
    for i in range(4):
        actual = d.encode(actual)
        print(actual, i)

    assert_equal(actual, "de andere drie vierkanten zijn gedraaid ze gebruiken ook een andere fractionerin")


def test_blockrotate():
    ciphertext = "iqyaajex ocizyoyebylescohdvfn tjaikec qxrkidbktscrwoavkptepfnkzoltkqvikgdkpvaxvrl"
    actual = block_rotate(ciphertext)
    
    assert_equal(actual[:18], "dokkcfyoiklpt nlcq")
    assert_equal(actual[-18:], "rkkadkdexlgzvbevb ")


def test_hgrid():
    actual = hgrid("kwartslg")
    assert_equal(actual, ["kwartslg ", "bcdefhijm", "nopquvxyz"])

def test_vgrid():
    actual = vgrid("fractionering")
    assert_equal(actual, ["fra", "cti", "one", "g b", "dhj", "klm", "pqs", "uvw", "xyz"])

def test_grid_rotate():
    grid = vgrid("fractionering")

    actual = grid_rotate(grid)
      
    print("ACTUAL", actual)
    assert_equal(actual, ["xupkdgocf", "yvqlh ntr", "zwsmjbeia"])

def test_num_rotate():
    numbers = [[1,2,3],[4,5,6],[7,8,9]]
    
    actual = num_rotate(numbers)
    assert_equal(actual, [[7,4,1],[8,5,2],[9,6,3]])

def test_encode_rechtsboven_linksboven():
    ciphertext = "iqyaajex ocizyoyebylescohdvfn tjaikec qxrkidbktscrwoavkptepfnkzoltkqvikgdkpvaxvrl"
    ciphertext = block_rotate(ciphertext)[:-1]

    grid1 = grid_rotate(vgrid("puzzelmaker"))
    grid2 = grid_rotate(hgrid("kwartslag"))

    numbers = num_rotate([[7,8,5],[1,9,3],[6,2,4]])

    d = Digrafid(grid1, grid2, numbers, 5)
    actual = ciphertext
    for i in range(5):
      actual = d.encode(actual)
    assert_equal(actual[:80], "de overgebleven sleutels in de vier vierkanten linksboven zijn allemaal beroepen")

def test_encode_rechtsboven_rechtsonder():
    grid1 = grid_rotate(grid_rotate(grid_rotate(vgrid("sudoku"))))
    grid2 = grid_rotate(grid_rotate(grid_rotate(hgrid("coudenbergh"))))
    block = "yvgaimpkuoaidxqjhtpxek v wishr oorvrwmjbpksibkqihmptzsuowbfobzjmbr rprkk dd ezkdk"

    ciphertext = block_rotate(block_rotate(block_rotate(block)))[:-1]
    numbers = num_rotate(num_rotate(num_rotate([[3,4,5],[2,6,8],[9,1,7]])))

    explore(grid1, grid2, numbers, ciphertext)

    d = Digrafid(grid1, grid2, numbers, 10)
    actual = multiround(d, ciphertext, 27)

    assert_equal(actual[:len(ciphertext)], "disclaimer natuurlijk is puzzelmaker voor ons geen beroep dit is puur hobbymatig")


def multiround(d, ciphertext, rounds):
    result = ciphertext

    for n in range(rounds):
        result = d.encode(result)

    return result

def explore(grid1, grid2, numbers, ciphertext):
    print(grid1)
    print(grid2)
    print(ciphertext)
    print(numbers)

    for f in range(1, 40):
        d = Digrafid(grid1, grid2, numbers, f)
        actual = ciphertext
        loop = False
        i = 1
        while not loop:
            actual = d.encode(actual)
            print(f, i, actual)
            i+=1
            if actual[:20] == ciphertext[:20]:
                loop = True
        
