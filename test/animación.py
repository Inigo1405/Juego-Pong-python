import pygame, sys


#Definir colores
BLACK = (0,0,0)
WHITE = (255,255,255)

#Inicializar la librería
pygame.init()

#Crear ventana
size = (800, 500)
screen = pygame.display.set_mode(size)

# Controla los FPS
clock = pygame.time.Clock()


#* Coordenadas del cuadrado
large, height = screen.get_size()

pos_x = large/2
pos_y = height/2

side = 30



#? Velocidad del cuadrado
speed_x = 5
speed_y = 5


#*Correr juego
while True:
     #Registra todo lo de la ventana
     for event in pygame.event.get():
          #print(event)
          #Saldrá al cerrar ventana
          if event.type == pygame.QUIT:
               sys.exit()

     #Color fondo
     screen.fill(BLACK)
     
     #! --- Zona de animación ---

     #Para que rebote el cuadrado
     if pos_x > large-side or pos_x < 0:
          speed_x *= -1
     
     if pos_y > height-side or pos_y < 0:
          speed_y *= -1

     pos_x += speed_x
     pos_y += speed_y
          

     if pos_y == height-side and pos_x == large-side:          
          print("Esquina!!!")



     #! --- Zona de dibujo ---
     pygame.draw.rect(screen, WHITE, (pos_x, pos_y, side, side))


     #Actualizar pantalla
     pygame.display.flip()
     clock.tick(60)