from pointsMarker import Points_marker

class GameManager:
     def __init__(self, player1, player2, ball, windowSize):
          self.p1 = player1
          self.p2 = player2

          self.ball = ball
          self.screen = windowSize

          self.p1_marker = Points_marker(windowSize)
          # self.p2_marker = Points_marker(windowSize)



     def collision_ball(self):
          ball_x1, ball_y1, ball_x2, ball_y2 = self.ball.hitBox

          if ball_x1 < self.screen[0] // 2:
               player = self.p1
          else:
               player = self.p2

          player_x1, player_y1, player_x2, player_y2 = player.hitBox
          if ball_x1 >= player_x2 and ball_x2 <= player_x1 and ball_y1 <= player_y2 and ball_y2 >= player_y1:
               self.ball.speed_x *= -1



     def ball_restart(self):
          if self.ball.pos_x > self.screen[0] + self.ball.halfSize or self.ball.pos_x <= -self.ball.halfSize:
               self.ball.pos_x = self.ball.x_start
               self.ball.pos_y = self.ball.y_start
          
          if self.ball.pos_x > self.screen[0] + self.ball.halfSize:
               self.p1.points += 1
          else:
               self.p2.points += 1

          # self.player_points(screen)



     def player_points(self, screen):
          self.p1_marker.set_number(self.p1.points)
          self.p1_marker.draw(screen)
