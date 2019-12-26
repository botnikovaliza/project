import random
import pygame
import numpy as np
import random
pygame.init()
display_width = 1280
display_height = 720
fps=60
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('My game')
bg = pygame.image.load('фон.jpg').convert()
pb = pygame.image.load('paddle.png').convert()
bl = pygame.image.load('ball.png').convert()
bl1=pygame.image.load('block1.png').convert()
bl2=pygame.image.load('block2.png').convert()
clock = pygame.time.Clock()
BLACK=(0,0,0)
fp_paddle_x=600
fp_paddle_y=650
speed_paddle=9
fp_bl_x=500
fp_bl_y=500
# матрица для блоков
fp_block = np.array([[10, 15]])
fp_block2 = np.array([[1172, 319]])
x=9
y=15
A = np.zeros((x, y))
A[0,0]=1
A[x-1, y-1]=1
kol_bl=40
i=0
while i<kol_bl:
    r=random.randint(0,x-1)
    r2=random.randint(0, y-1)
    if A[r, r2] == 0:
        A[r, r2] = 1
        if random.randint(0, 1) == 1:
            fp_block=np.append(fp_block, [[10+r2*83, 15+r*38]], axis = 0)
        else:
            fp_block2=np.append(fp_block2, [[10+r2*83, 15+r*38]], axis = 0)
        i+=1
kol=int(fp_block.size/2)
kol2=int(fp_block2.size/2)

speed_ball = 6
class Paddle(pygame.sprite.Sprite):
    def __init__(self, fp_paddle_x, fp_paddle_y, speed_paddle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pb, (150, 25))
        self.rect = self.image.get_rect()
        self.rect.x=fp_paddle_x
        self.rect.y=fp_paddle_y
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -speed_paddle
        if keystate[pygame.K_RIGHT]:
            self.speedx = speed_paddle
        self.rect.x += self.speedx
        if self.rect.right > display_width:
            self.rect.right = display_width
        if self.rect.left < 0:
            self.rect.left = 0

class Ball(pygame.sprite.Sprite):
    def __init__(self, fp_bl_x, fp_bl_y, speed_ball):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bl, (25,25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x=fp_bl_x
        self.rect.y=fp_bl_y
        self.speedx = speed_ball
        self.speedy = -speed_ball
    def speed(self):
        self.speedx=-self.speedx
        self.speedy=-self.speedy
    def update(self):
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        #касание со стенками
        if self.rect.bottom > display_height:
            self.rect.bottom  = display_height
            self.speedx=0
        if self.rect.top < 0:
            self.speedy=-self.speedy
        if self.rect.right > display_width:
            self.speedx=-self.speedx
        if self.rect.left < 0:
            self.speedx=-self.speedx
        #касание с платформой
        if ball.rect.right > paddle.rect.left and ball.rect.left < paddle.rect.right and  ball.rect.bottom > paddle.rect.top and  ball.rect.top < paddle.rect.bottom:
            self.speedy=-speed_ball
            self.rect.x+=2*paddle.speedx+self.speedx

class Block(pygame.sprite.Sprite):
    def __init__(self,  fp_block):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bl1, (80, 35))
        self.rect = self.image.get_rect()
        self.rect.x=fp_block[0]
        self.rect.y=fp_block[1]
    def update(self):
        self.rect.x=self.rect.x
        self.rect.y=self.rect.y
class Block2(pygame.sprite.Sprite):
    def __init__(self, fp_block):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(bl2, (80,35))
        self.rect = self.image.get_rect()
        self.rect.x=fp_block[0]
        self.rect.y=fp_block[1]
    def update(self):
        self.rect.x=self.rect.x
        self.rect.y=self.rect.y

all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
blocks2 = pygame.sprite.Group()
paddle = Paddle(fp_paddle_x, fp_paddle_y, speed_paddle)
ball = Ball(fp_bl_x, fp_bl_y, speed_ball)
all_sprites.add(paddle)
all_sprites.add(ball)
for i in range(kol):
    block2=Block2(fp_block[i])
    all_sprites.add(block2)
    blocks2.add(block2)
for i in range(kol):
    block = Block(fp_block[i])
    all_sprites.add(block)
    blocks.add(block)
for i in range(kol2):
    block2 = Block2(fp_block2[i])
    all_sprites.add(block2)
    blocks2.add(block2)



def run_game():
    game = True
    while game:
     #скорость игры
        clock.tick(fps)
        #ввод процесса события
        for event in pygame.event.get():
        # проверить закрытие окна
            if event.type == pygame.QUIT:
                game = False

        #Обновление
        all_sprites.update()
        #столкновение с блоком
        hits = pygame.sprite.spritecollide(ball, blocks, True)
        if hits:
            ball.speed()
        else:
            hits = pygame.sprite.spritecollide(ball, blocks2, True)
            if hits:
                ball.speed()

        #Рендеринг
        display.blit(bg, (0,0))
        all_sprites.draw(display)
        pygame.display.flip() 
run_game() 
pygame.quit()