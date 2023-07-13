import pygame, sys, random
pygame.init()


#Definir colores
BLACK = (0,0,0)
WHITE = (255,255,255)



size = (800, 500)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

#Guarda ubicación de los puntos aleatorios
coor_list = list()
for i in range(70):
     x = random.randint(0, 800)
     y =  random.randint(0, 500)
     pygame.draw.circle(screen, WHITE, (x , y), 2)

     coor_list.append([x,y])


#* Corre juego
while True:
     for event in pygame.event.get():
          if event.type == pygame.QUIT:
               sys.exit()


     screen.fill(BLACK)

     for coord in coor_list:
          pygame.draw.circle(screen, WHITE, coord, 2)
          coord[1] += 1

          if coord[1] > 500:
               coord[1] = 0 


     pygame.display.flip()
     clock.tick(120)
