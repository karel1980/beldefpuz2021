
from digrafid import Digrafid


def cycle(grid1, grid2, numbers, fraction, text):
    print("Fraction", fraction)

    result = digraf_encode(grid1, grid2, numbers, fraction, text)
    print(1, result)

    result1 = result
    for i in range(100):
        result = digraf_encode(grid1, grid2, numbers, fraction, result)
        print(i+1, result)
        if result == result1:
            return

def main():
    var encoder = Digrafid("digraf", "fractionering", [[1,2,3],[4,5,6],[7,8,9]], 3)

    print(encoder.encode("hello world"))


if __name__=="__main__":
    main()
