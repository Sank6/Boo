import pygame
from pygame.locals import *
import time
import math
import json
import random
import os

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

## text input box
INPUT_MAIN = (228, 201, 150)

pygame.init()
pygame.display.set_caption("Boo - The Game")
programIcon = pygame.image.load('assets/boo/up.png')
pygame.display.set_icon(programIcon)

class Game:
    def __init__(self, s_width, s_height):
        self.screen = pygame.display.set_mode((s_width, s_height), flags=pygame.SCALED)
        self.level = 1
        self.levels = len(os.listdir("levels/"))
        self.paused = False
        self.running = True
        self.in_level = False
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()

        self.barrier_sprites = pygame.sprite.Group()
        self.kid_sprites = pygame.sprite.Group()
        self.witch_sprites = pygame.sprite.Group()
        self.potion_sprites = pygame.sprite.Group()
        self.uncaptured_key_sprites = pygame.sprite.Group()
        self.captured_key_sprites = pygame.sprite.Group()
        self.props_sprites = pygame.sprite.Group()
        self.blackout_sprites = pygame.sprite.Group()
        self.debuff_sprites = pygame.sprite.Group()

        # Custom Sprites
        self.witch = None
        self.boo = None # ✨ The Player ✨
        self.time_taken_in_game = 0
        self.total_time = 4 * 60
        self.time_box = None
        self.key_box = None
        self.player_name = ""
        self.cut_scene = None

        self.keybinds = {
            "LEFT_KEY": [pygame.K_a, pygame.K_LEFT],
            "RIGHT_KEY": [pygame.K_d, pygame.K_RIGHT],
            "UP_KEY": [pygame.K_w, pygame.K_UP],
            "DOWN_KEY": [pygame.K_s, pygame.K_DOWN],
        }

        self.default_keybinds = self.keybinds.copy()

        self.start_title_screen()

        self.keybinds_reversed = False

        pygame.mixer.music.load("assets/title_screen_music.mp3")
        pygame.mixer.music.play(-1)

    def start(self):
        self.control_loop()

    def start_title_screen(self):
        self.clean()
        self.backgrounds = [
            pygame.image.load("assets/title_background/1.png"),
            pygame.image.load("assets/title_background/2.png"),
            pygame.image.load("assets/title_background/3.png"),
        ]
        self.level = 1
        playButton = Button(self, 65, 90, 110, 25, "NEW GAME", self.intro_cut_screen)
        playButton = Button(self, 65, 120, 110, 25, "HI-SCORES", self.start_leaderboard_screen)
        quitButton = Button(self, 37.5, 150, 80, 20, "QUIT", self.quit)
        quitButton = Button(self, 122.5, 150, 80, 20, "CREDITS", self.credits)

    def start_title_screen_callback(self, button, event, game):
        pygame.mixer.music.fadeout(500)
        pygame.mixer.music.load("assets/title_screen_music.mp3")
        pygame.mixer.music.play(-1)
        self.start_title_screen()

    def start_leaderboard_screen(self, button, event, game):
        self.clean()
        self.backgrounds = [pygame.image.load("assets/leaderboard_background.png")]
        Button(self, 4, 155, 60, 20, "BACK", self.start_title_screen_callback)
        LeaderboardContent(self)

    def intro_cut_screen(self, button, event, game):
        self.clean()
        self.backgrounds = [
            pygame.image.load("assets/cutscene/bg1.png"),
            pygame.image.load("assets/cutscene/bg2.png"),
            pygame.image.load("assets/cutscene/bg2.png")
        ]
        self.cut_scene = CutSceneContent(self)
        Button(self, 4, 155, 60, 20, "SKIP", self.start_game)

    def credits(self, button, event, game):
        self.clean()
        self.backgrounds = [pygame.image.load("assets/credits.png")]
        Button(self, 4, 155, 60, 20, "BACK", self.start_title_screen_callback)

    def quit(self, button, event, game):
        self.running = False

    def start_game(self, button, event, game):
        self.all_sprites.remove(self.cut_scene)
        self.cut_scene = None
        self.time_taken_in_game = 0
        pygame.mixer.music.fadeout(500)
        pygame.mixer.music.load("assets/audio.mp3")
        pygame.mixer.music.play(-1)
        self.play(button, event, game)

    def reverse_keybinds(self):
        kb = self.keybinds.copy()
        self.keybinds["LEFT_KEY"] = kb["RIGHT_KEY"]
        self.keybinds["RIGHT_KEY"] = kb["LEFT_KEY"]
        self.keybinds["UP_KEY"] = kb["DOWN_KEY"]
        self.keybinds["DOWN_KEY"] = kb["UP_KEY"]
        self.keybinds_reversed = time.time()

    def play(self, button, event, game):
        self.clean()
        self.in_level = True
        self.boo = Boo(self)
        self.backgrounds = [pygame.image.load(f"assets/level_backgrounds/{self.level}.png")]

        for i in range(0, 20):
            prop = random.choice(["rock", "rocks", "mushroom", "weed"])
            Prop(self, random.randint(8, 208), random.randint(10, 150), prop)

        ##load game programatically
        lines = []
        f = open(f"levels/{self.level}.txt", "r")
        lines = f.readlines()
        x,y,k=0,0,0
        kid_coords = {}
        for line in lines:
            last_was_barrier = False
            for char in line:
                if char == "#":
                    if last_was_barrier != False and random.randint(0,5) == 1:
                        self.all_sprites.remove(last_was_barrier)
                        self.barrier_sprites.remove(last_was_barrier)
                        last_was_barrier = False
                        Barrier(self, 16*(x-1)+8, 16*y+10, log=True)
                    else:
                        last_was_barrier = Barrier(self, 16*x+8, 16*y+10)
                else:
                    last_was_barrier = False
                if char == "K":
                    Key(self, 16*x+8, 16*y+10, k)
                    k += 1
                elif char == "D":
                    Door(self, 16*x+8, 16*y+10)
                elif char == "W":
                    Witch(self, 16*x+8, 16*y-6)
                elif char == "P":
                    self.boo.x = 16*x+8
                    self.boo.y = 16*y+10
                elif char == "T":
                    Barrier(self, 16*x+8, 16*y+10, tree=True)
                elif char == " ":
                    pass
                elif char.isnumeric():
                    if char in kid_coords:
                        kid_coords[char].append((16*x+8, 16*y-6))
                    else:
                        kid_coords[char] = [(16*x+8, 16*y-6)]
                x+=1
            x=0
            y+=1

        for key in kid_coords:
            Kid(self, kid_coords[key])

        for sprite in self.captured_key_sprites:
            self.captured_key_sprites.remove(sprite)

        self.time_box = TextBox(self, 213, 3, 6, "Loading")
        self.key_box = TextBox(self, 20, 1, 6, "0", colour=BUTTON_MAIN)
        BatCompanion(self, self.boo)

    def restart_level(self):
        self.clean()
        self.in_level = False

        self.backgrounds = [pygame.image.load("assets/title_background/0.png")]

        Button(self, 65, 90, 110, 25, "TRY AGAIN", self.play)
        Button(self, 80, 150, 80, 20, "QUIT", self.start_title_screen_callback)

    def level_completed(self):
        self.in_level = False
        if self.level == self.levels:
            self.game_completed()
        else:
            self.next_level()

    def game_completed(self):
        self.level = 1
        self.clean()

        self.backgrounds = [pygame.image.load("assets/end_screen.png")]

        TextBox(self, 70, 85, 10, str(int(self.time_taken_in_game))+"s")
        TextInput(self, 19, 106, 203, 18, "Enter your name:", self.player_entered_name)
        Button(self, 65, 140, 110, 25, "CONTINUE", self.player_entered_name_button)

    def game_over(self):
        self.in_level = False
        self.clean()

        self.backgrounds = [pygame.image.load("assets/game_over.png")]

        TextBox(self, 125, 85, 10, str(int((self.level - 1) * 100 / self.levels))+"%")
        TextInput(self, 19, 106, 203, 18, "Enter your name:", self.player_entered_name)
        Button(self, 65, 140, 110, 25, "TRY AGAIN", self.player_entered_name_button)
        self.level = 1

    def player_entered_name_button(self, game, event, button):
        self.game_over_ = False
        for s in self.all_sprites:
            if isinstance(s, TextInput):
                name = s.text
        self.player_entered_name(name)

    def player_entered_name(self, name):
        self.player_name = name

        with open("scores.json") as scores_json:
            leaderboard = json.load(scores_json)
        leaderboard.append({
            "name": self.player_name,
            "time": int(self.time_taken_in_game)
        })
        leaderboard.sort(key = lambda p: p["time"])
        with open("scores.json", "w") as scores_json:
            json.dump(leaderboard, scores_json, indent=3)
        self.time_taken_in_game = 0
        self.start_title_screen()



    def next_level(self):
        self.in_level = False
        self.level += 1
        self.clean()

        self.backgrounds = [pygame.image.load("assets/title_background/1.png")]

        Button(self, 65, 90, 110, 25, "CONTINUE", self.play)
        Button(self, 80, 150, 80, 20, "QUIT", self.start_title_screen_callback)


    def clean(self):
        self.all_sprites.empty()
        self.barrier_sprites.empty()
        self.kid_sprites.empty()
        self.witch = None
        self.boo = None

        self.game_over_ = False

        self.keybinds = self.default_keybinds.copy()

    def control_loop(self):
        frame_count = 0
        while self.running:
            if self.time_taken_in_game > self.total_time and not self.game_over_ and self.in_level:
                self.game_over()
                self.game_over_ = True
                continue
            frame_count = (frame_count + 1) % 3600
            self.screen.blit(self.backgrounds[math.floor(frame_count / 10) % len(self.backgrounds)], (0, 0))

            self.all_sprites.update()

            # This needs to be outside events so holding a key moves Boo
            if self.boo != None:
                self.boo.move(pygame.key.get_pressed())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                for sprite in self.all_sprites:
                    if isinstance(sprite, (Button, TextInput)):
                        sprite.check_state(event)

            for sprite in self.all_sprites:
                sprite.draw(frame_count)

            if self.boo != None:
                self.boo.draw(frame_count)

            for blackout in self.blackout_sprites:
                blackout.draw(frame_count)

            self.update()

            if self.keybinds_reversed != False:
                if time.time() - self.keybinds_reversed > 10:
                    self.keybinds_reversed = False
                    self.keybinds = self.default_keybinds.copy()

                    if self.boo:
                        for debuff in self.boo.debuffs:
                            if debuff.prop == "reversed":
                                debuff.delete_sprite()

            if self.in_level:
                if (self.time_box):
                    self.time_box.text = str(int(self.total_time - self.time_taken_in_game))
                if (self.key_box):
                    self.key_box.text = str(len(self.captured_key_sprites))
                self.time_taken_in_game += 1/60

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
        self.current_target_index = 1

        self.draw_x = points[0][0]
        self.draw_y = points[0][1]

        self.x = self.draw_x
        self.y = self.draw_y + 12

        self.width = 16
        self.height = 20

        self.images = {
            "down": pygame.image.load("assets/kid/down.png"),
            "down_walking_1": pygame.image.load("assets/kid/down_walking_1.png"),
            "down_walking_2": pygame.image.load("assets/kid/down_walking_2.png"),
            "left": pygame.image.load("assets/kid/left.png"),
            "left_walking": pygame.image.load("assets/kid/left_walking.png"),
            "up": pygame.image.load("assets/kid/up.png"),
            "up_walking_1": pygame.image.load("assets/kid/up_walking_1.png"),
            "up_walking_2": pygame.image.load("assets/kid/up_walking_2.png"),
            "right": pygame.image.load("assets/kid/right.png"),
            "right_walking": pygame.image.load("assets/kid/right_walking.png"),
        }
        self.dir = "down"

    def update(self):
        if len(self.points) == 0: return None

        last_point = self.points[self.current_target_index-1]
        target_point = self.points[self.current_target_index]

        if target_point[0] != last_point[0]:
            dir = ((target_point[0]-last_point[0]) / abs(target_point[0]-last_point[0]))
            self.draw_x += 0.4 * dir
            if dir < 0:
                self.dir = "left"
            else:
                self.dir = "right"
        if target_point[1] != last_point[1]:
            dir = ((target_point[1]-last_point[1]) / abs(target_point[1]-last_point[1]))
            self.draw_y += 0.4 * dir
            if dir < 0:
                self.dir = "up"
            else:
                self.dir = "down"

        if (self.draw_x-0.2 <= target_point[0] <= self.draw_x+0.2
        and self.draw_y-0.2 <= target_point[1] <= self.draw_y+0.2):
            self.draw_x, self.draw_y = target_point
            if self.current_target_index+1 == len(self.points):
                self.current_target_index = 1
                self.points.reverse()
            else:
                self.current_target_index += 1

        self.x = self.draw_x
        self.y = self.draw_y + 12

    def draw(self, frame_count):
        image = self.images[self.dir]
        if self.dir == "left" or self.dir == "right":
            if (math.floor(frame_count / 10)) % 2 == 0:
                image = self.images[self.dir + "_walking"]
        elif self.dir == "up" or self.dir == "down":
            if (math.floor(frame_count / 10)) % 2 == 0:
                image = self.images[self.dir + "_walking_1"]
            else:
                image = self.images[self.dir + "_walking_2"]
        self.game.screen.blit(image, (self.draw_x, self.draw_y))


