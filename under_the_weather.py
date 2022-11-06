import pygame
import random
import neat
import os
import pickle
import sys
import time

pygame.init()
win = pygame.display.set_mode((500,500))
pygame.display.set_caption("Under the Weather")
color = (0,255,0)
mode = "start"
level = 0
at_level = 1
endless = False
class levels:
    def __init__(self):
        self.cloud = pygame.image.load("cloud.PNG")
        self.dude = pygame.image.load("umbrella.PNG")
    def select(self):
        global mode
        global at_level
        global level
        global amount
        global others
        global storms
        global nets
        global ge
        ge = []
        storms = []
        nets = []
        with open("AI.pickle","rb") as f:
            genome = pickle.load(f)
        config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "config-feedforward.txt")
        ge = []
        nets = []
        storms = []
        count = 0
        font = pygame.font.SysFont('Corbel',50)
        Tinyfont = pygame.font.SysFont('Corbel',15)
        Title = font.render('Level Select' , True , (255,255,255))
        win.blit(Title,(120,20))
        win.blit(self.cloud,(150,90))
        win.blit(self.dude,(250,90))
        for i in range(5):
            for z in range(2):
                count += 1
                label = font.render(str(count) , True , (255,255,255))
                num = (i + 1) * 80
                num2 = (z + 1) * 80
                pygame.draw.rect(win,(100,100,100),(-10 + num,130 + num2,50,50))
                win.blit(label,(-10 + num,130 + num2))
                left, middle, right = pygame.mouse.get_pressed()
                if left:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] >= -10 + num and mouse[0] <= (-10 + num) + 50:
                        if mouse[1] >= 130 + num2 and mouse[1] <= (130 + num2) + 50:
                            if at_level >= count:
                                level = count
                                others = []
                                for i in range(random.randint(1,level)):
                                    others.append(other())
                                mode = "play"
Levels = levels()
            
class start:
    def __init__(self):
        self.x1 = 150
        self.y1 = 200
        self.x2 = 120
        self.y2 = 300
        self.bg = pygame.image.load("rain.JPG")
        self.background = pygame.transform.scale(self.bg,(500,500))
        
    def select(self):
        global mode
        global endless
        global others
        others = []
        smallfont = pygame.font.SysFont('Corbel',35)
        font = pygame.font.SysFont('Corbel',50)
        text = smallfont.render('Levels' , True , color)
        text2 = smallfont.render('Endless Mode' , True , color)
        Title = smallfont.render('Under the Weather' , True , color)
        #pygame.draw.rect(win,(100,100,100),(self.x1,self.y1,150,50))
        #pygame.draw.rect(win,(100,100,100),(self.x2,self.y2,220,50))
        win.blit(text,(self.x1 + 25, self.y1 + 10))
        win.blit(text2,(self.x2 + 25, self.y2 + 10))
        win.blit(Title,(100, 20))
        left, middle, right = pygame.mouse.get_pressed()
        if left:
            mouse = pygame.mouse.get_pos()
            if mouse[0] >= self.x1 and mouse[0] <= self.x1 + 150:
                if mouse[1] >= self.y1 and mouse[1] <= self.y1 + 50:
                    endless = False
                    mode = "levels"
            if mouse[0] >= self.x2 and mouse[0] <= self.x2 + 220:
                if mouse[1] >= self.y2 and mouse[1] <= self.y2 + 50:
                    endless = True
                    for i in range(random.randint(1,10)):
                        others.append(other())
                    mode = "play"
                
            
Start = start()
        
class other:
    def __init__(self):
        self.x = random.randint(0,9) * 50
        self.y = random.randint(0,9) * 50
        self.x2 = random.randint(0,9) * 50
        self.y2 = random.randint(0,9) * 50
        self.direction = random.randint(1,4)
        self.wait = 0
        self.house = pygame.image.load("House.PNG")
        self.car = pygame.image.load("automobile.PNG")
        self.light = pygame.image.load("traffic.PNG")
    def draw(self):
        win.blit(self.light,(self.x,self.y))
        win.blit(self.car,(self.x2,self.y2))
    def move(self):
        self.wait += 1
        if self.wait >= 5:
            if self.direction == 1:
                self.x2 += 50
            elif self.direction == 2:
                self.x2 -= 50
            elif self.direction == 3:
                self.y2 += 50
            elif self.direction == 4:
                self.y2 -= 50
            self.wait = 0
class army:
    def __init__(self):
        self.infantry = pygame.image.load("umbrella.PNG")
        self.house = pygame.image.load("House.PNG")
        self.x = 0
        self.y = 0
        self.end_x = random.randint(0,9) * 50
        self.end_y = random.randint(4,9) * 50
    def draw(self):
        win.blit(self.house,(self.end_x,self.end_y))
        win.blit(self.infantry,(self.x,self.y))
    def move(self):
        global wait
        global mode
        move = True
        movement = pygame.key.get_pressed()
        if movement[pygame.K_q]:
            mode = "start"

        if movement[pygame.K_LEFT] and self.x >= 50:
            for obstacle in others:
                if self.x - 50 != obstacle.x or self.y != obstacle.y:
                    pass
                else:
                    move = False
            if move:
                self.x -= 50
                wait += 5
        elif movement[pygame.K_RIGHT] and self.x <= 400:
            for obstacle in others:
                if self.x + 50 != obstacle.x or self.y != obstacle.y:
                    pass
                else:
                    move = False
            if move:
                self.x += 50
                wait += 5
        elif movement[pygame.K_UP] and self.y >= 50:
            for obstacle in others:
                if self.y - 50 != obstacle.y or self.x != obstacle.x:
                    pass
                else:
                    move = False
            if move:
                self.y -= 50
                wait += 5
        elif movement[pygame.K_DOWN] and self.y <= 400:
            for obstacle in others:
                if self.y + 50 != obstacle.y or self.x != obstacle.x:
                    pass
                else:
                    move = False
            if move:
                self.y += 50
                wait += 5
        if self.x == self.end_x:
            if self.y == self.end_y:
                clear()
                
        

