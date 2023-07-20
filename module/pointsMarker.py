from pygame import font

class Points_marker():
     def __init__(self):
          self.font = font.Font("module/resource/undertale.ttf", 50)
          self.position = [0, 40]
          self.color = (255, 255, 255)
          self.number = 0


     def set_number(self, number):
          self.number = number


     def draw(self, screen, x=0):
          self.position[0] =  x
          text = self.font.render(str(f"{self.number}"), True, self.color)
          text_rect = text.get_rect(center=self.position)
          screen.blit(text, text_rect)
