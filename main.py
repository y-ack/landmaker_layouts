#!/usr/bin/python
import sys, pygame

pygame.display.init()

DIR = "layout_norm"
PREFIX = "layout_norm_"
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

SIZE = WIDTH, HEIGHT = 160-32, 232 * 2.5
black = 0, 0, 0
screen = pygame.display.set_mode(SIZE)
tilerect = tiles[RED].get_rect()

class Tile(pygame.sprite.Sprite):
    def __init__(self, texture, x, y):
       pygame.sprite.Sprite.__init__(self)

       self.image = texture
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y + 232*1.75 - 41

class BoardBG(pygame.sprite.Sprite):
    def __init__(self, texture) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = texture
        self.rect = self.image.get_rect()
        self.rect.x = 5
        self.rect.y = 232*1.75
class DLine(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = LINE_TEX
        self.rect = self.image.get_rect()
        self.rect.x = 5
        self.rect.y = 232*1.75 + 10

color_counts_all = {}
for stage in range(1,9):
    color_counts = {}
    for variant in range(1,5):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        layered_group = pygame.sprite.LayeredUpdates()

        bg = BoardBG(boards.get(f"{PREFIX}{stage}", BOARD_AW))
        layered_group.add(bg, layer=-1000)

        with open(f"{DIR}/{PREFIX}{stage}_{variant}") as pattern:
            words = pattern.readline().split()
            for i in range(0, len(words), 4):
                x = int(words[i], 16)
                if x == 0xFFFF:
                    break
                y = int(words[i+1], 16)
                # WARN: not the exact check
                # reject bad (misaligned) tile data
                if (y & 7 != 0) or ((x-4) % 12 != 0):
                    continue
                c = int(words[i+2], 16)
                color_counts[c] = color_counts.get(c, 0) + 1
                color_counts_all[c] = color_counts_all.get(c, 0) + 1
                z = int(words[i+3], 16)
                t = Tile(tiles[c], x, y)
                
                layered_group.add(t, layer=y)
        
        line = DLine()
        layered_group.add(line, layer=-999)

        with open(f"{DIR}/{PREFIX}{stage}_{variant}u") as pattern:
            words = pattern.readline().split()
            for i in range(0, len(words), 4):
                x = int(words[i], 16)
                if x == 0xFFFF:
                    break
                y = int(words[i+1], 16)
                c = int(words[i+2], 16)
                color_counts[c] = color_counts.get(c, 0) + 1
                color_counts_all[c] = color_counts_all.get(c, 0) + 1
                z = int(words[i+3], 16)
                y = 0x30 + 8 - z - (8 if (x-4) % 24 == 0 else 0)
                t = Tile(tiles[c], x, y)
                
                layered_group.add(t, layer=y)
        
        screen.fill(black)
        layered_group.update()
        layered_group.draw(screen)
        pygame.display.update()
        pygame.image.save(screen, f"out/{PREFIX}{stage}_{variant}.png")
        pygame.time.delay(10)
    print(stage)
    print("RED   :", color_counts.get(RED,0))
    print("BLUE  :", color_counts.get(BLUE,0))
    print("ORANGE:", color_counts.get(ORANGE,0))
    print("GREEN :", color_counts.get(GREEN,0))
    print("CYAN  :", color_counts.get(CYAN,0))
    print("YELLOW:", color_counts.get(YELLOW,0))
    print("PURPLE:", color_counts.get(PURPLE,0))
    print()


print("RED   :", color_counts_all.get(RED,0))
print("BLUE  :", color_counts_all.get(BLUE,0))
print("ORANGE:", color_counts_all.get(ORANGE,0))
print("GREEN :", color_counts_all.get(GREEN,0))
print("CYAN  :", color_counts_all.get(CYAN,0))
print("YELLOW:", color_counts_all.get(YELLOW,0))
print("PURPLE:", color_counts_all.get(PURPLE,0))
