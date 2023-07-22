import os
import pygame as pg
import time
from pygame.locals import *
import sys
import random

def load_image(name, size):
    file_loc = os.path.join(img_dir, name)

    img = pg.image.load(file_loc)
    # cur_width = img.get_width()
    # cur_height = img.get_height()

    img = pg.transform.scale(img, (size, size))

    return img

def draw_grid(surface, line_color):
    width = surface.get_width()
    gap = width // 3
    surface.fill("white")
    for i in range(gap, width, gap):
        pg.draw.line(surface, line_color, (0, i), (width, i), 2)
        pg.draw.line(surface, line_color, (i, 0), (i, width), 2)
    pg.display.flip()

def clean_values(values):
    values = [ele for ele in values if (ele != "X" and ele != "O")]
    return values


class Board:
    def __init__(self):
        self.winner = None
        self.values = [x for x in range(1, 10)]
        self.turn = 1

    def mark(self, pos, value):
        self.values[pos-1] = value

    def check_mark(self, pos):
        print("In check mark: ", pos, self.values)
        if pos in self.values:
            return True
        else:
            return False

    def get_turn(self):
        return self.turn

    def inc_turn(self):
         self.turn += 1

    def __str__(self):
        # board = self.transform()
        board = self.values
        board_str = f"{board[0]} | {board[1]} | {board[2]}\n" \
                    f"{board[3]} | {board[4]} | {board[5]}\n" \
                    f"{board[6]} | {board[7]} | {board[8]} "
        return board_str

    def transform(self):
        board = [" " if value == 0 else "O" if value==1 else "X" if value==2 else "nan" for value in self.values]
        return board

    def print_winner(self):
        text = "Player " + str(self.winner) + " wins"
        print(text)
        return text

    def has_winner(self):
        for i in range(3):
            if self.check_row(i):
                self.winner = self.get_winner(i * 3)
                return True
            elif self.check_col(i):
                self.winner = self.get_winner(i)
                return True
        if self.check_diags():

            self.winner = self.get_winner(4)
            return True
        return False

    def get_winner(self, pos):
        if self.values[pos] == "X":
            return 0
        else:
            return 1
    def is_tie(self):
        values = clean_values(self.values)
        if len(values) == 0:
            return True

    def check_row(self, row_num):
        if row_num < 0 or row_num > 2:
            return None
        else:
            if self.values[row_num * 3] == self.values[row_num * 3 + 1] and \
                    self.values[row_num * 3] == self.values[row_num * 3 + 2]:
                return True
            else:
                return False

    def check_col(self, col_num):
        if col_num < 0 or col_num > 2:
            return False
        else:
            if self.values[col_num] == self.values[col_num + 3 ] and \
                    self.values[col_num + 3] == self.values[col_num + 6]:
                return True
            else:
                return False


    def check_diags(self):
        #on diagonal
        # print("In check diags")
        # print("values are: ", self.values[4], self.values[0], self.values[8])
        if self.values[4] == self.values[0] == self.values[8]:
            return True
        #off diagonal
        elif self.values[4] == self.values[2] == self.values[6]:
            return True
        return False


    def wins(self, pos, mark):
        self.mark(pos, mark)
        wins = self.has_winner()
        self.mark(pos, pos)
        return wins




