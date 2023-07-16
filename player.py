class Player():
     def __init__(self, numPlayer):
          self.width = 10  # Ancho de la paleta
          self.height = 0  # Altura de la paleta
          self.halfHeight = 0

          self.numPlayer = numPlayer

          self.speed_y = 0 
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
               self.pos_x = width - self.width

          elif self.numPlayer == 2:
               self.pos_x = 0
          

          self.pos_y = self.y_start

     

     def player_movement(self, windowSize):
          width, height = windowSize

          if self.pos_y >= height - self.halfHeight:
               self.pos_y = height - self.halfHeight

          if self.pos_y <= 0 + self.halfHeight:
               self.pos_y = 0 + self.halfHeight


          self.pos_y += self.speed_y