class weather:
    def __init__(self):
        self.cloud = pygame.image.load("cloud.PNG")
        self.x = random.randint(0,9) * 50
        self.y = random.randint(0,9) * 50
        self.time = 0
    def draw(self):
        win.blit(self.cloud,(self.x,self.y))
            
            
        
def ow():
    global mode
    soldiers[0].x = 0
    soldiers[0].y = 0
    soldiers[0].end_x = random.randint(0,9) * 50
    soldiers[0].end_y = random.randint(0,9) * 50
    for cloud in storms:
        cloud.x = random.randint(0,9) * 50
        cloud.y = random.randint(0,9) * 50
    for other in others:
        other.x = random.randint(0,9) * 50
        other.y = random.randint(0,9) * 50
    mode = "start"
def clear():
    global mode
    global level
    global at_level
    soldiers[0].x = 0
    soldiers[0].y = 0
    soldiers[0].end_x = random.randint(0,9) * 50
    soldiers[0].end_y = random.randint(0,9) * 50
    for cloud in storms:
        cloud.x = random.randint(0,9) * 50
        cloud.y = random.randint(0,9) * 50
    for other in others:
        other.x = random.randint(0,9) * 50
        other.y = random.randint(0,9) * 50
    if level >= at_level:
        at_level += 1
    if not endless:
        mode = "levels"
    
storms = []
def draw():
    global wait
    global others
    global storms
    if mode == "start":
        win.blit(Start.background,(0,0))
        Start.select()
        pygame.display.update()
    if mode == "levels":
        win.fill((0,0,0))
        Levels.select()
        pygame.display.update()
                           
    if mode == "play":
        win.fill((0,255,0))
        for obstacle in others:
            obstacle.draw()
            if obstacle.x2 == soldiers[0].x:
                if obstacle.y2 == soldiers[0].y:
                    ow()
        soldiers[0].draw()
        soldiers[0].move()
        for i,storm in enumerate(storms):
            if storms[i].x - soldiers[0].x == 0:
                    if storms[i].y - soldiers[0].y == 0:
                        ow()
                            
        for i in range(10):
            num = i + 1
            pygame.draw.rect(win,(0,0,0),(0,i * 50,50,50),1)
            pygame.draw.rect(win,(0,0,0),(50,i * 50,50,50),1)
            pygame.draw.rect(win,(0,0,0),(100,i * 50,50,50),1)
            pygame.draw.rect(win,(0,0,0),(150,i * 50,50,50),1)
            pygame.draw.rect(win,(0,0,0),(200,i * 50,50,50),1)
            pygame.draw.rect(win,(0,0,0),(250,i * 50,50,50),1)
            pygame.draw.rect(win,(0,0,0),(300,i * 50,50,50),1)
            pygame.draw.rect(win,(0,0,0),(350,i * 50,50,50),1)
            pygame.draw.rect(win,(0,0,0),(400,i * 50,50,50),1)
            pygame.draw.rect(win,(0,0,0),(450,i * 50,50,50),1)
def train(genome,config):
    global wait
    global ge
    global soldiers
    global others
    storms = []
    ge = []
    nets = []
    soldiers = []
    run = True
    wait = 0
    for i in range(random.randint(1,10)):
        storms.append(weather())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)

    soldiers.append(army())

    while run:
        pygame.time.delay(300)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
        draw()
        if mode == "play":
            wait += 10
            for other in others:
                other.move()

            if len(storms) == 0:
                break
                        
            move = True
            if wait >= 30:
                for i, storm in enumerate(storms):
                    output = nets[i].activate((storm.x - soldiers[0].x,storm.y - soldiers[0].y))
                    descision = output.index(max(output))
                    if descision == 0 and storm.x >= 50:
                        for obstacle in others:
                            if storm.x - 50 != obstacle.x or storm.y != obstacle.y:
                                pass
                            else:
                                move = False
                        if move:
                            storm.x -= 50
                    elif descision == 1 and storm.x <= 400:
                        for obstacle in others:
                            if storm.x + 50 != obstacle.x or storm.y != obstacle.y:
                                pass
                            else:
                                move = False
                        if move:
                            storm.x += 50
                    elif descision == 2 and storm.y >= 50:
                        for obstacle in others:
                            if storm.y - 50 != obstacle.y or storm.x != obstacle.x:
                                pass
                            else:
                                move = False
                        if move:
                            storm.y -= 50
                    elif descision == 3 and storm.y <= 400:
                        for obstacle in others:
                            if storm.y + 50 != obstacle.y or storm.x != obstacle.x:
                                pass
                            else:
                                move = False
                        if move:
                            storm.y += 50
                    wait = 0
                if storms[0].x - soldiers[0].x == 0:
                        if storms[0].y - soldiers[0].y == 0:
                            ow()
            for storm in storms:
                storm.draw()
            #draw()
                        
                
            pygame.display.update()
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    AI = pop.run(train, 10)
    with open("AI.pickle","wb") as f:
        pickle.dump(AI,f)
def test(config):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "config-feedforward.txt"
    )
    with open("AI.pickle","rb") as f:
        winner = pickle.load(f)
    genome = [(1,winner)]
    train(winner,config)
    


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    #run(config_path)
    test(config_path)
    
    

