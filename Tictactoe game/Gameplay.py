from board import *

board = Board()
print(board)

if input("Do you want X or O?").lower() == 'x':
    player = Player(1, True)
else:
    player = Player(2, True)

player.make_move()
player.put_mark(board, int(input("where do you want the mark?")))
print(board)
print("Player is manual: ",player.is_manual())


