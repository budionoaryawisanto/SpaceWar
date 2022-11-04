import sys
import random
import pygame
from pygame.locals import *

pygame.init()


planet = ['sun.jpg', 'moon.jpg', 'earth.jpg',]
player_ship = 'playership.png'
enemy_ship = 'enemyship1.png'
meteor = 'meteor.png'
player_bullet = 'pbullet.png'
enemy_bullet = 'ebullet.png'


screen = pygame.display.set_mode((0,0), FULLSCREEN)
s_width, s_height = screen.get_size()

clock = pygame.time.Clock()
FPS = 60

background_group = pygame.sprite.Group()
planet_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
playerbullet_group = pygame.sprite.Group()
enemybullet_group = pygame.sprite.Group()

sprite_group = pygame.sprite.Group()

class Background(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([x,y])
        self.image.fill('white')
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 1
        self.rect.x += 1 
        if self.rect.y > s_height:
            self.rect.y = random.randrange(-10, 0)
            self.rect.x = random.randrange(-400, s_width)

class Sun(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('black')

    def update(self):
        self.rect.y += 1
        if self.rect.y > s_height:
            self.rect.y = -8000

class Moon(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('black')

    def update(self):
        self.rect.y += 1
        if self.rect.y > s_height:
            self.rect.y = -8000

class Player(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img) 
        self.rect = self.image.get_rect()
        self.image.set_colorkey('black')

    def update(self):
        mouse = pygame.mouse.get_pos()
        self.rect.x = mouse[0] - 9
        self.rect.y = mouse[1] - 5

    def shoot(self):
        bullet = PlayerBullet(player_bullet)
        mouse = pygame.mouse.get_pos()
        bullet.rect.x = mouse[0]
        bullet.rect.y = mouse[1]
        playerbullet_group.add(bullet)
        sprite_group.add(bullet)

class Enemy(Player):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = random.randrange(0, s_width)
        self.rect.y = random.randrange(-500, 0)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y += 1
        if self.rect.y > s_height:
            self.rect.x = random.randrange(0, s_width)
            self.rect.y = random.randrange(-500, 0)
        self.shoot()
    
    def shoot(self):
        if self.rect.y > 0:
            if self.rect.y % 80 == 0:
                enemybullet = EnemyBullet(enemy_bullet)
                enemybullet.rect.x = self.rect.x + 28
                enemybullet.rect.y = self.rect.y + 20
                enemybullet_group.add(enemybullet)
                sprite_group.add(enemybullet)


class Meteor(Enemy):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = random.randrange(0, s_width)
        self.rect.y = random.randrange(-900, -300)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y += 1
        if self.rect.y > s_height:
            self.rect.x = random.randrange(0, s_width)
            self.rect.y = random.randrange(-900, -300)

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('black')

    def update(self):
        self.rect.y -= 5
        if self.rect.y < 0:
            self.kill()

class EnemyBullet(PlayerBullet):
    def __init__(self, img):
        super().__init__(img)

    def update(self):
        self.rect.y += 3
        if self.rect.y > s_height:
            self.kill()

class Game: 
    def __init__(self):
        self.count_enemyHit = 0
        self.count_meteorHit = 0
        self.lives = 3
        self.run_game()

    def create_background(self):
        for i in range(30):
            x = random.randint(1,3)
            background_image = Background(x,x)
            background_image.rect.x = random.randrange(0, s_width)
            background_image.rect.y = random.randrange(0, s_height)
            background_group.add(background_image)
            sprite_group.add(background_image)

    def create_sun(self):
        for i in range(1):
            planet_image = Sun(planet[i])
            planet_image.rect.x = s_width - 1500
            planet_image.rect.y = -4000
            planet_group.add(planet_image)
            sprite_group.add(planet_image)

    def create_moon(self):
        for i in range(1):
            planet_image = Moon(planet[1])
            planet_image.rect.x = s_width - 1000
            planet_image.rect.y = -8000
            planet_group.add(planet_image)
            sprite_group.add(planet_image)

    def create_player(self):
        self.player = Player(player_ship)
        player_group.add(self.player)
        sprite_group.add(self.player)

    def create_enemy(self):
        for i in range(10):
            self.enemy = Enemy(enemy_ship)
            enemy_group.add(self.enemy)
            sprite_group.add(self.enemy)

    def create_meteor(self):
        for i in range(3):
            self.meteor = Meteor(meteor)
            meteor_group.add(self.meteor)
            sprite_group.add(self.meteor)

    def playerbullet_hits_enemy(self):
        hits = pygame.sprite.groupcollide(enemy_group, playerbullet_group, False, True)
        for i in hits:
            self.count_enemyHit += 1
            if self.count_enemyHit == 3:
                i.rect.x = random.randrange(0, s_width)
                i.rect.y = random.randrange(-600, -300)
                self.count_enemyHit = 0

    def playerbullet_hits_meteor(self):
        hits = pygame.sprite.groupcollide(meteor_group, playerbullet_group, False, True)
        for i in hits:
            self.count_meteorHit += 1
            if self.count_meteorHit == 6:
                i.rect.x = random.randrange(0, s_width)
                i.rect.y = random.randrange(-600, -300)
                self.count_meteorHit = 0

    def enemybullet_hits_player(self):
        hits = pygame.sprite.spritecollide(self.player, enemybullet_group, True)
        if hits:
            self.lives -= 1
            if self.lives == 0:
                pygame.quit()
                sys.exit()

    def enemybullet_hits_meteor(self):
        hits = pygame.sprite.groupcollide(meteor_group, enemybullet_group, False, True)
        for i in hits:
            self.count_meteorHit += 1
            if self.count_meteorHit == 6:
                i.rect.x = random.randrange(0, s_width)
                i.rect.y = random.randrange(-600, -300)
                self.count_meteorHit = 0

    def create_lives(self):
        self.lives_img = pygame.image.load(player_ship)
        self.lives_img = pygame.transform.scale(self.lives_img, (25,25))
        n = 0
        for i in range(self.lives):
            screen.blit(self.lives_img, (10+n, s_height-50))
            n += 40

    def run_update(self):
        sprite_group.draw(screen)
        sprite_group.update()

    def run_game(self):
        self.create_background()
        self.create_sun()
        self.create_moon()
        self.create_player()
        self.create_enemy()
        self.create_meteor()
        while True:
            screen.fill('black')
            self.playerbullet_hits_enemy()
            self.playerbullet_hits_meteor()
            self.enemybullet_hits_player()
            self.enemybullet_hits_meteor()
            self.create_lives()
            self.run_update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    self.player.shoot()

                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            clock.tick(FPS)

def main():
    game = Game()

if __name__ == '__main__':
    main()