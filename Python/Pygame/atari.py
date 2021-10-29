
'''
    Date: 27-Oct-2021
    Description: juego de atari
    Author: Edwin Andrés Timaná Burbano
'''

#librerias importadas

import time
import os
import pygame
import sys


pygame.init()

pygame.mixer.music.load("sonidos/sonic.mp3")
pygame.mixer.music.play(1)

#Sonidos del juego

caer = pygame.mixer.Sound("sonidos/caer.wav")
elimi = pygame.mixer.Sound("sonidos/elimi.wav")
terminado= pygame.mixer.Sound("sonidos/terminado.wav")


#############################################

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img_ball = pygame.image.load('images/bolita.png')
        self.rect = self.img_ball.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2

        # [Param1 -> Veloc del mov. / Param2 -> Amplitud del mov]
        # A mayor amplitud rebote afecta eje Y y a menor amplitud rebote afecte eje X.

        self.speed = [3,3] #[]
        
    def pibot(self):

        #validate Y ¡!
        if self.rect.bottom >= HEIGHT or self.rect.top <=0:
            
            self.speed[1] = -self.speed[1]
            
            #sonido de un lado
            caer.play()
            

        elif self.rect.right >= WIDTH or self.rect.left <=0:
            
            self.speed[0] = -self.speed[0]
            
            #sonido del otro lado
            caer.play()
                 
        #validate x <- x ->
        self.rect.move_ip(self.speed)
        

#########################################################


class Bar(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.img_bar = pygame.image.load('images/paleta.png')
        self.rect = self.img_bar.get_rect()
        self.rect.midbottom = (WIDTH / 2,HEIGHT-10)
        self.speed = [0,0] # []
                

    def slide(self,listener):
        
        if listener.key == pygame.K_LEFT and self.rect.left > 0 :
            self.speed = [-5,0]

        elif listener.key == pygame.K_RIGHT and self.rect.right < WIDTH:
            self.speed =  [5,0]

        else:
            self.speed = [0,0]

        self.rect.move_ip(self.speed)

#######################################################

class Brick(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/ladrillo.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = position
                

#######################################################

class Wall(pygame.sprite.Group):
    def __init__(self,totalBrick):
        pygame.sprite.Group.__init__(self)
        posX = 0
        posY = 10
        
        for i in range(totalBrick):
            brick = Brick(( posX,posY ))
            self.add(brick)
            
            posX += brick.rect.width
            if posX >= WIDTH :
                posX = 0
                posY += brick.rect.height

#######################################################

def game_over():
    msg = "Perdiste. Vuelve a intentarlo"
    txt_color = (255,0,0)
    txt_style = pygame.font.SysFont('Arial',35) #(Tipo de letra,Tamaño)
    txt_screen = txt_style.render(msg,True,txt_color)
    txt_screen_rect = txt_screen.get_rect()
    txt_screen_rect.center = [WIDTH/2,HEIGHT/2]
    screen.blit(txt_screen,txt_screen_rect)
    pygame.display.flip()
    print("Game Over") 
    time.sleep(3)
    sys.exit()

def set_score():
    
    text_color = (130, 190, 67)
    txt_style = pygame.font.SysFont('Arial',35) #(Tipo de letra,Tamaño)
    txt_screen= txt_style.render(str(score).zfill(1),True,text_color)
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
    
    


#######################################

#General settings

WIDTH = 640
HEIGHT = 480
BG_COLOR = (60,210,90)

screen = pygame.display.set_mode( (WIDTH,  HEIGHT) )
pygame.display.set_caption('Atari')
icon = pygame.image.load('images/main_icon.png')
pygame.display.set_icon(icon)

game_clock = pygame.time.Clock()#Reloj
pygame.key.set_repeat(20)



print(":::::::::::::::::::::::::::")
print("Menu nivel del juego")
print(":::::::::::::::::::::::::::")
print("1. Nivel Inicial")
print("2. Nivel Intermedio")
print("3. Nivel Avanzado")
print("4. Salir")
print("")


status = True
while status:

    opt=int(input("Seleccione el nivel: "))
    
    if opt>=1 and opt<=4:
        status = False

if opt==1:
    ladrillos=20
    
elif opt==2:
    ladrillos=100
    
elif opt==3:
    ladrillos=200
    
elif opt==4:

    print("Has salido del juego")
    os.system("pause")
    sys.exit()

else:
    print("Opcion invalida.")
    os.system("pause")
    sys.exit()

wall = Wall(ladrillos)
ball = Ball()
player = Bar()
score = 0
player_lives = 3


#Loop (Revisión cíclica de los eventos) => Listener

while True:
    game_clock.tick(60)
    for event in pygame.event.get():
        
        # Verifica si se preciono la letra x de la ventana

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Verifica si el jugador precionó tecla del teclado

        elif event.type == pygame.KEYDOWN:
            player.slide(event)
            


    #call pibot
    ball.pibot()

    #collisions between bar and ball
    #Cambio de trayectoria de la bola

    if pygame.sprite.collide_rect(ball,player):  #Player is the bar.

        ball.speed[1]=-ball.speed[1]
         
        #sonido al caer al suelo
        caer.play()

    #Collisions between ball and wall (bricks)Destroy bricks (Destruir ladrillos)
    
    elements =  pygame.sprite.spritecollide(ball,wall,False,collided=None)
    
    if elements : #Mientras existan ladrillos para chocar.

        brink = elements[0]
        centx = ball.rect.centerx
    
        if centx < brink.rect.left or centx > brink.rect.right:

            #Afectamos velocidad

            ball.speed[0] = -ball.speed[0]
    
        else:
            # Afectamos trayectoria
            ball.speed[1] = -ball.speed[1]
        wall.remove(brink)

        #sonido eliminar ladrillo

        elimi.play()
        
        score = score + 1  #score+=1

    #Llamar la función game over cuando la bola  toque el piso

    if ball.rect.bottom >= HEIGHT:
        player_lives = player_lives-1 #player_lives-=1
    
    if player_lives == 0:
        terminado.play()
        game_over()
            
        


    #set Background Color

    screen.fill(BG_COLOR)
    set_score()

    set_lives()

    #Draw de la ball

    screen.blit(ball.img_ball, ball.rect)
    
    #Draw de la bar

    screen.blit(player.img_bar, player.rect)
    
    #Draw muro

    wall.draw(screen)
    
    #Refresh de elementos en screen

    pygame.display.flip()