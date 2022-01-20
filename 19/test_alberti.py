
from alberti import *

from nose.tools import assert_equal


def test_alberti():
    outer="ABCDEFGILMNOPQRSTVXZ1234"
    inner="gklnprtvz&xysomqihfdbace"

    alberti = Alberti(outer, inner)

    assert_equal(alberti.decode('n'), 'D')
    assert_equal(alberti.decode('p'), 'E')
    assert_equal(alberti.decode('z'), 'L')


def test_bike():
    outer="ABCDEFGILMNOPQRSTVXZ1234"
    inner="gklnprtvz&xysomqihfdbace"

    front = Alberti(outer, inner)
    back = Alberti(outer, inner)
    
    bike = Bike(front, back)

    ciphertext = "npzpv npmXo i&xbt zxAhg zihzg fhyym Mfdbc kct&e cck2o dlbes kApbh &&kgk oD&x1 kzggd rOxVg yax2& hhbD& xIdlx Iodti 1xyBv tt&Od haoeq hhni2 rtId& sSpff zScp1 chAnp XexbA yym2o f1fpm TkzfX &xEob p2acc aXddk 2cqqr Ixl1s gxPee tPaii Oooe2 btfTo aXzdE d&oz1 vocSa iC&lz 2bver hV&eb gLqry Lyry1 &xIxa kNzf2 o&kkh iGvxo Sakg1 hfLxe eOgk1 ibrTk Xg"
    decoded = bike.decode_phrase("npzpv npmXo i&xbt zxAhg zihzg fhyym Mfdbc kct&e cck2o dlbes kApbh &&kgk oD&x1 kzggd rOxVg yax2& hhbD& xIdlx Iodti 1xyBv tt&Od haoeq hhni2 rtId& sSpff zScp1 chAnp XexbA yym2o f1fpm TkzfX &xEob p2acc aXddk 2cqqr Ixl1s gxPee tPaii Oooe2 btfTo aXzdE d&oz1 vocSa iC&lz 2bver hV&eb gLqry Lyry1 &xIxa kNzf2 o&kkh iGvxo Sakg1 hfLxe eOgk1 ibrTk Xg")

    print(decoded)
    print(ciphertext)

    expect_start = "DELEIDERINDERACEVALTVLAXVOORDEFINISX"

    assert_equal(decoded[1][:len(expect_start)], "DELEIDERINDERACEVALTVLAXVOORDEFINISX")

def test_alberti():
    outer="ABCDEFGILMNOPQRSTVXZ1234"
    inner="gklnprtvz&xysomqihfdbace"

    alberti = Alberti(outer, inner)

    assert_equal(alberti.decode('g'), 'A')

    alberti.rotate_to('B')
 
    assert_equal(alberti.decode('g'), 'B')
    
