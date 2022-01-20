from solve import Die, MOVES, NORTH, SOUTH, EAST, WEST, MOVE_NORTH, MOVE_SOUTH, MOVE_EAST, MOVE_WEST, Board, Cell, solve
from nose.tools import assert_equal

def test_board_creation():
    b = Board()

    assert_equal(len(b.grid), 8)
    assert_equal(len(b.grid[0]), 8)

    assert_equal(b.grid[0][0].liberties, 2)
    assert_equal(b.grid[0][1].liberties, 3)
    assert_equal(b.grid[1][1].liberties, 4)

def test_board_set_value():
    b = Board()

    b.set_value((0,1), 100)

    assert_equal(b.grid[0][1].value, 100)
    assert_equal(b.grid[0][0].liberties, 1)
    assert_equal(b.grid[0][2].liberties, 2)

    b.clear_value((0,1))

    assert_equal(b.grid[0][1].value, None)
    assert_equal(b.grid[0][0].liberties, 2)
    assert_equal(b.grid[0][2].liberties, 3)

def test_board_count_free():
    b = Board()
    assert_equal(b.count_free(), 64)

    b.set_value((0,1), 100)
    assert_equal(b.count_free(), 63)

    b.clear_value((0,1))
    assert_equal(b.count_free(), 64)


def test_cell_is_set():
    c = Cell((10, 10), 4)
    assert_equal(c.is_set(), False)
    
    c.value = 100
    assert_equal(c.is_set(), True)
      

def test_die():
    die = Die()
    die.roll(MOVE_NORTH)

    assert_equal(die.pos, (0,3))
    assert_equal(die.top, 2)
    assert_equal(die.bottom, 5)
    assert_equal(die.front, 1)
    assert_equal(die.back, 6)
    assert_equal(die.left, 3)
    assert_equal(die.right, 4)


def test_move_is_valid():
    board = Board()
    die = Die()
    r,c = die.pos

    actual = list(board.get_horse_values(die.pos))
    assert_equal(actual, [])

    board.set_value((r-1, c-2), 10)

    print(board.show_path(die.pos, []))
    actual = list(board.get_horse_values(die.pos))
    assert_equal(actual, [ 10 ])


def test_solve():
    actual = solve(Board(5, 5), Die())

    expected="SSSENNNNWWSSSSWNNNNWSSSS"
    assert_equal("".join([m.name for m in actual]), expected)
