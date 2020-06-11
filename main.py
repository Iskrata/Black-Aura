import pygame 
import sys
import random

mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()

pygame.display.set_caption("Black Aura")

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

bg_im = pygame.image.load("data\\images\\ms_bg.png")
bg_im_inv = pygame.image.load("data\\images\\ms_bg_inv.png")
bg_es = pygame.image.load("data\\images\\es_bg.png")

font = pygame.font.Font("data\\fonts\\MonospaceBold.ttf", 40)

black = (0, 0, 0)
white = (255, 255, 255)

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
    click = False
    frame = False
    while True:
        if pygame.time.get_ticks() % 300 == 0 or frame == True:
            if not frame:
                frame = True
                tm = pygame.time.get_ticks()
            if pygame.time.get_ticks() > tm+random.randint(200,1000):
                frame = False
            screen.blit(bg_im_inv, (0, 0))
            button = pygame.Rect(draw_text('[Start Game]', font, black, screen, 0, 600, True))
        else:
            screen.blit(bg_im, (0, 0))
            button = pygame.Rect(draw_text('[Start Game]', font, white, screen, 0, 600, True))

        mx, my = pygame.mouse.get_pos(475, 600, 200, 50)


        if button.collidepoint((mx, my)):
            if click:
                game()
            else:
                pygame.draw.rect(screen, (255, 255, 255), button) 
                draw_text('[Start Game]', font, (0, 0, 0), screen, 0, 600, True)


        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

def end_screen(points):
    screen.fill(black)

class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isBoost = False
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, screen):
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, white, self.hitbox)

class Obstacle():
    def __init__(self):
        self.type = random.randint(1, 4)
        self.x, self.y = self.dire()
        self.width = 10
        self.height = 10
        self.vel = 5  
        self.hitbox = (self.x, self.y, self.width, self.height)

    def dire(self):
        if self.type == 1:
            return 0, random.randint(0, SCREEN_HEIGHT)
        if self.type == 2:
            return random.randint(0, SCREEN_WIDTH), 0
        if self.type == 3:
            return SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT)
        if self.type == 4:
            return random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT
    def move(self):
        if self.type == 1:
            self.x += self.vel
        if self.type == 2:
            self.y += self.vel
        if self.type == 3:
            self.x -= self.vel
        if self.type == 4:
            self.y -= self.vel
    def draw(self, screen):
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, white, self.hitbox)


def game():
    running = True
    man = Player((SCREEN_WIDTH/2)-50, SCREEN_HEIGHT/2, 100, 100)
    enemies = []
    points = 0

    def redraw_win():
        screen.fill((50, 50, 50))
        for e in enemies:
            e.draw(screen)
        man.draw(screen)

        points_label = font.render(f"Points: {points}", 1, white)
        screen.blit(points_label, (SCREEN_WIDTH - points_label.get_width() - 10, 10))

        pygame.display.update()


    while running:

        redraw_win()

        keys = pygame.key.get_pressed()

        if len(enemies) == 0:
            points += 1
            for _ in range(points*2):
                enemy = Obstacle()
                enemies.append(enemy)
        
        for e in enemies[:]:
            e.move()
            r = pygame.Rect(man.hitbox)
            if r.collidepoint(e.x, e.y):
                running = False
            if not(e.x < SCREEN_WIDTH+e.width and e.x > 0-e.width and e.y < SCREEN_HEIGHT+e.height and e.y > 0-e.height):
                enemies.remove(e)

        if keys[pygame.K_LEFT] and man.x > man.vel:
            man.x -= man.vel
        if keys[pygame.K_RIGHT] and man.x < SCREEN_WIDTH - man.width - man.vel:
            man.x += man.vel
        if keys[pygame.K_UP] and man.y > man.vel:
            man.y -= man.vel
        if keys[pygame.K_DOWN] and man.y < SCREEN_HEIGHT - man.height - man.vel:
            man.y += man.vel
        if keys[pygame.K_SPACE]:
            man.isBoost = True
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        mainClock.tick(60)

    end_screen(points)



main_menu()

# TODO 
# Score count on the screen
# Boost
# Other power up (Ex. Slow time)
# Loose screen
# Make fency bg