class Witch(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)
        game.witch_sprites.add(self)

        self.game = game

        self.x = x
        self.y = y # Witch is 1x2 so the y coordinate is the top one.
        self.images = [
            pygame.image.load("assets/witch/up.png"),
            pygame.image.load("assets/witch/right.png"),
            pygame.image.load("assets/witch/down.png"),
            pygame.image.load("assets/witch/left.png"),
        ]

        self.potionDist = 16*4
        self.potion_timeout = 5
        self.last_potion_thrown_at = 0
        self.direction_index = 0

    def update(self):
        # Throw potion if close enough
        if abs(abs(self.x) - abs(self.game.boo.x)) < self.potionDist and abs(abs(self.y) - abs(self.game.boo.y)) < self.potionDist:
            if time.time() - self.last_potion_thrown_at > self.potion_timeout:
                Potion(self.game, self)
                self.last_potion_thrown_at = time.time()

    def draw(self, frame_count):
        self.game.screen.blit(self.images[math.floor(frame_count / 20) % (len(self.images))], (self.x, self.y))


class Potion(pygame.sprite.Sprite):
    def __init__(self, game, witch):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)
        game.potion_sprites.add(self)

        self.x = witch.x
        self.y = witch.y

        self.game = game
        self.witch = witch

        self.potion_colours = [ "b", "g", "r", "p", "y"]

        self.picked_colour = self.potion_colours[random.randint(0, len(self.potion_colours)-1)]

        self.animation = []

        for i in range(1, 3):
            self.animation.append(pygame.image.load("assets/potions/" + self.picked_colour + str(i) + ".png"))

        self.potion_effects = [
            "Speed Up",
            "Slow Down",
            "Stun",
            "Reverse Controls",
            "Blackout"
        ]

        self.len = 1
        self.total = 60


    def draw(self, frame_count):
        if self.len > self.total:
            self.game.potion_sprites.remove(self)
            self.game.all_sprites.remove(self)
            self.affected_by_potion()
            return
        # Animate potion
        calc = math.floor(self.len / 20)
        if calc >= len(self.animation):
            calc = len(self.animation) - 1
        self.game.screen.blit(self.animation[calc], (self.x, self.y))
        self.len = self.len + 1

        # lerp between witch and boo
        self.x = self.witch.x + (self.game.boo.x - self.witch.x) * (self.len / self.total)
        self.y = self.witch.y + (self.game.boo.y - self.witch.y) * (self.len / self.total)

    def affected_by_potion(self):
        # rng
        potion_effect = random.randint(0, len(self.potion_effects) - 1)
        self.game.boo.affected_by_potion = time.time()
        if potion_effect == 0:
            self.game.boo.speed = 1.5
            self.game.boo.new_debuff = True
            debuff = Debuff(self.game, len(self.game.boo.debuffs), "speed")
            self.game.boo.debuffs.append(debuff)
        elif potion_effect == 1:
            self.game.boo.speed = 0.25
            self.game.boo.new_debuff = True
            debuff = Debuff(self.game, len(self.game.boo.debuffs), "slowed")
            self.game.boo.debuffs.append(debuff)
        elif potion_effect == 2:
            self.game.boo.stunned = True
            self.game.boo.stun_timer = time.time()
            debuff = Debuff(self.game, len(self.game.boo.debuffs), "stunned")
            self.game.boo.debuffs.append(debuff)
        elif potion_effect == 3:
            self.game.reverse_keybinds()
            debuff = Debuff(self.game, len(self.game.boo.debuffs), "reversed")
            self.game.boo.debuffs.append(debuff)
        elif potion_effect == 4:
            Blackout(game=self.game)
            debuff = Debuff(self.game, len(self.game.boo.debuffs), "blackout")
            self.game.boo.debuffs.append(debuff)


