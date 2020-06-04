import pygame, sys
#import pygame_menu

mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

background_image = pygame.image.load("data\\images\\ms_bg.png")

font =  pygame.font.SysFont(None, 60)
font = pygame.font.Font("data\\fonts\\MonospaceBold.ttf", 40)

def draw_text(text, font, color, surface, x, y, center):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if center:
        textrect.topleft = ((SCREEN_WIDTH/2)-(textrect.width/2), y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    return (SCREEN_WIDTH/2)-(textrect.width/2), y, textrect.width, textrect.height

def main_menu():
    while True:
        screen.blit(background_image, (0, 0))
        button = pygame.Rect(draw_text('[Start Game]', font, (255, 255, 255), screen, 0, 600, True))

        mx, my = pygame.mouse.get_pos(475, 600, 200, 50)

        #button = pygame.Rect(475, 600, 200, 100)

        if button.collidepoint((mx, my)):
            if click:
                game()
        #pygame.draw.rect(screen, (255, 0, 0), button) 


        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

def game():
    screen.fill((155, 155, 155))
    running = True
    while running:
        pygame.display.update()
        mainClock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False



running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    main_menu()
    pygame.display.flip()

pygame.quit()