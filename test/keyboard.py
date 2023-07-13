import pygame, sys

#Inicializar la libraria
pygame.init()


#Definir colores
BLACK = (0,0,0)
WHITE = (255,255,255)


#Crear ventana
large = 800
height = 500

size = (large, height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# Cuadrado
side = 20
org_pos_x = coord_x = large / 2
org_pos_y = coord_y = height/2

#velocidad
x_speed = 0
y_speed = 0

while True:
     #Registra todo lo de la ventana
     for event in pygame.event.get():
          #print(event)
          #Saldra al cerrar ventana
          if event.type == pygame.QUIT:
               sys.exit()

          #! Eventos teclado
          #Al precionar tecla
          if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_a:
                    x_speed = -5
               if event.key == pygame.K_d:
                    x_speed = 5
               
               if event.key == pygame.K_w:
                    y_speed = -5
               if event.key == pygame.K_s:
                    y_speed = 5


          #Al soltar tecla
          if event.type == pygame.KEYUP:
               if event.key == pygame.K_a:
                    x_speed = 0
               if event.key == pygame.K_d:
                    x_speed = 0

               if event.key == pygame.K_w:
                    y_speed = 0
               if event.key == pygame.K_s:
                    y_speed = 0


     #! --- Zona de animación ---
     screen.fill(BLACK)

     #Para que rebote el cuadrado
     # if pos_x > large-side or pos_x < 0:
     #      speed_x *= -1
     
     # if pos_y > height-side or pos_y < 0:
     #      speed_y *= -1

     coord_x += x_speed
     coord_y += y_speed
     
     

     pygame.draw.rect(screen, WHITE, (coord_x, coord_y, side, side))


     pygame.display.flip()
     clock.tick(60)