class Blackout(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)
        game.blackout_sprites.add(self)

        self.game = game
        self.start_time = time.time()

    def draw(self, frame_count):
        if self.game.boo:
            pygame.draw.circle(self.game.screen, (0,0,0), (self.game.boo.x+8, self.game.boo.y+8), 24+240, 240)
        else:
            self.game.blackout_sprites.remove(self)
            self.game.all_sprites.remove(self)

    def update(self):
        if time.time() - self.start_time > 3:
            self.game.blackout_sprites.remove(self)
            self.game.all_sprites.remove(self)

            if self.game.boo:
                for debuff in self.game.boo.debuffs:
                    if debuff.prop == "blackout":
                        debuff.delete_sprite()


class Barrier(pygame.sprite.Sprite):
    def __init__(self, game, x, y, log = False, tree = False):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)
        game.barrier_sprites.add(self)

        self.game = game
        self.x = x+1
        self.y = y+1
        if log:
            self.image = pygame.image.load("assets/barriers/log.png")
            self.width = 30
            self.height = 14
        elif tree:
            self.image = pygame.image.load("assets/barriers/tree.png")
            self.width = 30
            self.height = 30
        else:
            self.image = pygame.image.load("assets/barriers/barrier.png")
            self.width = 14
            self.height = 14

    def draw(self, frame_count):
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

        self.speed = 1
        self.up = True
        self.frames_left = 10

        self.affected_by_potion = False
        self.stunned = False
        self.stun_timer = 0
        self.stun_timeout = 2
        self.debuffs = [] # "stunned", "slowed", "reversed", "speed", "blackout"

        self.debuff_timer = 0
        self.debuff_timeout = 10
        self.new_debuff = False

        self.flash_frames = 40

        self.images = {
            "left": pygame.image.load("assets/boo/left.png"),
            "right": pygame.image.load("assets/boo/right.png"),
            "up": pygame.image.load("assets/boo/up.png"),
            "down": pygame.image.load("assets/boo/down.png"),
        }
        self.images_inverted = {
            "left": pygame.image.load("assets/boo/left_inv.png"),
            "right": pygame.image.load("assets/boo/right_inv.png"),
            "up": pygame.image.load("assets/boo/up_inv.png"),
            "down": pygame.image.load("assets/boo/down_inv.png"),
        }
        self.images_stunned = {
            "stun1": pygame.image.load("assets/boo/stun_1.png"),
            "stun2": pygame.image.load("assets/boo/stun_2.png"),
        }

    def draw(self, frame_count):
        self.flash_frames -= 1
        if self.affected_by_potion != False and time.time() - self.affected_by_potion < 2 and self.flash_frames > 20:
            if self.stunned:
                boo = self.images_stunned["stun1"]
            else:
                boo = self.images_inverted[self.moving]
            self.game.screen.blit(boo, (self.x, self.y))
        elif self.affected_by_potion != False and time.time() - self.affected_by_potion < 2:
            if self.stunned:
                boo = self.images_stunned["stun2"]
            else:
                boo = self.images[self.moving]
            self.game.screen.blit(boo, (self.x, self.y))
        else:
            self.affected_by_potion = False
            boo = self.images[self.moving]
            self.game.screen.blit(boo, (self.x, self.y))

        if self.flash_frames <= 0:
            self.flash_frames = 40

    def concat(self, a, b, c):
        yield from a
        yield from b
        yield from c

    def move(self, keys):
        x_delta = 0
        y_delta = 0

        if keys[self.game.keybinds["LEFT_KEY"][0]] or keys[self.game.keybinds["LEFT_KEY"][1]]:
            x_delta = -self.speed
            self.moving = "left"
        if keys[self.game.keybinds["RIGHT_KEY"][0]] or keys[self.game.keybinds["RIGHT_KEY"][1]]:
            x_delta = self.speed
            self.moving = "right"
        if keys[self.game.keybinds["UP_KEY"][0]] or keys[self.game.keybinds["UP_KEY"][1]]:
            y_delta = -self.speed
            self.moving = "up"
        if keys[self.game.keybinds["DOWN_KEY"][0]] or keys[self.game.keybinds["DOWN_KEY"][1]]:
            y_delta = self.speed
            self.moving = "down"

        new_x = self.x + x_delta
        new_y = self.y + y_delta

        # Check if boo hit a wall
        for barrier in self.concat(self.game.barrier_sprites, self.game.kid_sprites, self.game.uncaptured_key_sprites):
            check_x = lambda x: barrier.x < x < barrier.x+barrier.width
            check_y = lambda y: barrier.y < y < barrier.y+barrier.height

            in_x_axis = lambda x: check_x(x) or check_x(x+self.width) or check_x(new_x+self.width/2)
            in_y_axis = lambda y: check_y(y) or check_y(y+self.height) or check_y(new_y+self.height/2)

            if in_y_axis(new_y) and in_x_axis(new_x):
                if hasattr(barrier, "door") and len(self.game.uncaptured_key_sprites) == 0: # DOOR
                    self.game.level_completed()
                    x_delta = 0
                    y_delta = 0
                elif isinstance(barrier, Kid):
                    self.game.restart_level()
                elif isinstance(barrier, Key):
                    self.game.captured_key_sprites.add(barrier)
                    self.game.all_sprites.remove(barrier)
                    self.game.uncaptured_key_sprites.remove(barrier)
                    self.keys.append(barrier)
                else:

                    if new_x+self.width-2 <= barrier.x <= new_x+self.width and in_y_axis(self.y):
                        x_delta = 0
                    if new_x <= barrier.x + barrier.width <= new_x+2 and in_y_axis(self.y):
                        x_delta = 0
                    if new_y+self.height-2 <= barrier.y <= new_y+self.height and in_x_axis(self.x):
                        y_delta = 0
                    if new_y <= barrier.y + barrier.height <= new_y+2 and in_x_axis(self.x):
                        y_delta = 0

                    new_x = self.x + x_delta
                    new_y = self.y + y_delta

        # Check that boo doesn't escape his container
        if new_x < 8 or new_x+self.width > 240-8:
            x_delta = 0
        if new_y < 10 or new_y+self.height > 180-10:
            y_delta = 0

        if self.new_debuff:
            self.debuff_timer += 1/60
            if self.debuff_timer >= self.debuff_timeout:
                self.debuff_timer = 0
                self.new_debuff = False
                for debuff in self.debuffs:
                    if debuff.prop == "slowed" or debuff.prop == "speed":
                        debuff.delete_sprite()
                self.speed = 1
        if self.stunned:
            if time.time() - self.stun_timer > self.stun_timeout:
                for debuff in self.debuffs:
                    if debuff.prop == "stunned":
                        debuff.delete_sprite()
                self.stunned = False
            else:
                return

        self.x += x_delta
        self.y += y_delta


