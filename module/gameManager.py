import time
from pygame import draw
from module.pointsMarker import Points_marker

class GameManager:
     def __init__(self, player1, player2, ball, windowSize):
          self.p1 = player1
          self.p2 = player2

          self.ball = ball
          self.windowSize = windowSize

          self.p1_marker = Points_marker()
          self.p2_marker = Points_marker()



     def collision_ball(self):
          ball_x1, ball_y1, ball_x2, ball_y2 = self.ball.hitBox

          if ball_x1 < self.windowSize[0] // 2:
               player = self.p1
          else:
               player = self.p2

          player_x1, player_y1, player_x2, player_y2 = player.hitBox
          if ball_x1 >= player_x2 and ball_x2 <= player_x1 and ball_y1 <= player_y2 and ball_y2 >= player_y1:
               self.ball.speed_x *= -1



     def ball_restart(self):
          if self.ball.pos_x > self.windowSize[0] + self.ball.halfSize or self.ball.pos_x <= -self.ball.halfSize:
               self.ball.pos_x = self.ball.x_start
               self.ball.pos_y = self.ball.y_start
               
               if self.ball.hitBox[0] > self.windowSize[0] // 2:
                    self.p1.points += 1
               else:
                    self.p2.points += 1

               #time.sleep(2)
          


     def player_points(self, screen):
          self.p1_marker.set_number(self.p1.points)
          self.p2_marker.set_number(self.p2.points)
          
          #(self.windowSize[0] // 2) - 50
          #print(x)
          
          self.p1_marker.draw(screen, (self.windowSize[0] // 2) - 200)
          self.p2_marker.draw(screen, (self.windowSize[0] // 2) + 200)