class Player:
    players = []

    def __init__(self, number, manual, ai_difficulty=None):
        self.mark = ""
        self.number = number
        self.manual = manual
        self.ai_difficulty = ai_difficulty
        if number == 1:
            self.mark = "X"
        else:
            self.mark = "O"
        self.players.append(self)

    def __str__(self):
        return f"Player {self.number + 1} with mark {self.get_mark()}"

    def get_player(self, number):
        for player in self.players:
            if player.number == number:
                return player
        print("No such player!!!")

    def is_manual(self):
        return self.manual

    def put_mark(self, board, pos):
        board.mark(pos, self.get_mark())

    def get_mark(self):
        return self.mark

    def other(self):
        rplayer = self.get_player(1 - self.number)
        return rplayer

    def make_move(self, board, pos=None):
        if self.is_manual():
            print(f"Player {self.number + 1}, ", end="")
            print("where do you want the mark?")
            self.put_mark(board, pos)
            return None

        elif not self.is_manual():
            values = clean_values(board.values)
            if self.ai_difficulty == 0:
                pos = random.choice(values)
                self.put_mark(board, pos)
                pos = pos - 1
                y_block = pos // 3
                x_block = pos - y_block * 3
                return x_block, y_block

            elif self.ai_difficulty == 1:
                for pos in values:
                    if board.wins(pos, self.get_mark()):
                        self.put_mark(board, pos)
                        pos = pos - 1
                        y_block = pos // 3
                        x_block = pos - y_block * 3
                        return x_block, y_block

                for pos in values:
                    if board.wins(pos, self.other().get_mark()):
                        self.put_mark(board, pos)
                        pos = pos - 1
                        y_block = pos // 3
                        x_block = pos - y_block * 3
                        return x_block, y_block

                pos = random.choice(values)
                self.put_mark(board, pos)
                pos = pos - 1
                y_block = pos // 3
                x_block = pos - y_block * 3
                return x_block, y_block

            elif self.ai_difficulty == 2:
                pos = None
                if board.turn == 1:
                    pos = random.choice([0, 2, 6, 8])
                    self.put_mark(board, pos)

                elif board.turn == 2:
                    #Always start in corner unless opponent starts in corner.
                    #if opponent starts in corner, take center
                    for value in [1, 3, 7, 9]:
                        if value not in values:
                            pos = 5
                    if pos is None:
                        pos = random.choice([1, 3, 7, 9])
                    self.put_mark(board, pos)
                    pos = pos - 1
                    y_block = pos // 3
                    x_block = pos - y_block * 3
                    return x_block, y_block


                elif board.turn == 4:
                    #block if must
                    for pos in values:
                        if board.wins(pos, self.other().get_mark()):
                            self.put_mark(board, pos)
                            pos = pos - 1
                            y_block = pos // 3
                            x_block = pos - y_block * 3
                            return x_block, y_block

                    #if in other places
                    pos = random.choice([val for val in [2, 4, 6, 8] if val in values])
                    self.put_mark(board, pos)
                    pos = pos - 1
                    y_block = pos // 3
                    x_block = pos - y_block * 3
                    return x_block, y_block
                else:
                    #winning moves
                    for pos in values:
                        if board.wins(pos, self.get_mark()):
                            self.put_mark(board, pos)
                            pos = pos - 1
                            y_block = pos // 3
                            x_block = pos - y_block * 3
                            return x_block, y_block
                    #blocking moves
                    for pos in values:
                        if board.wins(pos, self.other().get_mark()):
                            self.put_mark(board, pos)
                            pos = pos - 1
                            y_block = pos // 3
                            x_block = pos - y_block * 3
                            return x_block, y_block
                    pos = random.choice(values)
                    self.put_mark(board, pos)
                    pos = pos - 1
                    y_block = pos // 3
                    x_block = pos - y_block * 3
                    return x_block, y_block





def display_text(surface, msg):
    bg = pg.Surface((400, 100))
    bg = bg.convert()
    bg.fill("white")

    font = pg.font.Font(None, 40)
    text = font.render(msg, True, "black", "white")
    text_rect = text.get_rect(centerx=bg.get_width() / 2, y=bg.get_height() / 2)
    bg.blit(text, text_rect)

    surface.blit(bg, (0, 400))
    #surface.blit(bg, (surface.get_width() / 2, surface.get_height() - 50))
    pg.display.flip()

