from pygame import font

class Points_marker():
     def __init__(self, size=60):
          self.font = font.Font("module/resource/undertale.ttf", size)
          self.position = [0, 40]
          self.number = 0


     def set_text(self, number, color=(255, 255, 255)):
          self.color = color
          self.number = number


     def draw(self, screen, x=0, y=40):
          self.position[0] =  x
          self.position[1] =  y
          
          text = self.font.render(str(f"{self.number}"), True, self.color)
          text_rect = text.get_rect(center=self.position)
          
          screen.blit(text, text_rect)
