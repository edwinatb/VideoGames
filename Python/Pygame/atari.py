'''
    Date: 27-oct-2021
    Description: Video juego de atari.
    Author: Edwin Andrés Timaná Burbano

'''

#librerias importadas

import time
import pygame
import sys
import os
from typing import Text


pygame.init()

#############################

#Classes

#############################


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img_ball=pygame.image.load('images/bolita.png')
        self.rect=self.img_ball.get_rect()
        self.rect.centerx=WIDTH / 2
        self.rect.centery=HEIGHT / 2

        #A mayor amplitud rebote afecta el eje Y y a menor amplitud rebote afecta el eje X
        self.speed=[5,5] #[Param1->Veloc del mov. /Param2 -> Amplitud del mov. ] -> Concepto de las físicas

    def pibot(self):

        #Validate Y !¡

        if self.rect.bottom >= HEIGHT or self.rect.top <=0:
            self.speed[1] = -self.speed[1]

        #Validate x <- X ->

        elif self.rect.right >= WIDTH or self.rect.left <=0:
            self.speed[0] = -self.speed[0]

        self.rect.move_ip(self.speed)

##############################################################################


class Bar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img_bar=pygame.image.load('images/paleta.png')
        self.rect=self.img_bar.get_rect()
        self.rect.midbottom=(WIDTH/2,HEIGHT-10)
        self.speed=[0,0]


    def slide(self,listener):
        if listener.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed=[-5,0]
        elif listener.key == pygame.K_RIGHT and self.rect.right < WIDTH:
            self.speed = [5,0]
        else:
            self.speed=[0,0]
        self.rect.move_ip(self.speed)


##################################################################


class Brick(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('images/ladrillo.png')
        self.rect=self.image.get_rect()
        self.rect.topleft=position


class Wall(pygame.sprite.Group):
    def __init__(self,totalBricks):
        pygame.sprite.Group.__init__(self)
        posX=0
        posY=10


        for i in range(totalBricks):
            brick=Brick((posX,posY))
            self.add(brick)
            

            posX+=brick.rect.width
            if posX >= WIDTH:
                posX=0
                posY+=brick.rect.height


def game_over():
    msg = 'Perdiste. Vuelve a intentarlo'
    text_color=(130, 190, 67)
    text_style = pygame.font.SysFont('Arial',40) #(tipo de letra, tamaño)
    txt_screen = text_style.render(msg, True, text_color)
    txt_screen_rect = txt_screen.get_rect()
    txt_screen_rect.center = [WIDTH/2,HEIGHT/2]
    screen.blit(txt_screen,txt_screen_rect)
    pygame.display.flip()
    time.sleep(5)
    #sys.exit()


def set_score():
    text_color=(130, 190, 67)
    text_style = pygame.font.SysFont('Arial',40) #(tipo de letra, tamaño)
    txt_screen = text_style.render(str(score).zfill(3), True, text_color)
    txt_screen_rect = txt_screen.get_rect()
    txt_screen_rect.topleft = [1,400]
    screen.blit(txt_screen,txt_screen_rect)


def set_lives():
    label = "Vidas: "
    text_color=(130, 190, 67)
    text_style = pygame.font.SysFont('Arial',35)
    text = label + str(player_lives).zfill(1)
    txt_screen = text_style.render(text, True, text_color)
    txt_screen_rect = txt_screen.get_rect()
    txt_screen_rect.topleft = [500,400]
    screen.blit(txt_screen,txt_screen_rect)


#######################################################


#General settings

WIDTH=640
HEIGHT=480
BG_COLOR=(52,102,95) #(R,G,B)


screen=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Atari')
icon=pygame.image.load('images/main_icon.png')
pygame.display.set_icon(icon)


game_clock=pygame.time.Clock()  #Reloj del juego
pygame.key.set_repeat(20)


print("---- MENÚ NIVEL DE JUEGO----")
print("---- 1. NIVEL NORMAL")
print("---- 2. NIVEL INTERMEDIO")
print("---- 3. NIVEL AVANZADO")
print("---- 4. SALIR")


status = True
while status:
    opt = int(input("Seleccione el nivel: "))
    if opt >= 1 and opt <=4:
        status = False


if opt==1:
    ladrillos=20

elif opt==2:
    ladrillos=100

elif opt==3:
    ladrillos=200

elif opt==4:
    print("Has salido del juego.")
    time.sleep(4)
    sys.exit()

else:
    print("Opción invalida.")
    time.sleep(4)
    sys.exit()


player_lives = 3
score = 0
player=Bar()
ball=Ball()
wall=Wall(ladrillos)


#Loop (Revisión cíclica de los eventos) => Listener

while True:
    game_clock.tick(60)
    for event in pygame.event.get():

        #Verificar si se presiono el botón X de la ventana

        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

        #Verificar si el jugador presionó tecla del teclado

        elif event.type==pygame.KEYDOWN:
            player.slide(event)

    #Call pibot
    ball.pibot()

    #Collision between bar and ball
    #Cambio de trayectoria de la bola

    if pygame.sprite.collide_rect(ball,player): #PLayer is the bar
        ball.speed[1] = -ball.speed[1]

    #Collision between ball and wall (Bricks) Destroy bricks

    elements = pygame.sprite.spritecollide(ball,wall,False,collided=None)
    if elements: #Mientras existan ladrillos para chocar
        brick = elements[0]
        centX = ball.rect.centerx

        if centX < brick.rect.left or centX > brick.rect.right:
            
            #Afectamos velocidad
            ball.speed[0] = -ball.speed[0]
        else:
            #Afectamos trayectoria
            ball.speed[1] = -ball.speed[1]
        wall.remove(brick)
        score += 1

    #Call the function game over
    '''if ball.rect.bottom >= HEIGHT:
        game_over()'''

    #Restar vidas        
    if ball.rect.bottom >= HEIGHT:
        player_lives -= 1

    if player_lives == 0:
        game_over()

    #Set background color
    screen.fill(BG_COLOR)
    set_score()
    set_lives()
    
    #Draw de la ball
    screen.blit(ball.img_ball,ball.rect)
    #Draw de la bar
    screen.blit(player.img_bar,player.rect)
    #Draw wall
    wall.draw(screen)
    pygame.display.flip() #Refresh de elementos en screen