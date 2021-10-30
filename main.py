import pygame
from pygame.locals import *
import time

FRAMERATE = 60
GAMERUNNING = True

# Colours
orange = (245, 57, 0)
light = (230, 230, 230)
dark = (9, 0, 33)
purple = (68, 0, 255)

class Game:
    def __init__(self, s_width, s_height):
        self.screen = pygame.display.set_mode((s_width, s_height))
        self.player = None
        self.level = 1
        self.paused = False
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.startTitleScreen()

    def start(self):
        self.control_loop()

    def startTitleScreen(self):
        playButton = Button(self, 10, 10, 100, 50, dark, "play", self.play)

    def play(self, button, event, game):
        pass

    def control_loop(self):
        while self.running:
            self.all_sprites.update()
            print(self.all_sprites)
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    self.running = False

    def update(self):
        pygame.display.flip()

"""
game = Game(640, 480)
player = Player()
game.all_sprites.add(player)
"""

"""
#keeping track of ghost time
start_time = time.start_time
while start_time != 10:
    keep running game
"""

"""
#creating a quit button
quitButton = Button(100, 100, 100, 100, black, "Quit Game", quit)
#creating a start game button
startButton = Button(100, 100, 100, 100, black, "Join Game", start)
"""

"""
quit():
    exit;
"""


class Player(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position):
        pygame.sprite.Sprite.__init__(self)
        self.xPosition = x
        self.yPosition = y
        self.keys = []

class Button(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, colour, text, callback):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)

        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.text = text
        self.callback = callback

    def draw(self):
        pygame.draw.rect(self.game.screen, self.colour, [self.width/2,self.height/2,x,y])

    def check_clicked(self, event):
        mouse = dict(event)["pos"]
        if self.width/2 <= mouse[0] <= self.width/2+x and self.height/2 <= mouse[1] <= self.height/2+y:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click(event)
            else:
                pass
                # Hover event


    def click(self, event):
        self.callback(self, event, self.game)



def main():
    game = Game(640, 480)
    game.start()



if __name__ == "__main__":
    main()
