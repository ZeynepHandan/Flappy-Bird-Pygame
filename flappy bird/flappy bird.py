import pygame
import sys
import random
import time 
from PIL import Image
import os

pygame.init()
pygame.mixer.init()
music=pygame.mixer.music.load("Daft Punk- Derezzed (OFFICIAL TRACK)(FULL SONG)(HQ)(2010)TRON SOUNDTRACK.mp3")
pygame.mixer.music.play(-1)

clock=pygame.time.Clock()
window_size=(900,502)
window=pygame.display.set_mode(window_size)
pygame.display.set_caption('Flappy Bird Game')

welcome_img=pygame.image.load("flappy-bird-logo.png")
welcome_img=pygame.transform.scale(welcome_img,(300,100))
start_button=pygame.image.load("Start-button-sprite.png")
start_button=pygame.transform.scale(start_button,(100,40))
start_rect=start_button.get_rect(topleft=(400,180))
background_img=pygame.image.load('background.png')
ground_image=pygame.image.load('ground.png')
ground_height=52
ground_image=pygame.transform.scale(ground_image,(window_size[0],ground_height))
ground_y=window_size[1]-ground_height
top_pipe_img=pygame.image.load("top_pipe.png")
bottom_pipe_img=pygame.image.load("bottom_pipe.png")
game_over_img=pygame.image.load("gameoverimg.png")
game_over_img=pygame.transform.scale(game_over_img,(420,180))
jump_sound=pygame.mixer.Sound("flappy_whoosh-43099.mp3")
font=pygame.font.Font("PressStart2P-Regular.ttf ",35)
hit_sound=pygame.mixer.Sound("assets_audio_hit.ogg")
background1_img=pygame.image.load("background1.jpg")
background1_img=pygame.transform.scale(background1_img,(900,502))
background2_img=pygame.image.load("background2.jpg")
background2_img=pygame.transform.scale(background2_img,(900,502))
restart_button=pygame.image.load("362223.png")
restart_button=pygame.transform.scale(restart_button,(90,30))
restart_rect=restart_button.get_rect(topleft=(295,285))
exit_button=pygame.image.load("exit.jpg")
exit_button=pygame.transform.scale(exit_button,(60,30))
exit_rect=exit_button.get_rect(topleft=(430,285))
menu=pygame.image.load("hqdefault.jpg")
menu=pygame.transform.scale(menu,(70,30))
menu_rect=menu.get_rect(topleft=(535,285))
bg3=pygame.image.load("bg3.png")
bg3=pygame.transform.scale(bg3,(900,502))
bg4=pygame.image.load("bg4.png")
bg4=pygame.transform.scale(bg4,(900,502))
bg5=pygame.image.load("bg5.png")
bg5=pygame.transform.scale(bg5,(900,502))
bg6=pygame.image.load("bg6.jpg")
bg6=pygame.transform.scale(bg6,(900,502))
bird1= pygame.image.load("bird1.png").convert_alpha()
bird1= pygame.transform.scale(bird1, (40, 30))
bird2=pygame.image.load("bird2.png").convert_alpha()
bird2=pygame.transform.scale(bird2,(40,30))
bird3=pygame.image.load("bird3.png").convert_alpha()
bird3=pygame.transform.scale(bird3,(40,30))

def welcomeScreen():
    while True:
        window.blit(background_img,(0,0))
        window.blit(ground_image,(0,ground_y))
        window.blit(welcome_img,(300,50))
        window.blit(start_button,(400,180))
        window.blit(bird1,(420,270))
        a=pygame.transform.scale(top_pipe_img,(46,140))
        b=pygame.transform.scale(bottom_pipe_img,(46,140))
        window.blit(a,(120,0))
        window.blit(a,(720,0))
        window.blit(b,(120,312))
        window.blit(b,(720,312))
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    return
            if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
               pygame.quit()
               sys.exit()
welcomeScreen()

def game_over(score):
    gameover_screen=pygame.Rect(250,250,400,100)
    pygame.draw.rect(window,(238,232,170),gameover_screen,border_radius=20)
    pygame.draw.rect(window,(0,0,0),gameover_screen,3,border_radius=20)
    window.blit(game_over_img,(240,50))
    small_font=pygame.font.Font("PressStart2P-Regular.ttf",16)
    s_text=small_font.render(f"SCORE:{score}",True,(0,0,0))
    window.blit(s_text,(400,220))
    window.blit(restart_button,(295,285))
    window.blit(exit_button,(430,285))
    window.blit(menu,(535,285))
    pygame.display.update()
    hit_sound.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type==pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    mainGame()
                    return
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()
                if menu_rect.collidepoint(event.pos):
                    welcomeScreen()
                    return

