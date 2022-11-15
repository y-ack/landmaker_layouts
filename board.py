#!/usr/bin/python
import sys, pygame

pygame.display.init()

DIR = "attack_norm"
PREFIX = "attack_norm_"
DIR = sys.argv[1]
PREFIX = DIR + "_"

RED, BLUE, ORANGE, GREEN, CYAN, YELLOW, PURPLE  = 0, 2, 4, 6, 8, 10, 14
ARROW, STAR, MOON = 11, 12, 13
tiles = { RED    : pygame.image.load("pngtile/tilered.png"),
          BLUE   : pygame.image.load("pngtile/tileblue.png"),
          ORANGE : pygame.image.load("pngtile/tileorange.png"),
          GREEN  : pygame.image.load("pngtile/tilegreen.png"),
          CYAN   : pygame.image.load("pngtile/tilecyan.png"),
          YELLOW : pygame.image.load("pngtile/tileyellow.png"),
          PURPLE : pygame.image.load("pngtile/tilepurple.png"),
          ARROW : pygame.image.load("pngtile/tilegray.png"),
          STAR : pygame.image.load("pngtile/tilegray.png"),
          MOON : pygame.image.load("pngtile/tilegray.png")}
BOARD_BOSS = pygame.image.load("pngtile/bg/_BL_NFLI_A01.png")
BOARD_AW = pygame.image.load("pngtile/bg/_BL_NFLY_A01.png")
boards = { "layout_norm_1" : pygame.image.load("pngtile/bg/_BL_NFLA_B01.png"),
           "layout_norm_2" : pygame.image.load("pngtile/bg/_BL_NFLB_B01.png"),
           "layout_norm_3" : pygame.image.load("pngtile/bg/_BL_NFLC_B01.png"),
           "layout_norm_4" : pygame.image.load("pngtile/bg/_BL_NFLD_B01.png"),
           "layout_norm_5" : pygame.image.load("pngtile/bg/_BL_NFLE_A01.png"),
           "layout_norm_6" : pygame.image.load("pngtile/bg/_BL_NFLF_A01.png"),
           "layout_norm_7" : pygame.image.load("pngtile/bg/_BL_NFLG_B01.png"),
           "layout_norm_8" : pygame.image.load("pngtile/bg/_BL_NFLH_A01.png"),
           "layout_norm_9" : BOARD_BOSS,
           "layout_norm_10" : pygame.image.load("pngtile/bg/_BL_NFLJ_A01.png"),
           "layout_norm_11" : BOARD_BOSS,
           "layout_aw_2" : pygame.image.load("pngtile/bg/_BL_NFLY_A01.png")}
LINE_TEX = pygame.image.load("pngtile/line.png")

SIZE = WIDTH, HEIGHT = 160-32, 172
black = 0, 0, 0
screen = pygame.display.set_mode(SIZE)
tilerect = tiles[RED].get_rect()

class Tile(pygame.sprite.Sprite):
    def __init__(self, texture, x, y):
       pygame.sprite.Sprite.__init__(self)

       self.image = texture
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y + 8

class BoardBG(pygame.sprite.Sprite):
    def __init__(self, texture) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = texture
        self.rect = self.image.get_rect()
        self.rect.x = 5
        self.rect.y = 0
class DLine(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = LINE_TEX
        self.rect = self.image.get_rect()
        self.rect.x = 5
        self.rect.y = 0 + 10


for stage in range(0,18):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    layered_group = pygame.sprite.LayeredUpdates()

    bg = BoardBG(boards.get(f"{PREFIX}{stage}", BOARD_AW))
    layered_group.add(bg, layer=-1000)

    with open(f"{DIR}/{PREFIX}{stage}","r") as pattern_f:
        pattern = pattern_f.read()
        words = [pattern[idx:idx + 4] for idx in range(0, len(pattern), 4)]
        for i in range(0, len(words)):
            c = int(words[i], 16)
            if c == 0xFFFF:
                continue
            x = (i % 9) * 12 + 4
            y = (i // 9)*16
            if (i & 1) != (i//9 & 1):
                y += 8
            t = Tile(tiles[c], x, y)
            
            layered_group.add(t, layer=y)
    
    line = DLine()
    layered_group.add(line, layer=-999)

    screen.fill(black)
    layered_group.update()
    layered_group.draw(screen)
    pygame.display.update()
    pygame.image.save(screen, f"out/{PREFIX}{stage}.png")
    pygame.time.delay(100)

