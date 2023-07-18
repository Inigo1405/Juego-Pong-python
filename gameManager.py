# from player import p1, p2

class GameManager:
     def __init__(self, player1, player2, ball, windowSize):
          self.p1 = player1
          self.p2 = player2

          self.ball = ball
          self.screen = windowSize


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
          if self.pos_x >= (self.screen[0] - self.halfSize) or self.pos_x <= -self.halfSize:
               self.pos_x = self.x_start
               self.pos_y = self.y_start


     