def collision(bird_rect,pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe.top_rect.inflate(-2, -2)) or bird_rect.colliderect(pipe.bottom_rect.inflate(-2, -2)):
            return True
        if bird_rect.y <= 0 or bird_rect.y >= ground_y:
            if bird_rect.bottom == ground_y:
                y_velocity=0
                bird_rect.top=ground_y+30
            return True
    return False

def rotate_bird(bird_image,angle):
    return pygame.transform.rotate(bird_image,angle)

class PipePair:
    def __init__(self,gap):
        self.x=900
        self.gap=gap
        self.passed=False
        min_bottom_height=80
        max_top_height=window_size[1] - ground_height - self.gap - min_bottom_height
        self.top_height=random.randint(80 ,max_top_height)
        self.bottom_height=window_size[1] - ground_height - self.gap - self.top_height
        self.width=45

        self.top_image=pygame.transform.scale(top_pipe_img,(self.width,self.top_height))
        self.bottom_image=pygame.transform.scale(bottom_pipe_img,(self.width,self.bottom_height))

        self.top_rect=self.top_image.get_rect(topleft=(self.x,0))
        self.bottom_rect=self.bottom_image.get_rect(topleft=(self.x,window_size[1] - ground_height - self.bottom_height))


    def move(self,speed):
        self.x -= speed
        self.top_rect.x=self.x
        self.bottom_rect.x=self.x

    def draw(self,window):
        window.blit(self.top_image,(self.x,0))
        window.blit(self.bottom_image,(self.x,window_size[1] - ground_height - self.bottom_height))


class Score:
    def __init__(self):
        self.score=0
    def increase(self):
        self.score+=1
        return self.score

def mainGame():
    game_started=False
    player_score=Score()
    score=0
    bird_x=100
    bird_y=300
    pipe_gap=175
    pipes=[PipePair(pipe_gap)]
    running=True
    y_velocity=0
    gravity=0.008
    jump_strength=-1
    
    bird_image=bird1
    bird_rect=pygame.Rect(bird_x,bird_y,bird_image.get_width(),bird_image.get_height())
    bird_rect.y=bird_y
    bird_rect.x=bird_x

    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running= False
            
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE or event.key== pygame.K_UP:
                    if not game_started:
                        game_started=True
                    y_velocity=jump_strength
                    jump_sound.play()
        
        if game_started:
            y_velocity += gravity
            bird_y += y_velocity
            bird_rect.y=bird_y

        if 0 <= score <110:
            bird_image=bird1
        elif 110<= score <220:
            bird_image=bird2
        else:
            bird_image=bird3

        rotation_angle=min(50,max(-50,y_velocity*-10))

        if collision(bird_rect,pipes):
            game_over(player_score.score)

        if 0<=score<40:
            window.blit(background_img,(0,0))
        if 40<=score<90:
            window.blit(background1_img,(0,0))
        if 90<=score<150:
            window.blit(background2_img,(0,0))
        if 150<=score<220:
            window.blit(bg3,(0,0))
        if 220<=score<300:
            window.blit(bg4,(0,0))
        if 300<=score<400:
            window.blit(bg5,(0,0))
        if 400<=score:
            window.blit(bg6,(0,0))
        for pipe in pipes:
            if 0<=score<70:
                pipe.move(0.4)
            if 70<=score<130:
                pipe.move(0.5)
            if 130<=score<220:
                pipe.move(0.6)
            if 220<=score<300:
                pipe.move(0.7)
            if 300<=score:
                pipe.move(0.8)
            pipe.draw(window)
            if pipe.x + pipe.width < bird_x and not pipe.passed:
              score=player_score.increase()
              pipe.passed=True
        window.blit(ground_image,(0,ground_y))
        rotated_bird=rotate_bird(bird_image,rotation_angle)
        window.blit(rotated_bird,(bird_x,bird_y))
        scora=font.render(f"{score}",True,(255,255,255))
        window.blit(scora,(775,100))

        if pipes[-1].x <690:
            pipes.append(PipePair(pipe_gap))

        pipes=[pipe for pipe in pipes if pipe.x + pipe.width > 0]

        pygame.display.update()

mainGame()

pygame.display.flip()
clock.tick(30)

pygame.quit()

