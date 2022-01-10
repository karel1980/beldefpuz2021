lines = [ l.strip() for l in open('11_opgave.txt').readlines() ]

top = lines[0]
left = lines[1]
grid = lines[2:]

grid = [grid[-1], grid[1], grid[4], grid[2], grid[0], grid[3]]

for line in grid:
    pairs = list(zip(list(top), list(line)))
    pairs.sort()
    print("".join([c for _,c in pairs]))

for line in grid:
    pairs = list(zip(list(top), list(line)))
    pairs.sort()
    print("".join([c for _,c in pairs]).replace('.',' '))


