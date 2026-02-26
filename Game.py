import pygame
import sys
import random

class Ball:
    def __init__(self,number, fx, fy, vx, vy):
        self.number = number
        self.fx = fx
        self.fy = fy
        self.vx = vx
        self.vy = vy
        self.last_bounce_time = 0

    def move(self):
        self.fx += self.vx
        self.fy += self.vy
        current_time = pygame.time.get_ticks()

        if self.fx>= width-10 or self.fx<=10:
            self.vx = -self.vx
            if current_time - self.last_bounce_time > 20:
                bounce_channel.play(bounce_sound)
                self.last_bounce_time = current_time
            
        if self.fy>= height-10 or self.fy<=10:
            self.vy = -self.vy
            if current_time - self.last_bounce_time > 20:
                bounce_channel.play(bounce_sound)
                self.last_bounce_time = current_time

    def show_ball(self):
        pygame.draw.circle(screen, (255, 0, 0), (self.fx, self.fy), 10)

    def eat(self,x,y):
        balls.remove(self)
        damage_channel.play(damage_sound)
        
pygame.init()

width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

x, y = width//2, height//2
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

pygame.mixer.init()

pygame.mixer.set_num_channels(32)

bounce_channel = pygame.mixer.Channel(1)
damage_channel = pygame.mixer.Channel(2)

bounce_sound = pygame.mixer.Sound("Data/bounce.wav")
bounce_sound.set_volume(0.15)
damage_sound = pygame.mixer.Sound("Data/damage.wav")
damage_sound.set_volume(0.3)
pygame.mixer.music.load("Data/bg.wav")
pygame.mixer.music.play(-1)  # -1 = infinite loop

def generate_stars(w,h):
    x,y = random.randint(1,w),random.randint(1,h)
    return x,y

stars = []
for i in range(100):
    stars.append(generate_stars(width,height))

pygame.display.set_caption("Survive The Balls")
icon = pygame.image.load("Data/icon.png")
pygame.display.set_icon(icon)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # clear screen
    screen.fill((0, 0, 0))
    for star in stars:
        pygame.draw.circle(screen, (255,255,255), star, random.choice([1,1,1,2,3]))
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
            with open("Data/log.csv",'a') as f:
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

        font = pygame.font.SysFont(None, 25)
        with open("Data/log.csv",'r') as f:
            header = f.readline()
            m = 0
            for line in f.readlines():
                if int(line.strip())>m:
                    m = int(line.strip())

        count_text = font.render(f"Max Survival Time: {m}", True, (255, 255, 255))
        text_rect = count_text.get_rect(center=(width//2, height//2+40))
        screen.blit(count_text, text_rect)

        count_text = font.render(f"Press R to restart", True, (255, 255, 255))
        text_rect = count_text.get_rect(center=(width//2, height//2+60))
        screen.blit(count_text, text_rect)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            x, y = width//2, height//2
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

    pygame.display.flip()
    clock.tick(60)