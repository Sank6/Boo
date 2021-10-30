import pygame
from pygame.locals import *
import time, math

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

# Keybinds
LEFT_KEY = pygame.K_LEFT
RIGHT_KEY = pygame.K_RIGHT
UP_KEY = pygame.K_UP
DOWN_KEY = pygame.K_DOWN

pygame.init()

class Game:
    def __init__(self, s_width, s_height):
        self.screen = pygame.display.set_mode((s_width, s_height), flags=pygame.SCALED)
        self.level = 1
        self.paused = False
        self.running = True
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()

        self.barrier_sprites = pygame.sprite.Group()
        self.kid_sprites = pygame.sprite.Group()
        self.witch_sprites = pygame.sprite.Group()
        self.potion_sprites = pygame.sprite.Group()
        # Custom Sprites
        self.backgrounds = [
            pygame.image.load("assets/title_background_1.png"),
            pygame.image.load("assets/title_background_2.png"),
            pygame.image.load("assets/title_background_3.png"),
        ]
        self.witch = None
        self.boo = None # ✨ The Player ✨

        self.startTitleScreen()

    def start(self):
        self.control_loop()

    def startTitleScreen(self):
        playButton = Button(self, 65, 90, 110, 25, "NEW GAME", self.play)
        playButton = Button(self, 65, 120, 110, 25, "HI-SCORES", self.play)
        quitButton = Button(self, 80, 150, 80, 20, "QUIT", self.quit)

    def quit(self, button, event, game):
        self.running = False

    def play(self, button, event, game):
        self.clean()
        if self.level == 1:
            # Level 1 boo starting position
            self.boo.x = 33
            self.boo.y = 33
            self.boo.draw()
            self.backgrounds = [pygame.image.load("assets/level1_background.png")]

            # Level 1 barriers
            barriers = [
                Barrier(self, 8, 10),
                Barrier(self, 8, 24),
                Barrier(self, 8, 38),
            ]

            #Kid(self, [(160, 8), (160, 168)])
            Witch(game, 120, 120)

    def clean(self):
        self.all_sprites.empty()
        self.barrier_sprites.empty()
        self.kid_sprites.empty()
        self.witch = None
        self.boo = Boo(self)

    def control_loop(self):
        frame_count = 0
        while self.running:
            frame_count = (frame_count + 1) % 60
            self.screen.blit(self.backgrounds[math.floor(frame_count / 10) % len(self.backgrounds)], (0, 0))

            self.all_sprites.update()

            # This needs to be outside events so holding a key moves Boo
            if self.boo != None:
                self.boo.move(pygame.key.get_pressed())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            for sprite in self.all_sprites:
                if isinstance(sprite, Button):
                    sprite.check_state(event)
                if isinstance(sprite, Potion):
                    sprite.draw(frame_count)
                else:
                    sprite.draw()
            self.update()

        pygame.quit()

    def update(self):
        pygame.display.flip()
        self.clock.tick(60)


class Kid(pygame.sprite.Sprite):
    def __init__(self, game, points):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)
        game.kid_sprites.add(self)

        self.game = game
        self.points = points
        self.currentTargetIndex = 0

        self.x = points[0][0]
        self.y = points[0][1]

        self.image = pygame.image.load("assets/kid.png")

    def draw(self):
        lastPoint = self.points[self.previousPointIndex+1]
        nextPoint = self.points[self.previousPointIndex+1]

        if nextPoint[0] < self.x:
            self.x -= 1
        elif nextPoint[0] > self.x:
            self.x += 1
        if nextPoint[1] < self.y:
            self.y -= 1
        elif nextPoint[1] > self.y:
            self.y += 1

        if self.x == nextPoint[0] and self.y == nextPoint[1]:
            self.previousPointIndex += 1

        self.game.screen.blit(self.image, (self.x, self.y))

class Witch(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)
        game.witch_sprites.add(self)

        self.game = game

        self.x = x
        self.y = y # Witch is 1x2 so the y coordinate is the top one.
        self.image = pygame.image.load("assets/witch/up.png")

        self.potionDist = 50

        self.potion = None
    
    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))

        # Throw potion if close enough
        if abs(abs(self.x) - abs(self.game.boo.x)) < self.potionDist and abs(abs(self.y) - abs(self.game.boo.y)) < self.potionDist:
            if self.potion == None:
                self.potion = self.throwPotion()

    def throwPotion(self):
        return Potion(self.game, self)
    
class Potion(pygame.sprite.Sprite):
    def __init__(self, game, witch):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)
        game.potion_sprites.add(self)

        self.x = witch.x
        self.y = witch.y

        self.game = game
        self.witch = witch

        self.animation = [
            pygame.image.load("assets/potions/1.png"),
            pygame.image.load("assets/potions/2.png"),
            pygame.image.load("assets/potions/3.png"),
        ]

        self.len = 1
        self.total = 60
        print("Ooo")


    def draw(self, frame_count):
        if self.len > self.total:
            self.game.potion_sprites.remove(self)
            self.game.all_sprites.remove(self)
            return
        # Animate potion
        self.game.screen.blit(self.animation[math.floor(frame_count / 10) % len(self.animation)], (self.x, self.y))
        self.len = self.len + 1
        
        # lerp between witch and boo
        self.x = self.witch.x + (self.game.boo.x - self.witch.x) * (self.len / self.total)
        self.y = self.witch.y + (self.game.boo.y - self.witch.y) * (self.len / self.total)

class Barrier(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)
        game.barrier_sprites.add(self)

        self.game = game
        self.x = x+1
        self.y = y+1
        self.width = 14
        self.height = 14
        self.image = pygame.image.load("assets/barrier.png")

    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))

class Boo(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)

        self.width = 16
        self.height = 16
        self.x = 0
        self.y = 0
        self.keys = []
        self.game = game
        self.moving = "down" # "up", "down", "left", "right"

        self.images = {
            "left": pygame.image.load(f"assets/boo/left.png"),
            "right": pygame.image.load(f"assets/boo/right.png"),
            "up": pygame.image.load(f"assets/boo/up.png"),
            "down": pygame.image.load(f"assets/boo/down.png"),
        }

    def draw(self):
        boo = self.images[self.moving]
        self.game.screen.blit(boo, (self.x, self.y))

    def move(self, keys):
        x_delta = 0
        y_delta = 0

        if keys[LEFT_KEY]:
            x_delta = -1
            self.moving = "left"
        if keys[RIGHT_KEY]:
            x_delta = 1
            self.moving = "right"
        if keys[UP_KEY]:
            y_delta = -1
            self.moving = "up"
        if keys[DOWN_KEY]:
            y_delta = 1
            self.moving = "down"

        new_x = self.x + x_delta
        new_y = self.y + y_delta

        # Check if boo hit a wall
        for barrier in self.game.barrier_sprites:
            check_x = lambda x: barrier.x <= x <= barrier.x+barrier.width
            check_y = lambda y: barrier.y <= y <= barrier.y+barrier.height

            in_x_axis = lambda x: check_x(x) or check_x(x+self.width) or check_x(new_x+self.width/2)
            in_y_axis = lambda y: check_y(y) or check_y(y+self.height) or check_y(new_y+self.height/2)

            if in_y_axis(new_y) and in_x_axis(new_x):
                x_delta = 0
                y_delta = 0

        # Check that boo doesn't escape his container
        if new_x < 8 or new_x+self.width > 240-8:
            x_delta = 0
        if new_y < 10 or new_y+self.height > 180-10:
            y_delta = 0

        self.x += x_delta
        self.y += y_delta


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




if __name__ == "__main__":
    game = Game(240, 180)
    game.start()
