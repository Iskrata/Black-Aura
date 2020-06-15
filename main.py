import pygame 
import sys
import random
import json

mainClock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption("Black Aura")

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

bg_im = pygame.image.load("data\\images\\ms_bg.png")
bg_im_inv = pygame.image.load("data\\images\\ms_bg_inv.png")
bg_es = pygame.image.load("data\\images\\es_bg.png")

font = pygame.font.Font("data\\fonts\\MonospaceBold.ttf", 40)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

physics = True

def draw_text(text, font, color, surface, x, y, is_centered):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if is_centered:
        textrect.topleft = (int((SCREEN_WIDTH/2)-(textrect.width/2)), y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    return int((SCREEN_WIDTH/2)-(textrect.width/2)), y, textrect.width, textrect.height

def main_menu():
    click = False
    frame = False
    global physics
    while True:
        if pygame.time.get_ticks() % 300 == 0 or frame == True:
            if not frame:
                frame = True
                tm = pygame.time.get_ticks()
            if pygame.time.get_ticks() > tm+random.randint(200,1000):
                frame = False
            screen.blit(bg_im_inv, (0, 0))
            button = pygame.Rect(draw_text('[Start Game]', font, BLACK, screen, 0, 600, True))
        else:
            screen.blit(bg_im, (0, 0))
            button = pygame.Rect(draw_text('[Start Game]', font, WHITE, screen, 0, 600, True))

        mx, my = pygame.mouse.get_pos()

        if not physics:
            button2 = pygame.Rect(draw_text('[Physics] = OFF', font, WHITE, screen, 0, 650, True))
        if physics:
            button2 = pygame.Rect(draw_text('[Physics] = ON', font, WHITE, screen, 0, 650, True))

        if button.collidepoint((mx, my)):
            if click:
                game()
            else:
                pygame.draw.rect(screen, WHITE, button) 
                draw_text('[Start Game]', font, BLACK, screen, 0, 600, True)

        if button2.collidepoint((mx, my)):
            if click:
                if physics:
                    physics = False
                else:
                    physics = True
            else:
                pygame.draw.rect(screen, WHITE, button2) 
                if not physics:
                    button2 = pygame.Rect(draw_text('[Physics] = OFF', font, BLACK, screen, 0, 650, True))
                if physics:
                    button2 = pygame.Rect(draw_text('[Physics] = ON', font, BLACK, screen, 0, 650, True))


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

    inEnd = True
    click = False
    while inEnd:
        screen.blit(bg_es, (0, 0))
        button = pygame.Rect(draw_text('[Main Menu]', font, WHITE, screen, 0, 650, True))
        pygame.Rect(draw_text(f'[Points] // {points}', font, WHITE, screen, 0, 600, True))

        mx, my = pygame.mouse.get_pos()

        if button.collidepoint((mx, my)):
            if click:
                inEnd = False
            else:
                pygame.draw.rect(screen, WHITE, button) 
                draw_text('[Main Menu]', font, BLACK, screen, 0, 650, True)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inEnd = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)
    
    main_menu()

class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velx = 0
        self.vely = 0
        self.isBoost = False
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, screen):
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, WHITE, self.hitbox)
        pygame.draw.rect(screen, (50, 50, 50), (self.x+25, self.y+25, self.width/2, self.height/2))

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
        pygame.draw.rect(screen, WHITE, self.hitbox)


def game():
    pygame.mixer.music.stop()
    pygame.mixer.music.load('data\\music\\ingame.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    global physics
    running = True
    man = Player((SCREEN_WIDTH/2)-50, SCREEN_HEIGHT/2, 100, 100)
    enemies = []
    points = 0

    def redraw_win():
        screen.fill((50, 50, 50))
        for e in enemies:
            e.draw(screen)
        man.draw(screen)

        points_label = font.render(f"Points: {points}", 1, WHITE)
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
            if r.collidepoint(e.x + e.width/2, e.y + e.height/2):
                pygame.mixer.music.stop()
                pygame.mixer.music.load('data\\music\\pop.mp3')
                pygame.mixer.music.play(1)
                running = False
            if not(e.x < SCREEN_WIDTH+e.width and e.x > 0-e.width and e.y < SCREEN_HEIGHT+e.height and e.y > 0-e.height):
                enemies.remove(e)

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            if physics:
                if man.velx > -7:
                    man.velx -= 0.2
            else:
                man.velx = -5
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            if physics:
                if man.velx  < 7:
                    man.velx += 0.2
            else: 
                man.velx = 5
        if (keys[pygame.K_UP] or keys[pygame.K_w]):
            if physics:
                if man.vely > -7:
                    man.vely -= 0.2
            else:
                man.vely = -5
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            if physics:
                if man.vely < 7:
                    man.vely += 0.2
            else:
                man.vely = 5
        if keys[pygame.K_SPACE]:
            man.isBoost = True

        if man.x + man.velx > 5 and man.x + 5 < SCREEN_WIDTH - man.width - man.velx and man.y + man.vely > 5 and man.y + 5 < SCREEN_HEIGHT - man.height - man.vely:
            man.x += man.velx
            man.y += man.vely
        else:
            man.velx = 0
            man.vely = 0

        if physics:
            if man.velx < 0:
                man.velx += 0.1
            if man.velx > 0:
                man.velx -= 0.1
            if man.vely < 0:
                man.vely += 0.1
            if man.vely > 0:
                man.vely -= 0.1
        else:
            man.velx = 0
            man.vely = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        mainClock.tick(60)

    end_screen(points)



main_menu()