class BatCompanion(pygame.sprite.Sprite):
    def __init__(self, game, parent):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)
        self.game = game

        self.images = [
            pygame.image.load("assets/bat/1.png"),
            pygame.image.load("assets/bat/2.png"),
            pygame.image.load("assets/bat/3.png")
        ]
        self.parent = parent
        self.width = 10
        self.height = 8
        self.x = self.parent.x - self.width - 3
        self.y = self.parent.y - self.height - 3
        self.max_displacement = 8


    def update(self):
        target_x = self.parent.x - self.width - 3
        target_y = self.parent.y - self.height - 3

        if abs((target_x - self.x)) > self.max_displacement:
            x_dir = (target_x - self.x) / abs((target_x - self.x))
            self.x += 0.3 * x_dir

        if abs((target_y - self.y)) > self.max_displacement:
            y_dir = (target_y - self.y) / abs((target_y - self.y))
            self.y += 0.3 * y_dir


    def draw(self, frame_count):
        image = self.images[math.floor(frame_count / 10) % len(self.images)]
        self.game.screen.blit(image, (self.x, self.y))


class LeaderboardContent(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)
        self.game = game

        with open("scores.json") as scores_json:
            self.leaderboard = json.load(scores_json)
            self.leaderboard = self.leaderboard[:8]
        self.number_font = pygame.font.Font("assets/font.ttf", 10)

    def update(self):
        pass

    def draw(self, frame_count):
        screen = self.game.screen

        for i, player in enumerate(self.leaderboard):
            name = player["name"]
            time = player["time"]

            text = self.number_font.render(f"{time}s - ", True, BUTTON_TEXT_COLOUR)
            text_rect = text.get_rect(topleft = (30, 55 + 11*i))
            screen.blit(text, text_rect)

            text = self.number_font.render(name[:12], True, BUTTON_TEXT_COLOUR)
            text_rect = text.get_rect(topleft = (30 + text_rect.width, 55 + 11*i))
            screen.blit(text, text_rect)


