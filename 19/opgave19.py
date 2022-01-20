from playfair import create_keygrid, playfair_decode

phrase_nl = "OLYMPISCHESPELEN1920"
circles_nl = dict(
  blauw="ZMAKK2PBKCWNEOH6PW1UMSTPEPJKIWOTCPN1WI1BESHAMGQE",
  rood="ZPQW91WNLLOBWP1ADMPIECEYTCN1SV930MAMP0MU1WMWL2KU",
  geel="ELWH6E1SKEIIRT2LPASOXOVSPLAPB6GNKIPETPGYTEW1K91O",
  zwart="OLV9KE16DNWERYIL1EGOTP2SCI1LX2WF1YALTSDDSS16PRRE",
  groen="LMDOQFCSPP1CRLZPIL9N1DLEMUOAM612K0SVDSIR2EWEWEBY",
)

phrase_fr = "JEUXOLYMPIQUES1920"
circles_fr = dict(
  blauw="POQ44ZOJOXRJ9JPLMU2JUCLOE9WRNVADWA9LNIMRIPMU28OE",
  geel="EEUPLIMT4IILTDZSUUPAGYTCMLXAJRMRRNOUUO8ISEU2O09J",
  zwart="RST0OEU6XRUITUZPVUMYS6MYKL9LGSUSDIXEUQWLDTMRUFL1",
  groen="JXXPXSKQKUVMLP96ZQY9ULGEUFRUS6DSLODLWYUFMA4AU1RU",
  rood="9KX0YMFJGJPR4MH9SXOUAMAXWM9XMLRMOEUXUDUFW9SUQOLB"
)


def build_map(circle, key_offset2, offset1, offset2):
    result = dict()
    for i in range(len(circle)):
        left = circle[i] + circle[(i+len(circle)+key_offset2)%len(circle)]
        right = circle[(i+len(circle)+offset1)%len(circle)] + circle[(i+len(circle)+offset2)%len(circle)]
        result.setdefault(left, []).append((right, i))
        
    return result


def fase1(circles):
    blauw_map = build_map(circles["blauw"], 10, 0, 10)
    geel_map = build_map(circles["geel"], -10, 12, 2)
    zwart_map = build_map(circles["zwart"], 10, -12, -2)
    groen_map = build_map(circles["groen"], -10, 12, 2)
    rood_map = build_map(circles["rood"], 10, 0, 10)

    for AB in blauw_map.keys():
      if AB in geel_map.keys():
        for CDpair in geel_map.get(AB,[]):
          CD, CDloc = CDpair
          for EFpair in zwart_map.get(CD,[]):
            EF, EFloc = EFpair
            for GHpair in groen_map.get(EF, []):
              GH, GHloc = GHpair
              if GH in rood_map:
                  print("%s%s%s%s%s%s%s%s"%(AB[0], CD[1], EF[0], GH[1], AB[1], CD[0], EF[1], GH[0]))
              else:
                  print("---discard---")

def main(phrase, circles):
    fase1(circles)
    #fase2(phrase, circles)

if __name__=="__main__":
    print("NEDERLANDS")
    main(phrase_nl, circles_nl)
    print("FRANS")
    main(phrase_fr, circles_fr)
