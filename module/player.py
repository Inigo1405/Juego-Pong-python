from pygame import K_UP, K_DOWN, K_w, K_s

class Player():
     def __init__(self, numPlayer):
          self.width = 10  # Ancho de la paleta
          self.height = 0  # Altura de la paleta

          self.halfHeight = 0

          self.points = 0
          self.hitBox = [0, 0, 0, 0]
          self.numPlayer = numPlayer

          self.speed_y = 0 
          self.maxSpeed = 7
          self.color = (255,255,255)

          self.y_start = None

          self.pos_x = None
          self.pos_y = None


    
     def get_player_start(self, windowSize):
          width, height = windowSize

          self.height = height / 4
          self.halfHeight = self.height/2

          self.y_start = height / 2


          if self.numPlayer == 1:
               self.pos_x = 0

          elif self.numPlayer == 2:
               self.pos_x = width - self.width
          

          self.pos_y = self.y_start

     

     def player_movement(self, windowSize):
          width, height = windowSize

          if self.pos_y >= height - self.halfHeight:
               self.pos_y = height - self.halfHeight

          if self.pos_y <= 0 + self.halfHeight:
               self.pos_y = 0 + self.halfHeight

          self.pos_y += self.speed_y

          #HitBox values
          self.hitBox[1] = self.pos_y - self.halfHeight
          self.hitBox[3] = self.pos_y + self.halfHeight

          if self.numPlayer == 1:
               self.hitBox[0] = self.pos_x + self.width
               self.hitBox[2] = self.pos_x

          elif self.numPlayer == 2:
               self.hitBox[0] = self.pos_x + self.width
               self.hitBox[2] = self.pos_x


     
     def update_player_speed(self, teclas_presionadas):
          if self.numPlayer == 1:
               if K_w in teclas_presionadas:
                    self.speed_y = -self.maxSpeed
               elif K_s in teclas_presionadas:
                    self.speed_y = self.maxSpeed
               else:
                    self.speed_y = 0
          
          elif self.numPlayer == 2:
               if K_UP in teclas_presionadas:
                    self.speed_y = -self.maxSpeed
               elif K_DOWN in teclas_presionadas:
                    self.speed_y = self.maxSpeed
               else:
                    self.speed_y = 0