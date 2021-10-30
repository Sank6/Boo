import pygame

FRAMERATE = 60
GAMERUNNING = True

def loop():
    global GAMERUNNING
    
    while GAMERUNNING:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                GAMERUNNING = False



def main():
    (width, height) = (640, 480)
    screen = pygame.display.set_mode((width, height))
    pygame.display.flip()
    loop()


if __name__ == "__main__":
    main()