class CutSceneContent(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)
        self.game = game

        self.images = [
            pygame.image.load("assets/cutscene/pre1.png"),
            pygame.image.load("assets/cutscene/pre2.png"),
            pygame.image.load("assets/cutscene/pre3.png"),
            pygame.image.load("assets/cutscene/pre4.png"),
            pygame.image.load("assets/cutscene/pre5.png"),
            pygame.image.load("assets/cutscene/pre6.png"),
            pygame.image.load("assets/cutscene/1.png"),
            pygame.image.load("assets/cutscene/2.png"),
            pygame.image.load("assets/cutscene/3.png"),
            pygame.image.load("assets/cutscene/4.png"),
            pygame.image.load("assets/cutscene/5.png"),
            pygame.image.load("assets/cutscene/6.png"),
        ]
        self.timeout = 30
        self.count = 0
        self.starting_frame_count = -1

    def draw(self, frame_count):
        if self.starting_frame_count == -1:
            self.starting_frame_count = frame_count
        if self.count < 5:
            self.timeout = 30
        elif self.count == 5:
            self.timeout = 180
        elif self.count == 6:
            self.timeout = 240
        elif self.count <  10:
            self.timeout = 720
        else:
            self.timeout = 540
        if frame_count < self.starting_frame_count and frame_count > self.timeout:
            self.starting_frame_count = frame_count
            self.count += 1
        elif frame_count - self.starting_frame_count > self.timeout:
            self.starting_frame_count = frame_count
            self.count += 1

        if self.count >= len(self.images):
            self.game.all_sprites.remove(self)
            self.game.cutscene_content = None
            self.game.start_game(None, None, self.game)
            return

        self.game.screen.blit(self.images[self.count], (0, 0))


