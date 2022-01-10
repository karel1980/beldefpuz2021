
from nose.tools import assert_equal
from playfair import create_keygrid, playfair_encode, playfair_decode

def test_create_keygrid_works():
    actual = create_keygrid("STALINGRAD", 5, "ABCDEFGHIKLMNOPQRSTUVWXYZ")

    expected = [ "STALI", "NGRDB", "CEFHK", "MOPQU", "VWXYZ" ]
    assert_equal(actual, expected)


def test_encode():
    keygrid = create_keygrid("STALINGRAD", 5, "ABCDEFGHIKLMNOPQRSTUVWXYZ")
    plaintext = "DITISEENZEERGEHEIMBERICHT"

    actual = playfair_encode(keygrid, plaintext)

    expected = "BLASTCCGWKFGEOKFSUGKBAEKAW"
    assert_equal(actual, expected)

def test_decode():
    keygrid = create_keygrid("STALINGRAD", 5, "ABCDEFGHIKLMNOPQRSTUVWXYZ")
    ciphertext = "BLASTCCGWKFGEOKFSUGKBAEKAW"

    actual = playfair_decode(keygrid, ciphertext)

    expected = "DITISEENZEERGEHEIMBERICHTX"
    assert_equal(actual, expected)

