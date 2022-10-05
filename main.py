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

size = width, height = 160-32, 232 * 2.5
black = 0, 0, 0
screen = pygame.display.set_mode(size)
tilerect = tiles[RED].get_rect()

class Tile(pygame.sprite.Sprite):
    def __init__(self, texture, x, y):
       pygame.sprite.Sprite.__init__(self)

       self.image = texture
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y + 232*1.75

for stage in range(1,12):
    for variant in range(1,5):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        layered_group = pygame.sprite.LayeredUpdates()

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
                z = int(words[i+3], 16)
                t = Tile(tiles[c], x, y)
                
                layered_group.add(t, layer=y)

        with open(f"{DIR}/{PREFIX}{stage}_{variant}u") as pattern:
            words = pattern.readline().split()
            for i in range(0, len(words), 4):
                x = int(words[i], 16)
                if x == 0xFFFF:
                    break
                y = int(words[i+1], 16)
                c = int(words[i+2], 16)
                z = int(words[i+3], 16)
                y = 0x30 + 8 - z - (8 if (x-4) % 24 == 0 else 0)
                t = Tile(tiles[c], x, y)
                
                layered_group.add(t, layer=y)


        screen.fill(black)
        layered_group.update()
        layered_group.draw(screen)
        pygame.display.update()
        pygame.image.save(screen, f"out/{PREFIX}{stage}_{variant}.png")
        pygame.time.delay(1000)