def select_difficulty(surface):
    bg = pg.Surface((400, 500))
    bg = bg.convert()
    bg.fill("black")

    font = pg.font.Font(None, 40)
    text = font.render("What difficulty?", True, "white", "black")
    text_rect = text.get_rect(centerx=bg.get_width() / 2, y=bg.get_height() / 3)
    bg.blit(text, text_rect)

    button1 = pg.font.Font(None, 36)
    button2 = pg.font.Font(None, 36)
    button3 = pg.font.Font(None, 36)

    text1 = button1.render("Easy", True, "white", "black")
    text_rect1 = text1.get_rect(centerx=bg.get_width() / 2 - 150, y=bg.get_height() / 2)
    bg.blit(text1, text_rect1)

    text2 = button2.render("Med", True, "white", "black")
    text_rect2 = text2.get_rect(centerx=bg.get_width() / 2, y=bg.get_height() / 2)
    bg.blit(text2, text_rect2)

    text3 = button3.render("HARD!", True, "white", "black")
    text_rect3 = text3.get_rect(centerx=bg.get_width() / 2 + 150, y=bg.get_height() / 2)
    bg.blit(text3, text_rect3)
    surface.blit(bg, (0, 0))
    pg.display.flip()

    while True:
        x, y = pg.mouse.get_pos()
        b1_hover = bg.get_width() / 2 - 170 < x < bg.get_width() / 2 - 130 and bg.get_height() / 2 - 30 < y < bg.get_height() / 2 + 30
        b2_hover = bg.get_width() / 2 - 20 < x < bg.get_width() / 2 + 20 and bg.get_height() / 2 - 30 < y < bg.get_height() / 2 + 30
        b3_hover = bg.get_width() / 2 + 130 < x < bg.get_width() / 2 + 170 and bg.get_height() / 2 - 30 < y < bg.get_height() / 2 + 30
        if b1_hover:
            text1_hov = button1.render("Easy", True, "white", "gray")
            text_rect1_hov = text1.get_rect(centerx=bg.get_width() / 2 - 150, y=bg.get_height() / 2)
            bg.blit(text1_hov, text_rect1_hov)

        elif b2_hover:
            button2 = pg.font.Font(None, 36)
            text2_hov = button2.render("Med", True, "white", "gray")
            text_rect2_hov = text2_hov.get_rect(centerx=bg.get_width() / 2, y=bg.get_height() / 2)
            bg.blit(text2_hov, text_rect2_hov)

        elif b3_hover:
            button3 = pg.font.Font(None, 36)
            text3_hov = button3.render("HARD!", True, "white", "gray")
            text_rect3_hov = text3_hov.get_rect(centerx=bg.get_width() / 2 + 150, y=bg.get_height() / 2)
            bg.blit(text3_hov, text_rect3_hov)

        else:
            bg.blit(text1, text_rect1)
            bg.blit(text2, text_rect2)
            bg.blit(text3, text_rect3)

        surface.blit(bg, (0, 0))
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif b1_hover and event.type == pg.MOUSEBUTTONDOWN:
                return 0

            elif b2_hover and event.type == pg.MOUSEBUTTONDOWN:
                return 1

            elif b3_hover and event.type == pg.MOUSEBUTTONDOWN:
                return 2


def ask_input(surface):
    bg = pg.Surface((400, 500))
    bg = bg.convert()
    bg.fill("black")

    font = pg.font.Font(None, 40)
    text = font.render("How many players?", True, "white", "black")
    text_rect = text.get_rect(centerx=bg.get_width() / 2, y=bg.get_height() / 3)
    bg.blit(text, text_rect)

    button1 = pg.font.Font(None, 36)
    button2 = pg.font.Font(None, 36)
    text1 = button1.render("One", True, "white", "black")
    text_rect1 = text1.get_rect(centerx=bg.get_width() / 2 - 100, y=bg.get_height() / 2)
    bg.blit(text1, text_rect1)

    text2 = button2.render("Two", True, "white", "black")
    text_rect2 = text2.get_rect(centerx=bg.get_width() / 2 + 100, y=bg.get_height() / 2)
    bg.blit(text2, text_rect2)
    surface.blit(bg, (0, 0))
    pg.display.flip()

    while True:
        x, y = pg.mouse.get_pos()
        b1_hover = bg.get_width() / 2 - 125 < x < bg.get_width() / 2 - 70 and bg.get_height() / 2 - 30 < y < bg.get_height() / 2 + 30
        b2_hover = bg.get_width() / 2 + 70 < x < bg.get_width() / 2 + 125 and bg.get_height() / 2 - 30 < y < bg.get_height() / 2 + 30
        if b1_hover:
            text1_hov = button1.render("One", True, "white", "gray")
            text_rect1_hov = text1.get_rect(centerx=bg.get_width() / 2 - 100, y=bg.get_height() / 2)
            bg.blit(text1_hov, text_rect1_hov)


        elif b2_hover:
            print("hovering second ...i")
            button2 = pg.font.Font(None, 36)
            text2_hov = button2.render("Two", True, "white", "gray")
            text_rect2_hov = text2_hov.get_rect(centerx=bg.get_width() / 2 + 100, y=bg.get_height() / 2)
            bg.blit(text2_hov, text_rect2_hov)

        else:
            bg.blit(text1, text_rect1)
            bg.blit(text2, text_rect2)

        surface.blit(bg, (0, 0))
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif b1_hover and event.type == pg.MOUSEBUTTONDOWN:
                difficulty = select_difficulty(surface)
                return False, difficulty

            elif b2_hover and event.type == pg.MOUSEBUTTONDOWN:
                return True, None


    # surface.blit(bg, (surface.get_width() / 2, surface.get_height() - 50))


