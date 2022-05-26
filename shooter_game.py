from pygame import *
from pygame import sprite
from random import randint
import random

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
font.init()


kills = 0
lost1 = 0
FPS = 20
clock = time.Clock()
window = display.set_mode((700, 500))
display.set_caption('Space Shooter')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
font1 = font.Font(None, 36)
font2 = font.Font(None, 36)
font3 = font.Font(None, 50)
font4 = font.Font(None, 50)

class GameSprite(sprite.Sprite):
    def __init__(self, imag, speed, x, y, width, length):
        super().__init__()
        self.image = transform.scale(image.load(imag), (width, length))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
     def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0 :
            self.kill()

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        centr1 = self.rect.centerx
        top1 =  self.rect.top
        bullet = Bullet('bullet.png', 10, centr1, top1,  30, 30)
        bullets.add(bullet)   

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost1
        if self.rect.y > 430:
            self.rect.x = random.randint(80, 635 - 80)
            self.rect.y = 0
            lost1 = lost1 + 1
rocket = Player('rocket.png', 10, 300, 400, 65, 65)

lost1 = 0
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', 2, random.randint(0, 635), random.randint(1, 2), 50, 50)
    monsters.add(monster)


bullets = sprite.Group()
asteroids = sprite.Group()
for r in range(3):
    asteroid = Enemy('asteroid.png', 2, random.randint(0, 635), random.randint(2, 3), random.randint(50, 50), random.randint(50, 50))
    asteroids.add(asteroid)

text_win = font3.render('You win!! ', 100, (0, 255, 0))
text_lose = font4.render('You lose!! ', 100, (250, 0, 0))

run = True
finish = False
while run:
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
            if e.key == K_TAB:
                finish = False
        
        if e.type == QUIT:
            run = False
    if finish != True:

        text_kills = font2.render('Убито: ' + str(kills), 10, (255, 255, 255))
        text_lost = font1.render('Пропущено: ' + str(lost1), 1, (255, 255, 255))

        window.blit(background, (0, 0))
        window.blit(text_kills, (0, 30))
        window.blit(text_lost, (0, 10))

        monsters.draw(window)
        monsters.update()

        asteroids.draw(window)
        asteroids.update()

        rocket.update()
        rocket.reset()

        bullets.update()
        bullets.draw(window)

        sprite_colide_rocket = sprite.spritecollide(
            rocket, monsters, True
        )

        sprite_colide_asteroid = sprite.spritecollide(
            rocket, asteroids, True
        )
        
        sprite_colide_bullet = sprite.groupcollide(
            bullets, monsters, True,True      
        )
        
        for q in sprite_colide_bullet:
            kills = kills + 1
            monster = Enemy ('ufo.png', 2, random.randint(0, 635), random.randint(1, 2), 50, 50)
            monsters.add(monster) 

        for w in sprite_colide_rocket:
            finish = True
            window.blit(text_lose, (270, 200))
            

        for d in sprite_colide_asteroid:
            finish = True
            window.blit(text_lose, (270, 200))

        if kills == 10:
            finish = True
            window.blit(text_win, (270, 200))

    display.update()
    clock.tick(FPS)