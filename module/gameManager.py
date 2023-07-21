import time
from sys import exit
from pygame import draw, event, QUIT, KEYDOWN, K_SPACE
from module.pointsMarker import Points_marker

class GameManager:
     def __init__(self, player1, player2, ball, windowSize, screen):
          self.p1 = player1
          self.p2 = player2

          self.ball = ball
          self.windowSize = windowSize
          self.screen = screen

          self.p1_marker = Points_marker()
          self.p2_marker = Points_marker()

          self.start_button = False


     def start_game(self):
          for evt in event.get():
               if evt.type == QUIT:
                    exit()

               if evt.type == KEYDOWN:
                    if evt.key == K_SPACE:
                         return True
          


     def collision_ball(self):
          ball_x1, ball_y1, ball_x2, ball_y2 = self.ball.hitBox

          if ball_x1 < self.windowSize[0] // 2:
               player = self.p1
          else:
               player = self.p2

          player_x1, player_y1, player_x2, player_y2 = player.hitBox
          if ball_x1 >= player_x2 and ball_x2 <= player_x1 and ball_y1 <= player_y2 and ball_y2 >= player_y1:

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
          #Jugador 2
          if self.ball.pos_x > self.windowSize[0] // 2:

               if side == 'up':
                    if self.ball.last_angle != 0:
                         self.ball.speed_y = +self.ball.last_angle

                    # Speed_y positivo
                    if self.ball.speed_y > 0:
                         self.ball.speed_y *= -1
                    self._speedValues()
                    self.ball.last_angle = 0


               if side == 'down':
                    if self.ball.last_angle != 0:
                         self.ball.speed_y = -self.ball.last_angle

                    # Speed_y positivo
                    if self.ball.speed_y < 0:
                         self.ball.speed_y *= -1
                    self._speedValues()
                    self.ball.last_angle = 0

          #Jugador 1
          else:

               if side == 'up':
                    if self.ball.last_angle != 0:
                         self.ball.speed_y = +self.ball.last_angle

                    # Speed_y positivo
                    if self.ball.speed_y > 0:
                         self.ball.speed_y *= -1
                    self._speedValues()
                    self.ball.last_angle = 0


               if side == 'down':
                    if self.ball.last_angle != 0:
                         self.ball.speed_y = -self.ball.last_angle

                    # Speed_y positivo
                    if self.ball.speed_y < 0:
                         self.ball.speed_y *= -1
                    self._speedValues()
                    self.ball.last_angle = 0


          if side == 'center':
               if self.ball.last_angle == 0:
                    self.ball.last_angle = abs(self.ball.speed_y)
               self._speedValues()
               self.ball.speed_y = 0
               


     def _speedValues(self):
          # Aumento de la velocidad
          if self.ball.speed_x > 0 and self.ball.speed_x <= 15: 
               self.ball.speed_x += 1

          elif self.ball.speed_x >= -15:
               self.ball.speed_x -= 1


          if self.ball.speed_y > 0 and self.ball.speed_x <= 10:
               self.ball.speed_y += 1

          elif self.ball.speed_y >= -10:
               self.ball.speed_y -= 1
          


     def ball_restart(self):
          if self.ball.pos_x > self.windowSize[0] + self.ball.halfSize or self.ball.pos_x <= -self.ball.halfSize:
               self.ball.pos_x = self.ball.x_start
               self.ball.pos_y = self.ball.y_start

               self.ball.last_angle = 0
               
               self.ball.speed_x = self.ball.speed_x_start
               self.ball.speed_y = self.ball.speed_y_start

               # Punto ganado
               if self.ball.hitBox[0] > self.windowSize[0] // 2:
                    self.p1.points += 1
               else:
                    self.p2.points += 1

               #time.sleep(2)
          


     def player_points(self):
          self.p1_marker.set_number(self.p1.points)
          self.p2_marker.set_number(self.p2.points)
          
          self.p1_marker.draw(self.screen, (self.windowSize[0] // 2) - 200)
          self.p2_marker.draw(self.screen, (self.windowSize[0] // 2) + 200)