class Key(pygame.sprite.Sprite):
    def __init__(self, game, x, y, keyType):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)
        game.uncaptured_key_sprites.add(self)

        self.game = game
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16

        self.keys = [
            pygame.image.load("assets/keys/1.png"),
            pygame.image.load("assets/keys/2.png"),
            pygame.image.load("assets/keys/3.png"),
        ]

        self.keyType = keyType

    def draw(self, frame_count):
        self.game.screen.blit(self.keys[self.keyType], (self.x, self.y))


class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)
        game.barrier_sprites.add(self)

        self.game = game
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16

        self.door = True

        self.image = pygame.image.load("assets/door.png")
        self.under = pygame.image.load("assets/under_door.png")

    def update(self):
        pass

    def draw(self, frame_count):
        self.game.screen.blit(self.image, (self.x, self.y))
        self.game.screen.blit(self.under, (self.x, self.y + self.height))


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

    def draw(self, frame_count):
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


class TextInput(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, text, callback):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)

        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tooltip = text
        self.text = ""
        self.callback = callback
        self.font = pygame.font.Font("assets/font.ttf", height-10)

        self.state = "none" # "none", "active"

    def draw(self, frame_count):
        screen = self.game.screen
        if self.state == "none":
            pygame.draw.rect(screen, BUTTON_OUTLINE_0, [self.x,self.y+1,self.width,self.height-2])
            pygame.draw.rect(screen, BUTTON_OUTLINE_0, [self.x+1,self.y, self.width-2,self.height])
            pygame.draw.rect(screen, BUTTON_OUTLINE_1, [self.x+1,self.y+1, self.width-2,self.height-2])

            pygame.draw.rect(screen, INPUT_MAIN, [self.x+2,self.y+2,self.width-4,self.height-4])

        elif self.state == "active":
            pygame.draw.rect(screen, BUTTON_PRESSED_OUTLINE_0, [self.x+1,self.y+2,self.width-2,self.height-4])
            pygame.draw.rect(screen, BUTTON_PRESSED_OUTLINE_0, [self.x+2,self.y+1, self.width-4,self.height-2])
            pygame.draw.rect(screen, BUTTON_PRESSED_OUTLINE_1, [self.x+2,self.y+2, self.width-4,self.height-4])

            pygame.draw.rect(screen, BUTTON_PRESSED_MAIN, [self.x+3,self.y+3,self.width-6,self.height-6])

        text = self.font.render(self.tooltip, True, BUTTON_TEXT_COLOUR)
        text_rect_tt = text.get_rect(center=(self.x+self.width/2, self.y+self.height/2))
        screen.blit(text, (self.x + 4, self.y + 4))

        text = self.font.render(self.text, True, BUTTON_TEXT_COLOUR)
        text_rect = text.get_rect(center=(self.x+self.width/2, self.y+self.height/2))
        screen.blit(text, (text_rect_tt.width + self.x + 4, self.y + 4))

    def check_state(self, event):
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x <= mouse[0] <= self.x+self.width and self.y <= mouse[1] <= self.y+self.height:
                self.state = "active"
            else:
                self.state = "none"

        if event.type == pygame.KEYDOWN and self.state == "active":
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.callback(self.text)
                self.state = "none"
            else:
                self.text += event.unicode


