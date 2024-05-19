import pygame
from pygame import mixer
import random
import time
from tkinter import messagebox
import sys

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

pygame.init()

s_height = 1000
s_width = 800

screen = pygame.display.set_mode((s_height,s_width))
pygame.display.set_caption('Astro Clash')

font_path = r'F:\Projects\Pygame\assets\PressStart2P-Regular.ttf'
## adasda
font30 = pygame.font.Font(font_path, 30)
font40 = pygame.font.Font(font_path, 40)

pygame_icon = pygame.image.load(r'F:\Projects\Pygame\assets\icon.png')
pygame.display.set_icon(pygame_icon)

laser_fx = pygame.mixer.Sound(r'F:\Projects\Pygame\assets\blaster.mp3')
laser_fx.set_volume(0.4)

game_over_fx = pygame.mixer.Sound(r'F:\Projects\Pygame\assets\game_over.mp3')
game_over_fx.set_volume(1)

blast_fx= pygame.mixer.Sound(r'F:\Projects\Pygame\assets\blast.mp3')
blast_fx.set_volume(0.125)

countdown_fx= pygame.mixer.Sound(r'F:\Projects\Pygame\assets\countdown.mp3')
countdown_fx.set_volume(0.125)


background = pygame.image.load(r'F:\Projects\Pygame\assets\space_bg.png')

clock = pygame.time.Clock()
fps = 60

countdown = 3
points = 0
last_count = pygame.time.get_ticks()


red = (255,0 ,0)
green = (0, 255, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)

def reset_game():
    global game_over, spacecraft, asteroid_group, blast_group ,start_time ,countdown, points
    game_over = False
    spacecraft.rect.center = [500, 400]
    asteroid_group.empty()
    blast_group.empty()
    laser_group.empty()
    start_time = time.time() + 2
    countdown = 4
    points = 0
   
    pygame.time.delay(2000)
    

def draw_bg():
    screen.blit(background, (0, 0))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class Spacecraft(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load(r'F:\Projects\Pygame\assets\spacecraft.png')
        self.image = pygame.transform.scale(self.original_image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.recharge = pygame.time.get_ticks()
    
    def update(self):
        if not game_over:
            speed = 5
            cooldown = 400
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= speed
            if key[pygame.K_RIGHT] and self.rect.right < 1000:
                self.rect.x += speed
            if key[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= speed
            if key[pygame.K_DOWN] and self.rect.bottom < 800:
                self.rect.y += speed

            
            timer = pygame.time.get_ticks()

            if key[pygame.K_SPACE] and timer - self.recharge > cooldown :
                laser_fx.play()
                laser = Lasers((self.rect.centerx)+17, (self.rect.centery)-20)
                laser_group.add(laser)
                self.recharge = timer            
            
            self.mask = pygame.mask.from_surface(self.image)

class Lasers(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load(r'F:\Projects\Pygame\assets\laser.png')
        self.image = pygame.transform.scale(self.original_image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 7
        global points
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, asteroid_group, True , pygame.sprite.collide_mask):
            
            self.kill()
            blast_fx.play()           
            points += 1
            blast = Blast(self.rect.centerx - 22, self.rect.centery - 30, 2)
            blast_group.add(blast)


class Asteroids(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load(r'F:\Projects\Pygame\assets\asteroid.png')
        self.image = pygame.transform.scale(self.original_image, (70,70))
        self.rect = self.image.get_rect()
        
        self.reset_pos()
    def reset_pos(self):
        
        self.rect.x = random.randint(0, 1000)
        self.rect.y = random.randint(-100,70)

    def update(self):
        global game_over
        if not game_over:
            self.rect.y += 2
            if self.rect.top > 1000:
                self.reset_pos()
            if pygame.sprite.spritecollide(self, spacecraft_group, False, pygame.sprite.collide_mask):
                self.kill()
                game_over_fx.play()
                game_over = True
        

        self.mask = pygame.mask.from_surface(self.image)
        

class Blast(pygame.sprite.Sprite):
    def __init__(self, x ,y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,6):
            img = pygame.image.load(f'F:\Projects\Pygame\\assets\exp{num}.png')
            if size == 1:
                img = pygame.transform.scale(img, (20,20))
            if size == 2:
                img = pygame.transform.scale(img, (40,40))
            if size == 3:
                img = pygame.transform.scale(img, (150,150))

            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index] 
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        exp_speed = 3
        self.counter += 1

        if self.counter >= exp_speed and self.index < len(self.images) - 1:
            self.counter = 1
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= exp_speed:
            self.kill()


spacecraft_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
blast_group = pygame.sprite.Group()

spacecraft = Spacecraft(500,400)
asteroid = Asteroids()


spacecraft_group.add(spacecraft)
asteroid_group.add(asteroid)

spawn_timer = 0
spawn_frequency = 30
game_over = False
start_time = time.time()

run = True

while run:


    
    clock.tick(fps)
    
    draw_bg()
    
    blast_group.update()

    spacecraft_group.draw(screen)
    laser_group.draw(screen)
    asteroid_group.draw(screen)
    blast_group.draw(screen)
    

    if countdown == 0:

        
        if game_over:
            draw_text('GAME OVER', font40, white, 330, 350)
            draw_text('Press R to retry', font30, white, 270, 420)
            
             
        
        else:
            spawn_timer += 1
            if spawn_timer >= spawn_frequency:
                asteroid = Asteroids()
                asteroid.reset_pos()
                asteroid_group.add(asteroid)
                spawn_timer = 0

        
            spacecraft.update()
            laser_group.update()
            asteroid_group.update()
            elapsed_time = int(time.time() - start_time)
            draw_text(f'Timer: {elapsed_time - 3}', font30, white, 10, 10)
            draw_text(f'Points: {points}', font30, white, 700, 10)
            

    if countdown > 0:
            draw_text('ASTRO CLASH', font40, white ,280,220)
            countdown_fx.play()
            draw_text(str(countdown), font30, white ,485,280)
            count_timer = pygame.time.get_ticks()
            if count_timer - last_count > 1000:
                countdown -= 1
                last_count = count_timer
                    
                    
   
    
    for event in pygame.event.get():
       
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            reset_game()

        
    
    pygame.display.update()

pygame.quit()