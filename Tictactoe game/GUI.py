import pygame as pg
import sys
import time
import os
from pygame.locals import *


size = 400
line_color = "black"
gap = size // 3

# prepare paths

fldr = os.path.split(os.path.abspath(__file__))[0]
img_dir = os.path.join(fldr, "images")


def load_image(name, size):
    file_loc = os.path.join(img_dir, name)

    img = pg.image.load(file_loc)
    # cur_width = img.get_width()
    # cur_height = img.get_height()

    img = pg.transform.scale(img, (size, size))

    return img

def draw_grid(surface):
    width = surface.get_width()
    gap = width // 3
    surface.fill("white")
    for i in range(gap, width, gap):
        pg.draw.line(surface, line_color, (0, i), (width, i), 2)
        pg.draw.line(surface, line_color, (i, 0), (i, width), 2)
    pg.display.flip()


pg.init()
screen = pg.display.set_mode((size, size))
pg.display.set_caption("My tic tac toe")
pg.mouse.set_visible(True)

x_img = load_image("x.png", gap)
o_img = load_image("o.png", gap)


bg = pg.Surface(screen.get_size())
bg = bg.convert()
bg.fill((0, 0, 200))

if pg.font:
    font_style = pg.font.Font(None, 50)
    text = font_style.render("Welcome to Tic Tac Toe", True, "white", "black")
    text_rect = text.get_rect(centerx=bg.get_width() / 2, y=bg.get_height() / 3)
    bg.blit(text, text_rect)

screen.blit(bg, (0, 0))
pg.display.flip()

time.sleep(2)

# quran = load_image("quran.jpg")
# screen.fill((0,0,0))
# screen.blit(quran, (0, 0))
# pg.display.flip()
# time.sleep(2)

draw_grid(screen)
time.sleep(3)

keep_playing = True

while keep_playing:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            keep_playing = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            gap = screen.get_width() // 3
            x, y = pg.mouse.get_pos()
            x_block = x // gap
            y_block = y // gap

            print("In mouse event")

            x_loc = (x_block ) * gap
            y_loc = (y_block) * gap
            screen.blit(x_img, (x_loc, y_loc))
            pg.display.update()

