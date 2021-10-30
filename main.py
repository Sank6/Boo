import pygame
from pygame.locals import *
import time

BUTTON_TEXT_COLOUR = (64, 28, 20)
## none button
BUTTON_OUTLINE_0 = (162, 88, 69)
BUTTON_OUTLINE_1 = (102, 33, 64)
BUTTON_OUTLINE_2 = (102, 56, 45)
BUTTON_OUTLINE_3 = (162, 88, 69)
BUTTON_OUTLINE_SHADOW = (64, 28, 20)
BUTTON_MAIN = (210, 148, 101)

## pressed Button
BUTTON_PRESSED_OUTLINE_0 = (117, 46, 55)
BUTTON_PRESSED_OUTLINE_1 = (210, 148, 101)
BUTTON_PRESSED_MAIN = (162, 88, 69)

## hovered button
BUTTON_HOVERED_MAIN = (207, 157, 122)

pygame.init()

class Game:
    def __init__(self, s_width, s_height):
        self.screen = pygame.display.set_mode((s_width, s_height), flags=pygame.SCALED)
        self.player = None
        self.level = 1
        self.paused = False
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("assets/title_background.png")

        self.startTitleScreen()

    def start(self):
        self.control_loop()

    def startTitleScreen(self):
        playButton = Button(self, 65, 86, 111, 25, "NEW GAME", self.play)
        playButton = Button(self, 65, 115, 111, 25, "HI-SCORES", self.play)
        quitButton = Button(self, 80, 145, 80, 20, "QUIT", self.quit)


    def quit(self, button, event, game):
        self.running = False

    def play(self, button, event, game):
        pass

    def control_loop(self):
        while self.running:
            self.screen.blit(self.background, (0, 0))

            self.all_sprites.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            for sprite in self.all_sprites:
                if isinstance(sprite, Button):
                    sprite.check_state(event)
                sprite.draw()
            self.update()

        pygame.quit()

    def update(self):
        pygame.display.flip()
        self.clock.tick(60)

"""
game = Game(640, 480)
player = Player()
game.all_sprites.add(player)
"""

"""
#keeping track of ghost time
start_time = time.start_time
while start_time != 600:
    keep running game
"""

"""
#creating a quit button
quitButton = Button(100, 100, 100, 100, black, "Quit Game", quit)
#creating a start game button
startButton = Button(100, 100, 100, 100, black, "Join Game", start)
"""

class Box(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position, width, height, colour, text):
        self.x = x_position
        self.y = y_position
        self.width = width
        self.height = height
        self.colour = colour
        self.text = text
        self.font = pygame.font.Font("assets/font.ttf", height-10)


class Player(pygame.sprite.Sprite):
    def __init__(self, x_position, y_position):
        pygame.sprite.Sprite.__init__(self)
        self.xPosition = x
        self.yPosition = y
        self.keys = []


class Button(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, text, callback):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)

        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font("assets/font.ttf", height-14)

        self.state = "none" # "none", "hovered", "pressed"

    def draw(self):
        screen = self.game.screen
        if self.state == "none":
            pygame.draw.rect(screen, BUTTON_OUTLINE_0, [self.x,self.y+1,self.width,self.height-2])
            pygame.draw.rect(screen, BUTTON_OUTLINE_0, [self.x+1,self.y, self.width-2,self.height])
            pygame.draw.rect(screen, BUTTON_OUTLINE_1, [self.x+1,self.y+1, self.width-2,self.height-2])
            pygame.draw.rect(screen, BUTTON_OUTLINE_2, [self.x+2,self.y+2,self.width-4,self.height-4])
            pygame.draw.rect(screen, BUTTON_OUTLINE_3, [self.x+3,self.y+3,self.width-6,self.height-6])

            pygame.draw.rect(screen, BUTTON_MAIN, [self.x+4,self.y+4,self.width-8,self.height-8])

            pygame.draw.rect(screen, BUTTON_OUTLINE_SHADOW, [self.x+3,self.y+self.height-3,self.width-4,2])
            pygame.draw.rect(screen, BUTTON_OUTLINE_SHADOW, [self.x+self.width-3,self.y+4,2,self.height-5])

        elif self.state == "hovered":
            pygame.draw.rect(screen, BUTTON_OUTLINE_0, [self.x,self.y+1,self.width,self.height-2])
            pygame.draw.rect(screen, BUTTON_OUTLINE_0, [self.x+1,self.y, self.width-2,self.height])
            pygame.draw.rect(screen, BUTTON_OUTLINE_1, [self.x+1,self.y+1, self.width-2,self.height-2])
            pygame.draw.rect(screen, BUTTON_OUTLINE_2, [self.x+2,self.y+2,self.width-4,self.height-4])
            pygame.draw.rect(screen, BUTTON_OUTLINE_3, [self.x+3,self.y+3,self.width-6,self.height-6])

            pygame.draw.rect(screen, BUTTON_HOVERED_MAIN, [self.x+4,self.y+4,self.width-8,self.height-8])

            pygame.draw.rect(screen, BUTTON_OUTLINE_SHADOW, [self.x+3,self.y+self.height-3,self.width-4,2])
            pygame.draw.rect(screen, BUTTON_OUTLINE_SHADOW, [self.x+self.width-3,self.y+4,2,self.height-5])

        elif self.state == "pressed":
            pygame.draw.rect(screen, BUTTON_PRESSED_OUTLINE_0, [self.x+1,self.y+2,self.width-2,self.height-4])
            pygame.draw.rect(screen, BUTTON_PRESSED_OUTLINE_0, [self.x+2,self.y+1, self.width-4,self.height-2])
            pygame.draw.rect(screen, BUTTON_PRESSED_OUTLINE_1, [self.x+2,self.y+2, self.width-4,self.height-4])

            pygame.draw.rect(screen, BUTTON_PRESSED_MAIN, [self.x+3,self.y+3,self.width-6,self.height-6])

        text = self.font.render(self.text, True, BUTTON_TEXT_COLOUR)
        text_rect = text.get_rect(center=(self.x+self.width/2, self.y+self.height/2))
        screen.blit(text, text_rect)

    def check_state(self, event):
        mouse = pygame.mouse.get_pos()
        if self.x <= mouse[0] <= self.x+self.width and self.y <= mouse[1] <= self.y+self.height:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.state == "pressed":
                    self.click(event)
                self.state = "hovered"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.state = "pressed"
            elif self.state == "none":
                self.state = "hovered"
        else:
            self.state = "none"


    def click(self, event):
        self.callback(self, event, self.game)



def main():
    game = Game(240, 180)
    game.start()



if __name__ == "__main__":
    main()
