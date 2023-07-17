class Ball():
    def __init__(self, size):
        self.sizeBall = size
        self.halfSize = size / 2

        self.hitBox = [0, 0, 0, 0]
        self.color = (255,255,255)

        self.x_start = None
        self.y_start = None

        self.pos_x = None
        self.pos_y = None

        self.speed_x = 5
        self.speed_y = 5



    def get_ball_start(self, windowSize):
        """Define el centro de la pantalla como el inicio"""
        large, height = windowSize

        self.x_start = large / 2
        self.y_start = height / 2

        self.pos_x = self.x_start
        self.pos_y = self.y_start



    def ball_movement(self, windowSize):
        width, height = windowSize
     
        # Regresa a su posición original al salir
        if self.pos_x >= width - (self.halfSize) or self.pos_x <= -self.halfSize:
            self.pos_x = self.x_start
            self.pos_y = self.y_start


        if self.pos_y > (height-self.halfSize) or self.pos_y < self.halfSize:
            self.speed_y *= -1


        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        
        self.hitBox[0] = self.pos_x + self.halfSize
        self.hitBox[1] = self.pos_y - self.halfSize
        self.hitBox[2] = self.pos_x - self.halfSize
        self.hitBox[3] = self.pos_y + self.halfSize

        #print(self.hitBox)
    
