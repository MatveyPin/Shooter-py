import pygame
from random import randint

pygame.mixer.init()
pygame.font.init()

window = pygame.display.set_mode((700, 500))
ground = pygame.transform.scale(pygame.image.load("galaxy.jpg"), (700, 500))

pygame.mixer.music.load("space.ogg")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.25)

pygame.display.set_caption("Шутер")

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width=75, height=100):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed 
        if keys[pygame.K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed 
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 10, 10, 25)
        bullets.add(bullet)
        fire = pygame.mixer.Sound("fire.ogg")
        fire.set_volume(0.25)
        fire.play()

player1 = Player("rocket.png", 300, 395, 6, 75, 100)

s = 0   
lost = 0
font = pygame.font.SysFont("Arial", 30)
font1 = pygame.font.SysFont("Arial", 30)
rah = font.render('Рахунок:' + str(s), True, (255, 255, 255))
los = font.render('Пропущено:' + str(lost), True, (255, 255, 255))
lose = font1.render('YOU LOST!', True, (255, 0, 0))
won = font1.render('YOU WON!', True, (0, 153, 51))

class Enemy(GameSprite):
    def update(self):
        global lost
        if self.rect.y == 0:
            self.direction = "down"
        if self.direction == "down":
            self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0, 500)
            lost += 1
            global los
            los = font.render('Пропущено:' + str(lost), True, (255, 255, 255))
    
            
class Bullet(GameSprite):
    def update(self):
        global s
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
        else:
            if pygame.sprite.spritecollide(self, monsters, True):
                s += 1
                global rah
                rah = font.render('Рахунок: ' + str(s), True, (255, 255, 255))
                self.kill()
                monster1 = Enemy("ufo.png", randint(0, 500), 0, randint(1,3), 85, 55)
                monsters.add(monster1)
            
         
bullets = pygame.sprite.Group()

            
monster1 = Enemy("ufo.png", randint(0, 500), 0, randint(1,3), 85, 55)
monster2 = Enemy("ufo.png", randint(0, 500), 0, randint(1,3), 85, 55)
monster3 = Enemy("ufo.png", randint(0, 500), 0, randint(1,3), 85, 55)
monster4 = Enemy("ufo.png", randint(0, 500), 0, randint(1,3), 85, 55)
monster5 = Enemy("ufo.png", randint(0, 500), 0, randint(1,3), 85, 55)
monsters = pygame.sprite.Group()
monsters.add(monster1, monster2, monster3, monster4, monster5)


game = True
fps = 60
clock = pygame.time.Clock()
x1 = 0
y1 = 0
y2 = 25
x = 200
y = 200
finish = False

while game:
    
    if finish == False:
        window.blit(ground, (x1, y1))
        player1.reset()
        player1.update()
        monsters.draw(window)
        monsters.update()
        window.blit(los, (x1, y2))
        window.blit(rah, (x1, y1))
        bullets.update()
        bullets.draw(window)
        if pygame.sprite.spritecollide(player1, monsters, False) or lost >= 3:
            finish = True
            window.blit(lose, (x, y))
        elif pygame.sprite.groupcollide(bullets, monsters, True, True):
            s += 1
        if s >= 10:
            finish = True
            window.blit(won, (x, y))
        

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                player1.fire()
            
    
    pygame.display.update()
    
    clock.tick(fps)
