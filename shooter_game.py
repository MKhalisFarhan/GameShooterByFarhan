from pygame import *
from pygame.sprite import Sprite, Group, spritecollide, groupcollide
from random import randint

class GameSprite(Sprite):
    def __init__(self, image_path, image_size, x, y):
        super().__init__()
        self.image = transform.scale(image.load(image_path), image_size)
        self.rect = self.image.get_rect(topleft=(x, y))

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed=key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -=5
        if key_pressed[K_d] and self.rect.x < size[0]-sprite[0]:
            self.rect.x +=5
    
    def fire(self):
        bullets.add(Bullet("rudal1.png" , bullet_size, player.rect.x + sprite[0]/2 - bullet_size[0]/2, player.rect.y))

class Enemy(GameSprite):
    def __init__(self, image_path, image_size, x, y, speed):
        super().__init__(image_path, image_size, x, y)
        self.speed = speed
    
    def update(self):
        global missed_score      
        self.rect.y += self.speed
        if self.rect.y > size[1]:
            self.rect.y = 0
            self.rect.x = randint(0, size[0]-sprite[0])
            missed_score += 1

class Bullet(GameSprite):    
    def update(self):
        self.rect.y -= 3
        if self.rect.y < 0:
            print('sudah batas')
            self.kill()


size = (700, 500) # (w,h)
sprite = (65,65)
bullet_size = (20,20)
window = display.set_mode(size)

display.set_caption("Space Shooter")

# define with class
back = GameSprite("bg2.png", size, 0, 0)
player = Player("pesawat1.png", sprite, size[0]/2 - sprite[0]/2, size[1] - sprite[1])

enemies = Group()
for i in range(2):
    enemies.add(Enemy("sus.png", sprite, randint(0, size[0]-sprite[0]), 0, randint(2,6)))

bullets = Group()

clock =time.Clock()
FPS = 30
 
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire = mixer.Sound('fire.ogg')

hit_score = 0
missed_score = 0

font.init()
font1 = font.Font(None, 32)
font2 = font.Font(None, 50)

lose = font2.render('You Lose!', True, (235, 150, 0))
win = font2.render('You Win!', True, (255, 215, 0))

game = True
inactive = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                print('hello from space')
                player.fire()
                fire.play()

    if not inactive:
        # blit with class
        back.reset()

        player.reset()
        player.update()

        bullets.draw(window)
        bullets.update()

        enemies.draw(window)
        enemies.update()

        # defeat
        if spritecollide(player, enemies, False) or missed_score == 3:
            inactive = True
            window.blit(lose, lose.get_rect(center=(size[0]/2, size[1]/2)))

        # win
        if groupcollide(bullets, enemies, True, True):
            hit_score += 1
            enemies.add(Enemy("ufo.png", sprite, randint(0, size[0]-sprite[0]), 0, randint(2,6)))
            if hit_score == 10:
                inactive = True
                window.blit(win, win.get_rect(center=(size[0]/2, size[1]/2)))

        hit = font1.render(f'Hit: {hit_score}', True, (255, 215, 0))
        window.blit(hit, hit.get_rect(topleft=(10, 20)))

        missed = font1.render(f'Missed: {missed_score}', True, (255, 0, 0))
        window.blit(missed, missed.get_rect(topleft=(10, 50)))

    display.update()
    clock.tick(FPS)