class TextBox(pygame.sprite.Sprite):
    def __init__(self, game, x, y, font_size, text, colour=BUTTON_TEXT_COLOUR):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)

        self.game = game
        self.x = x
        self.y = y
        self.height = 20
        self.width = 50
        self.text = text
        self.colour = colour

        self.font = pygame.font.Font("assets/font.ttf", font_size)

    def draw(self, frame_count):
        text = self.font.render(self.text, True, self.colour)
        text_rect = text.get_rect(center=(self.x+self.width/2, self.y+self.height/2))
        self.game.screen.blit(text, (self.x, self.y))


class Prop(pygame.sprite.Sprite):
    def __init__(self, game, x, y, prop):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)

        self.game = game
        self.x = x
        self.y = y

        self.image = pygame.image.load(f"assets/props/{prop}.png")

    def draw(self, frame_count):
        self.game.screen.blit(self.image, (self.x, self.y))


class Debuff(pygame.sprite.Sprite):
    def __init__(self, game, index, prop):
        pygame.sprite.Sprite.__init__(self)
        game.all_sprites.add(self)
        game.debuff_sprites.add(self)

        self.index = index

        self.game = game
        self.x = 35 + 8 * self.index
        self.y = 1
        self.prop = prop

        self.image = pygame.image.load(f"assets/debuffs/{self.prop}.png")

    def draw(self, frame_count):
        if self.game.boo and self in self.game.boo.debuffs:
            self.index = self.game.boo.debuffs.index(self)
        elif self.game.boo:
            print(self.game.boo.debuffs)
        self.x = 35 + 8 * self.index
        self.game.screen.blit(self.image, (self.x, self.y))

    def delete_sprite(self):
        if self.game.boo and self in self.game.boo.debuffs:
            self.game.boo.debuffs.remove(self)
        self.game.debuff_sprites.remove(self)
        self.game.all_sprites.remove(self)
        self.kill()


if __name__ == "__main__":
    game = Game(240, 180)
    game.start()
