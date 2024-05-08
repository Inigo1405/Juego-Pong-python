import random
import pygame
from sys import exit
from cv2 import destroyAllWindows

from module.pointsMarker import Points_marker

class GameManager:
     def __init__(self, player1, player2, ball, windowSize, screen, pressed_key):
          self.p1 = player1
          self.p2 = player2
          self.ball = ball

          self.windowSize = windowSize
          self.screen = screen

          self.title_label = Points_marker(100)
          self.start_label = Points_marker(45)
          self.p1_marker = Points_marker()
          self.p2_marker = Points_marker()

          self.start_button = False
          self.pressed_key = pressed_key



     def start_game(self, start_button, clock):
          WHITE = (255,255,255)
          BLACK = (0,0,0)

          tiempo_transcurrido = 0
          texto_visible = False
          
          pygame.mixer.music.load("module/resource/intro.mp3")
          pygame.mixer.music.set_volume(0.09)
          pygame.mixer.music.play(-1)

          while not start_button:
               if self.get_event():
                    return True
               
               tiempo_transcurrido += clock.tick()
               if tiempo_transcurrido >= 400:
                    texto_visible = not texto_visible  # Cambiar visibilidad del texto
                    tiempo_transcurrido = 0


               self.screen.fill(BLACK) 
               if texto_visible:
                    self.start_label.set_text('PRESS START', WHITE)
                    self.start_label.draw(self.screen, self.windowSize[0] // 2, self.windowSize[1] // 2)

               self.title_label.set_text('PONG GAME')
               self.title_label.draw(self.screen, self.windowSize[0] // 2, self.windowSize[1] // 5)

               pygame.display.flip()
          


     def collision_ball(self):
          # Identifica al jugador
          if self.ball.pos_x < self.windowSize[0] // 2:
               player = self.p1
          else:
               player = self.p2

          ball_x1, ball_y1, ball_x2, ball_y2 = self.ball.hitBox
          plr_x1, plr_y1, plr_x2, plr_y2 = player.hitBox

          # Compara que impacte en la paleta
          if ball_x1 >= plr_x2 and ball_x2 <= plr_x1 and ball_y1 <= plr_y2 and ball_y2 >= plr_y1:
               # Up
               if self.ball.pos_y <= player.pos_y - player.height/4:
                    self.bounce_off_paddle('up')

               # Down
               elif self.ball.pos_y >= player.pos_y + player.height/4:
                    self.bounce_off_paddle('down')

               # Center
               else:
                    self.bounce_off_paddle('center')

     

     def bounce_off_paddle(self, side):
          self.ball.speed_x *= -1
          
          sound2 = pygame.mixer.Sound("module/resource/hit.mp3")
          channel2 = sound2.play(0)
          channel2.set_volume(1)

          if side == 'up':
               # Recupera la velocidad en Y
               if self.ball.last_angle != 0:
                    self.ball.speed_y = +self.ball.last_angle

               # Speed_y positivo
               if self.ball.speed_y > 0:
                    self.ball.speed_y *= -1
               self._speedValues()
               self.ball.last_angle = 0

          elif side == 'down':
               # Recupera la velocidad en Y
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

          elif self.ball.speed_y == 0:
               self.ball.speed_y += 3

          elif self.ball.speed_y >= -10:
               self.ball.speed_y -= 1



     def ball_restart(self, clock, hand_pos_y, cap):
          if self.ball.pos_x > self.windowSize[0] + self.ball.halfSize or self.ball.pos_x <= -self.ball.halfSize:
              
               # Regresa la pelota sus valores iniciales
               self.ball.pos_x = self.ball.x_start
               self.ball.pos_y = self.ball.y_start

               self.ball.last_angle = 0

               self.ball.speed_x = self.ball.speed_x_start
               self.ball.speed_y = random.choice([5, -5])

               # Manda a los jugadores a sus posiciones iniciales
               self.p1.pos_y = self.p1.y_start
               self.p2.pos_y = self.p2.y_start

               self.p1.speed_y = 0 
               self.p2.speed_y = 0 
               
               hand_pos_y[0]['y'] = self.p1.y_start
               hand_pos_y[1]['y'] = self.p2.y_start

               # Punto ganado
               if self.ball.hitBox[0] > self.windowSize[0] // 2:
                    self.p1.points += 1
               else:
                    self.p2.points += 1


               # Permite eventos mientras sacan
               time_elapsed = 0
               while time_elapsed < 1200: # 1000 milisegundos '1 segundo'
                    self.draw_game()
                    self.get_event(cap)
                    pygame.display.update()
                    time_elapsed += clock.tick(60)

               
               
     def get_event(self, cap=None):
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    if cap:    
                         cap.release()
                         destroyAllWindows()
                    pygame.quit()
                    exit()
          
               # Eventos teclado
               if event.type == pygame.KEYDOWN:
                    self.pressed_key.add(event.key)
                    if event.key == pygame.K_SPACE:
                         return True
                    
               if event.type == pygame.KEYUP:
                    self.pressed_key.discard(event.key)
          return False



     def player_points(self):
          # Indica el número de puntos
          self.p1_marker.set_text(self.p1.points)
          self.p2_marker.set_text(self.p2.points)
          
          # Dibuja en pantalla los puntos
          self.p1_marker.draw(self.screen, (self.windowSize[0] // 2) - 200)
          self.p2_marker.draw(self.screen, (self.windowSize[0] // 2) + 200)


     
     def draw_game(self):
          # Text
          self.player_points()

          # Ball
          rectBall = (self.ball.pos_x - self.ball.halfSize), (self.ball.pos_y - self.ball.halfSize), self.ball.sizeBall, self.ball.sizeBall
          pygame.draw.rect(self.screen, self.ball.color, (rectBall))
          
          # Players
          pygame.draw.rect(self.screen, self.p1.color, (self.p1.pos_x, (self.p1.pos_y - self.p1.halfHeight), self.p1.width, self.p1.height))
          pygame.draw.rect(self.screen, self.p2.color, (self.p2.pos_x, (self.p2.pos_y - self.p2.halfHeight), self.p2.width, self.p2.height))