# prepare paths
fldr = os.path.split(os.path.abspath(__file__))[0]
img_dir = os.path.join(fldr, "images")


def play_game():
    size = 400
    line_color = "black"
    gap = size // 3

    # load images
    x_img = load_image("x.png", gap)
    o_img = load_image("o.png", gap)

    pg.init()
    screen = pg.display.set_mode((size, size + 100))
    pg.display.set_caption("My tic tac toe")
    pg.mouse.set_visible(True)


    bg = pg.Surface(screen.get_size())
    bg = bg.convert()
    bg.fill("black")

    #add introduction text
    if pg.font:
        font_style = pg.font.Font(None, 50)
        text = font_style.render("Welcome to Tic Tac Toe", True, "white", "black")
        text_rect = text.get_rect(centerx=bg.get_width() / 2, y=bg.get_height() / 3)
        bg.blit(text, text_rect)

    screen.blit(bg, (0, 0))
    pg.display.flip()
    time.sleep(2)


    #initialize players and board
    player1 = Player(0, True)
    print(player1)

    is_manual, ai_difficulty = ask_input(screen)

    player2 = Player(1, is_manual, ai_difficulty)
    print(player2)
    player = player1
    board = Board()
    print(board)

    draw_grid(screen, line_color)

    #display messages on GUI
    display_text(screen, "Player 1: " + player1.get_mark() + ",  Player 2: " + player2.get_mark())
    time.sleep(2)
    keep_playing = True

    while keep_playing:
        turn = "Player " + str(player.number + 1) + "'s turn"
        display_text(screen, turn)
        correct = False
        if player.is_manual():
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    keep_playing = False
                elif event.type == pg.MOUSEBUTTONDOWN:

                    gap = screen.get_width() // 3
                    x, y = pg.mouse.get_pos()
                    x_block = x // gap
                    y_block = y // gap
                    pos = y_block * 3 + x_block + 1
                    correct = board.check_mark(pos)
                    if not correct:
                        display_text(screen, "Please click a valid box")
                        time.sleep(2)
                        continue
                    correct = True

                    player.make_move(board, pos)
                    print(board)

                    x_loc = x_block * gap
                    y_loc = y_block * gap
                    if player.number == 0:
                        img = o_img
                    else:
                        img = x_img

                    screen.blit(img, (x_loc, y_loc))
                    pg.display.update()



        elif not player.is_manual():
            move = player.make_move(board)
            print(board)
            x_block, y_block = move
            x_loc = x_block * gap
            y_loc = y_block * gap
            if player.number == 0:
                img = o_img
            else:
                img = x_img

            correct = True

            screen.blit(img, (x_loc, y_loc))
            pg.display.update()

        if board.has_winner():
            msg = board.print_winner()
            display_text(screen, msg)
            time.sleep(2)
            keep_playing = False

        elif board.is_tie():
            display_text(screen, "It's a draw")
            time.sleep(2)
            keep_playing = False

        if correct:
            player = player.other()
            board.inc_turn()


play_game()


