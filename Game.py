import pygame
import sys
import random
import pandas as pd

class Ball:
    def __init__(self,number, fx, fy, vx, vy):
        self.number = number
        self.fx = fx
        self.fy = fy
        self.vx = vx
        self.vy = vy

    def move(self):
        self.fx += self.vx
        self.fy += self.vy
        if self.fx>= width-10 or self.fx<=10:
            self.vx = -self.vx
        if self.fy>= height-10 or self.fy<=10:
            self.vy = -self.vy

    def show_ball(self):
        pygame.draw.circle(screen, (255, 0, 0), (self.fx, self.fy), 10)

    def eat(self,x,y):
        balls.remove(self)

pygame.init()

width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

x, y = int(width/2), int(height/2)
v = 5
speed = [-12,-8,-6,-4,-3,3,4,6,8,12]
radius = 20

balls = [Ball(
            number=1,
            fx=random.randint(10,width-10),
            fy=random.randint(10,height-10),
            vx=random.choice(speed),
            vy=random.choice(speed)
        )]
time = 0
stopwatch = 7
survival_time = 0
health = 'O O O O O'
limiter = 0

while True:
    pygame.display.set_caption("Survive The Balls")
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # clear screen
    screen.fill((0, 0, 0))
    # draw ball
    if health!='':
        pygame.draw.circle(screen, (50, 50, 150), (x, y), radius)
        for ball in balls:
            ball.move()
            ball.show_ball()
            if (ball.fx-20 <=x<= ball.fx+20) and (ball.fy-20 <=y<= ball.fy+20):
                ball.eat(x,y)
                health = health[:len(health)-2]

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and y>=radius:
            y -= v
        if keys[pygame.K_DOWN] and y<=height-radius:
            y += v
        if keys[pygame.K_RIGHT] and x<=width-radius:
            x += v
        if keys[pygame.K_LEFT] and x>=radius:
            x -= v

        time += 1/60
        survival_time += 1/60

        if time >= stopwatch:
            time = 0
            if stopwatch>=5:
                stopwatch -= 0.3
            balls.append(Ball(
                number=len(balls),
                fx=random.randint(10,width-10),
                fy=random.randint(10,height-10),
                vx=random.choice(speed),
                vy=random.choice(speed)
            ))
            
        font = pygame.font.SysFont(None, 20)
        count_text = font.render(f"Balls: {len(balls)}", True, (255, 255, 255))
        text_rect = count_text.get_rect(topright=(width - 10, 10))
        screen.blit(count_text, text_rect)
        
        count_text = font.render(f"Health: {health}", True, (255, 255, 255))
        text_rect = count_text.get_rect(topright=(width - 10, 30))
        screen.blit(count_text, text_rect)

        count_text = font.render(f"Survival Time: {int(survival_time)}", True, (255, 255, 255))
        text_rect = count_text.get_rect(topright=(width - 10, 50))
        screen.blit(count_text, text_rect)
    else:
        if limiter==0:
            limiter=1
            with open("log.csv",'a') as f:
                f.write(f'{int(survival_time)}\n')
        font = pygame.font.SysFont(None, 20)
        count_text = font.render(f"Balls: {len(balls)}", True, (255, 255, 255))
        text_rect = count_text.get_rect(topright=(width - 10, 10))
        screen.blit(count_text, text_rect)
        
        count_text = font.render(f"Health: DEAD", True, (255, 0, 0))
        text_rect = count_text.get_rect(topright=(width - 10, 30))
        screen.blit(count_text, text_rect)

        count_text = font.render(f"Survival Time: {int(survival_time)}", True, (255, 255, 255))
        text_rect = count_text.get_rect(topright=(width - 10, 50))
        screen.blit(count_text, text_rect)
        font = pygame.font.SysFont(None, 70)

        count_text = font.render(f"Game Over", True, (255, 0, 0))
        text_rect = count_text.get_rect(center=(width//2, height//2))
        screen.blit(count_text, text_rect)

        log = pd.read_csv('log.csv')
        font = pygame.font.SysFont(None, 25)

        max_time = log['time'].max()
        count_text = font.render(f"Max Survival Time: {max_time}", True, (255, 255, 255))
        text_rect = count_text.get_rect(center=(width//2, height//2+40))
        screen.blit(count_text, text_rect)

    pygame.display.flip()
    clock.tick(60)