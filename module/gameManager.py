import time
import random
from sys import exit
import pygame
#from pygame import draw, event, QUIT, KEYDOWN, K_SPACE, display
from module.pointsMarker import Points_marker

class GameManager:
     def __init__(self, player1, player2, ball, windowSize, screen):
          self.p1 = player1
          self.p2 = player2

          self.ball = ball
          self.windowSize = windowSize
          self.screen = screen

          self.start_label = Points_marker(100)
          self.p1_marker = Points_marker()
          self.p2_marker = Points_marker()

          self.start_button = False


     def start_game(self, start_button, clock):
          WHITE = (255,255,255)
          BLACK = (0,0,0)

          tiempo_transcurrido = 0
          tiempo_maximo = 900  # 500 milisegundos (0.5 segundos)

          texto_visible = True
          color_fondo_visible = WHITE

          while not start_button:
               tiempo_transcurrido += clock.tick()
               if tiempo_transcurrido >= tiempo_maximo:
                    tiempo_transcurrido = 0
                    texto_visible = not texto_visible  # Cambiar visibilidad del texto
                    color_fondo_visible = BLACK if texto_visible else WHITE
                    

               self.screen.fill(BLACK) 
               if texto_visible:
                    self.start_label.set_number('PONG GAME')
                    self.start_label.draw(self.screen, self.windowSize[0] // 2, self.windowSize[1] // 2)

               pygame.display.flip()

               if self.get_event():
                    return True

          


     def collision_ball(self):
          # Define al jugador
          if self.ball.pos_x < self.windowSize[0] // 2:
               player = self.p1
          else:
               player = self.p2

          ball_x1, ball_y1, ball_x2, ball_y2 = self.ball.hitBox
          plr_x1, plr_y1, plr_x2, plr_y2 = player.hitBox

          # Compara que impacte en la paleta
          if ball_x1 >= plr_x2 and ball_x2 <= plr_x1 and ball_y1 <= plr_y2 and ball_y2 >= plr_y1:
               if self.ball.pos_y <= player.pos_y - player.height/4:
                    #print("Up")
                    self.bounce_off_paddle('up')

               elif self.ball.pos_y >= player.pos_y + player.height/4:
                    #print("Down")
                    self.bounce_off_paddle('down')

               else:
                    #print("Center")
                    self.bounce_off_paddle('center')

     

     def bounce_off_paddle(self, side):
          self.ball.speed_x *= -1

          if side == 'up':
               if self.ball.last_angle != 0:
                    self.ball.speed_y = +self.ball.last_angle

               # Speed_y positivo
               if self.ball.speed_y > 0:
                    self.ball.speed_y *= -1
               self._speedValues()
               self.ball.last_angle = 0

          elif side == 'down':
               if self.ball.last_angle != 0:
                    self.ball.speed_y = -self.ball.last_angle

               # Speed_y positivo
               if self.ball.speed_y < 0:
                    self.ball.speed_y *= -1
               self._speedValues()
               self.ball.last_angle = 0

          elif side == 'center':
               if self.ball.last_angle == 0:
                    self.ball.last_angle = abs(self.ball.speed_y)
               self._speedValues()
               self.ball.speed_y = 0
               


     def _speedValues(self):
          # Aumento de la velocidad en x
          if self.ball.speed_x > 0 and self.ball.speed_x <= 15: 
               self.ball.speed_x += 1

          elif self.ball.speed_x >= -15:
               self.ball.speed_x -= 1

          # Aumento de la velocidad en y
          if self.ball.speed_y > 0 and self.ball.speed_x <= 10:
               self.ball.speed_y += 1

          elif self.ball.speed_y >= -10:
               self.ball.speed_y -= 1
          


     def ball_restart(self, clock):
          if self.ball.pos_x > self.windowSize[0] + self.ball.halfSize or self.ball.pos_x <= -self.ball.halfSize:
              
               self.ball.pos_x = self.ball.x_start
               self.ball.pos_y = self.ball.y_start

               self.ball.last_angle = 0

               self.ball.speed_x = self.ball.speed_x_start
               self.ball.speed_y = random.choice([5, -5])

               self.p1.pos_y = self.p1.y_start
               self.p2.pos_y = self.p2.y_start

               # Punto ganado
               if self.ball.hitBox[0] > self.windowSize[0] // 2:
                    self.p1.points += 1
               else:
                    self.p2.points += 1


               # Permite eventos mientras sacan
               time_elapsed = 0
               while time_elapsed < 1000: # 1000 milisegundos (1 segundo)
                    self.draw_game()
                    self.get_event()
                    pygame.display.update()
                    time_elapsed += clock.tick(60)

               
               
     def get_event(self):
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    exit()
          
               # Eventos teclado
               if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                         return True
          return False



     def player_points(self):
          # Indica el número de puntos
          self.p1_marker.set_number(self.p1.points)
          self.p2_marker.set_number(self.p2.points)
          
          # Dibuja en pantalla los puntos
          self.p1_marker.draw(self.screen, (self.windowSize[0] // 2) - 200)
          self.p2_marker.draw(self.screen, (self.windowSize[0] // 2) + 200)


     
     def draw_game(self):
          # Texto
          self.player_points()

          # Pelota
          rectBall = (self.ball.pos_x - self.ball.halfSize), (self.ball.pos_y - self.ball.halfSize), self.ball.sizeBall, self.ball.sizeBall
          pygame.draw.rect(self.screen, self.ball.color, (rectBall))
          
          # Jugadores
          pygame.draw.rect(self.screen, self.p1.color, (self.p1.pos_x, (self.p1.pos_y - self.p1.halfHeight), self.p1.width, self.p1.height))
          pygame.draw.rect(self.screen, self.p2.color, (self.p2.pos_x, (self.p2.pos_y - self.p2.halfHeight), self.p2.width, self.p2.height))
