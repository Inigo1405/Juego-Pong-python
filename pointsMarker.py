from pygame import font

class Points_marker():
     def __init__(self, windowSize):
          self.font = font.Font("undertale.ttf", 50)
          self.position = windowSize[0] // 2, windowSize[1] // 2
          self.color = (255, 255, 255)
          self.number = 0

     def set_number(self, number):
          self.number = number

     def draw(self, screen):
          text = self.font.render(str(self.number), True, self.color)
          text_rect = text.get_rect(center=self.position)
          screen.blit(text, text_rect)
