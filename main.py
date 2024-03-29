import sys
import random
import pygame
from pygame.locals import *

pygame.init()


planet = ['assets/images/sun.jpg', 'assets/images/moon.jpg', 'assets/images/earth.jpg',]
player_ship = 'assets/images/playership.png'
enemy_ship = 'assets/images/enemyship1.png'
enemy_ship2 = 'assets/images/enemyship3.png'
meteor = 'assets/images/meteor.png'
player_bullet = 'assets/images/pbullet.png'
enemy_bullet = 'assets/images/ebullet.png'
enemy_bullet2 = 'assets/images/ebullet2.png'



shoot_sound = pygame.mixer.Sound('assets/sounds/laser.wav')
explosion_sound = pygame.mixer.Sound('assets/sounds/explosion.wav')
sun_sound = pygame.mixer.Sound('assets/sounds/play.wav')
game_over = pygame.mixer.Sound('assets/sounds/game_over.wav')
pause_sound = pygame.mixer.Sound('assets/sounds/pause.wav')
start_screen = pygame.mixer.Sound('assets/sounds/creepy.wav')
end_music = pygame.mixer.Sound('assets/sounds/creepy2.wav')

start_sound = pygame.mixer.music.load('assets/sounds/space.wav')

pygame.mixer.init()


screen = pygame.display.set_mode((0,0), FULLSCREEN)
s_width, s_height = screen.get_size()

clock = pygame.time.Clock()
FPS = 60

background_group = pygame.sprite.Group()
planet_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy2_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
playerbullet_group = pygame.sprite.Group()
enemybullet_group = pygame.sprite.Group()
enemybullet2_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

pygame.mouse.set_visible(False)
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
        self.alive = True
        self.count_to_lives = 0
        self.activate_bullet = True
        self.alpha_duration = 0

    def update(self):
        if self.alive:
            self.image.set_alpha(80)
            self.alpha_duration += 1
            if self.alpha_duration > 160:
                self.image.set_alpha(255)
            mouse = pygame.mouse.get_pos()
            self.rect.x = mouse[0] - 9
            self.rect.y = mouse[1] + 10
        else:
            self.alpha_duration = 0
            exp_x = self.rect.x + 25
            exp_y = self.rect.y + 25
            explosion = Explosion(exp_x, exp_y)
            explosion_group.add(explosion)
            sprite_group.add(explosion)
            pygame.time.delay(20)
            self.rect.y = s_height + 400
            self.count_to_lives += 1
            if self.count_to_lives > 50:
                self.alive = True
                self.count_to_lives = 0
                self.activate_bullet = True


    def shoot(self):
        if self.activate_bullet:
            bullet = PlayerBullet(player_bullet)
            mouse = pygame.mouse.get_pos()
            bullet.rect.x = mouse[0]
            bullet.rect.y = mouse[1]
            playerbullet_group.add(bullet)
            sprite_group.add(bullet)

    def dead(self):
        self.alive = False
        self.activate_bullet = False

class Enemy(Player):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = random.randrange(50, s_width - 50)
        self.rect.y = random.randrange(-500, 0)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y += 1
        if self.rect.y > s_height:
            self.rect.x = random.randrange(50, s_width - 50)
            self.rect.y = random.randrange(-500, 0)
        self.shoot()
    
    def shoot(self):
        if self.rect.y > 0:
            if self.rect.y % 100 == 0:
                enemybullet = EnemyBullet(enemy_bullet)
                enemybullet.rect.x = self.rect.x + 28
                enemybullet.rect.y = self.rect.y + 20
                enemybullet_group.add(enemybullet)
                sprite_group.add(enemybullet)

class Enemy2(Player):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = -1000
        self.rect.y = 50
        self.move = 1
        self.image.set_colorkey('white')
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.x += self.move
        if self.rect.x > s_width + 1000:
            self.move *= -1
        elif self.rect.x < - 1000:
            self.move *= -1
        self.shoot()
    
    def shoot(self):
        if self.rect.x > 0:
            if self.rect.x % 30 == 0:
                enemybullet2 = EnemyBullet2(enemy_bullet2)
                enemybullet2.rect.x = self.rect.x + 95
                enemybullet2.rect.y = self.rect.y + 160
                enemybullet2_group.add(enemybullet2)
                sprite_group.add(enemybullet2)


class Meteor(Enemy):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = random.randrange(20, s_width - 20)
        self.rect.y = random.randrange(-900, -300)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y += 2
        if self.rect.y > s_height + 20:
            self.rect.x = random.randrange(20, s_width - 20)
            self.rect.y = random.randrange(-900, -300)

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('black')

    def update(self):
        self.rect.y -= 10
        if self.rect.y < 0:
            self.kill()

class EnemyBullet(PlayerBullet):
    def __init__(self, img):
        super().__init__(img)

    def update(self):
        self.rect.y += 3
        if self.rect.y > s_height:
            self.kill()

class EnemyBullet2(PlayerBullet):
    def __init__(self, img):
        super().__init__(img)
        self.image.set_colorkey('black')

    def update(self):
        self.rect.y += 4
        if self.rect.y > s_height:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.exp_list = []
        pygame.mixer.Sound.play(explosion_sound)
        for i in range(1, 5):
            exp = pygame.image.load(f'assets/images/exp{i}.png').convert()
            exp.set_colorkey('black')
            exp = pygame.transform.scale(exp, (120, 120))
            self.exp_list.append(exp)
        self.index = 0
        self.image = self.exp_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.count_delay = 0

    def update(self):
        self.count_delay += 1
        if self.count_delay >= 12:
            if self.index < len(self.exp_list) - 1 :
                self.count_delay = 0
                self.index += 1
                self.image = self.exp_list[self.index]
        if self.index >= len(self.exp_list) - 1 :
            if self.count_delay >= 12 :
                self.kill()

class Game: 
    def __init__(self):
        self.count_enemyHit = 0
        self.count_enemyHit2 = 0
        self.count_meteorHit = 0
        self.lives = 3
        self.score = 0
        self.level = 1
        self.init_create = True
        self.play = 0
        self.gameOver_soundDelay = 0
        self.start_screen()

    def start_text(self):
        title = pygame.font.SysFont('Calibri', 70)
        text = title.render('SPACE WAR', True, 'white')
        text_rect = text.get_rect(center=(s_width/2, s_height/2))
        screen.blit(text, text_rect)
        
        instruction = pygame.font.SysFont('Calibri', 20)
        text = instruction.render('Press ENTER to start game...', True, 'red')
        text_rect = text.get_rect(center=(s_width/2, s_height/2 + 100))
        screen.blit(text, text_rect)

        instruction = pygame.font.SysFont('Calibri', 20)
        text = instruction.render('Press ESC to quit game...', True, 'red')
        text_rect = text.get_rect(center=(s_width/2, s_height/2 + 125))
        screen.blit(text, text_rect)

        instructionPause = pygame.font.SysFont('Calibri', 20)
        text = instructionPause.render('Press SPACE to pause/unpaused game...', True, 'red')
        text_rect = text.get_rect(center=(s_width/2, s_height/2 + 150))
        screen.blit(text, text_rect)


    def start_screen(self):
        pygame.mixer.Sound.stop(end_music)
        pygame.mixer.Sound.play(start_screen)
        self.lives = 3
        self.score = 0
        self.level = 1
        sprite_group.empty()
        background_group.empty()
        planet_group.empty()
        player_group.empty()
        enemy_group.empty()
        meteor_group.empty()
        playerbullet_group.empty()
        enemybullet_group.empty()
        explosion_group.empty()
        while True:
            screen.fill('black')
            self.start_text()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_RETURN:
                        pygame.mixer.Sound.stop(start_screen)
                        self.run_game()

            pygame.display.update()


    def pause_text(self):
        pauseTitle = pygame.font.SysFont('Calibri', 50)
        text = pauseTitle.render('PAUSED', True, 'white')
        text_rect = text.get_rect(center=(s_width/2, s_height/2))
        screen.blit(text, text_rect)


    def pause_screen(self):
        pygame.mixer.music.pause()
        pygame.mixer.Sound.play(pause_sound)
        self.init_create = False
        while True:
            self.pause_text()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_SPACE:
                        pygame.mixer.music.unpause()
                        pygame.mixer.Sound.play(pause_sound)
                        self.run_game()

            pygame.display.update()

    
    def gameOver_text(self):
        gameOver = pygame.font.SysFont('Calibri', 70)
        text = gameOver.render('GAME OVER', True, 'red')
        text_rect = text.get_rect(center=(s_width/2, s_height/2))
        screen.blit(text, text_rect)

        score = pygame.font.SysFont('Calibri', 35)
        text = score.render('Final Score  ' + (str(self.score)), True, 'white')
        text_rect = text.get_rect(center=(s_width/2, s_height/2 + 75))
        screen.blit(text, text_rect)

        level = pygame.font.SysFont('Calibri', 25)
        text = level.render('Level ' + (str(self.level)), True, 'green')
        text_rect = text.get_rect(center=(s_width/2, s_height/2 + 115))
        screen.blit(text, text_rect)

        gameOverinstr = pygame.font.SysFont('Calibri', 20)
        text = gameOverinstr.render('PRESS ENTER', True, 'white')
        text_rect = text.get_rect(center=(s_width/2, s_height/2 + 150))
        screen.blit(text, text_rect)


    def gameOver_screen(self):
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(game_over)
        while True:
            screen.fill('black')
            self.gameOver_text()
            self.gameOver_soundDelay += 1
            if self.gameOver_soundDelay > 1500:
                pygame.mixer.Sound.play(end_music)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.start_screen()

            pygame.display.update()


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
    
    def create_enemy2(self):
        for i in range(1):
            self.enemy2 = Enemy2(enemy_ship2)
            enemy2_group.add(self.enemy2)
            sprite_group.add(self.enemy2)

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
                self.score += 3
                exp_x = i.rect.x + 40
                exp_y = i.rect.y + 50
                explosion = Explosion(exp_x, exp_y)
                explosion_group.add(explosion)
                sprite_group.add(explosion)
                
                self.rect.y += 2
                i.rect.x = random.randrange(50, s_width - 50)
                i.rect.y = random.randrange(-600, -300)
                self.count_enemyHit = 0

    def playerbullet_hits_enemy2(self):
        hits = pygame.sprite.groupcollide(enemy2_group, playerbullet_group, False, True)
        for i in hits:
            self.count_enemyHit2 += 1
            if self.count_enemyHit2 == 50:
                self.score += 40
                exp_x = i.rect.x + 120
                exp_y = i.rect.y + 150
                explosion = Explosion(exp_x, exp_y)
                explosion_group.add(explosion)
                sprite_group.add(explosion)

                i.rect.x = -999
                self.count_enemyHit2 = 0

    def playerbullet_hits_meteor(self):
        hits = pygame.sprite.groupcollide(meteor_group, playerbullet_group, False, True)
        for i in hits:
            self.count_meteorHit += 1
            if self.count_meteorHit == 6:
                self.score += 5
                exp_x = i.rect.x + 60
                exp_y = i.rect.y + 70
                explosion = Explosion(exp_x, exp_y)
                explosion_group.add(explosion)
                sprite_group.add(explosion)

                i.rect.x = random.randrange(0, s_width)
                i.rect.y = random.randrange(-600, -300)
                self.count_meteorHit = 0

    def enemybullet_hits_player(self):
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, enemybullet_group, True)
            if hits:
                self.lives -= 1
                self.player.dead()
                if self.lives == 0:
                    self.gameOver_screen()

    def enemybullet_hits_meteor(self):
        hits = pygame.sprite.groupcollide(meteor_group, enemybullet_group, False, True)
        for i in hits:
            self.count_meteorHit += 1
            if self.count_meteorHit == 6:
                exp_x = i.rect.x + 60
                exp_y = i.rect.y + 70
                explosion = Explosion(exp_x, exp_y)
                explosion_group.add(explosion)
                sprite_group.add(explosion)
                i.rect.x = random.randrange(0, s_width)
                i.rect.y = random.randrange(-600, -300)
                self.count_meteorHit = 0

    def enemybullet2_hits_player(self):
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, enemybullet2_group, True)
            if hits:
                self.lives -= 1
                self.player.dead()
                if self.lives == 0:
                    self.gameOver_screen()

    def enemybullet2_hits_meteor(self):
        hits = pygame.sprite.groupcollide(meteor_group, enemybullet2_group, False, True)
        for i in hits:
            self.count_meteorHit += 1
            if self.count_meteorHit == 6:
                exp_x = i.rect.x + 60
                exp_y = i.rect.y + 70
                explosion = Explosion(exp_x, exp_y)
                explosion_group.add(explosion)
                sprite_group.add(explosion)
                i.rect.x = random.randrange(0, s_width)
                i.rect.y = random.randrange(-600, -300)
                self.count_meteorHit = 0

    def player_enemy_crash(self):
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, enemy_group, False)
            if hits:
                for i in hits:
                    self.score += 3
                    exp_x = i.rect.x + 40
                    exp_y = i.rect.y + 50
                    explosion = Explosion(exp_x, exp_y)
                    explosion_group.add(explosion)
                    sprite_group.add(explosion) 
                    i.rect.x = random.randrange(0, s_width)
                    i.rect.y = random.randrange(-600, -300)
                    self.lives -= 1
                    self.player.dead()
                    if self.lives == 0:
                        self.gameOver_screen()


    def player_enemy2_crash(self):
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, enemy2_group, False)
            if hits:
                for i in hits:
                    self.count_enemyHit2 =+ 20
                    exp_x = i.rect.x + 120
                    exp_y = i.rect.y + 150
                    explosion = Explosion(exp_x, exp_y)
                    explosion_group.add(explosion)
                    sprite_group.add(explosion) 
                    i.rect.x = -999
                    self.lives -= 1
                    self.player.dead()
                    if self.lives == 0:
                        self.gameOver_screen()

    def player_meteor_crash(self):
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, meteor_group, False)
            if hits:
                for i in hits:
                    self.score += 5
                    exp_x = i.rect.x + 60
                    exp_y = i.rect.y + 70
                    explosion = Explosion(exp_x, exp_y)
                    explosion_group.add(explosion)
                    sprite_group.add(explosion)
                    i.rect.x = random.randrange(0, s_width)
                    i.rect.y = random.randrange(-600, -300) 
                    self.lives -= 1
                    self.player.dead()
                    if self.lives == 0:
                        self.gameOver_screen()

    def create_lives(self):
        self.lives_img = pygame.image.load(player_ship)
        self.lives_img = pygame.transform.scale(self.lives_img, (25,25))
        n = 0
        for i in range(self.lives):
            screen.blit(self.lives_img, (10+n, s_height-50))
            n += 40

    def create_score(self):
        score = self.score
        font = pygame.font.SysFont('Calibri', 30)
        text = font.render(str(score), True, 'white')
        text_rect = text.get_rect(center=(25, 25))
        screen.blit(text, text_rect)

    def create_level(self):
        font = pygame.font.SysFont('Calibri', 30)
        text = font.render('Lvl ' + str(self.level), True, 'green')
        text_rect = text.get_rect(center=(s_width - 75, 25))
        screen.blit(text, text_rect)

    def run_update(self):
        sprite_group.draw(screen)
        sprite_group.update()

    def run_game(self):
        if self.init_create:
            pygame.mixer.music.play(-1)
            self.create_background()
            self.create_sun()
            self.create_moon()
            self.create_player()
            self.create_enemy()
        while True:
            screen.fill('black')
            self.playerbullet_hits_enemy()
            self.playerbullet_hits_enemy2()
            self.playerbullet_hits_meteor()
            self.enemybullet_hits_player()
            self.enemybullet2_hits_player()
            self.enemybullet_hits_meteor()
            self.enemybullet2_hits_meteor()
            self.player_enemy_crash()
            self.player_enemy2_crash()
            self.player_meteor_crash()
            self.run_update()
            self.create_lives()
            self.create_score()
            self.create_level()
            if self.score >= 100 and self.level == 1:
                self.create_meteor()
                self.create_enemy2()
                self.level += 1
            elif self.score >= 300 and self.level == 2:
                self.level += 1
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    pygame.mixer.Sound.play(shoot_sound)
                    self.player.shoot()

                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_SPACE:
                        self.pause_screen()

            pygame.display.update()
            clock.tick(FPS)

def main():
    game = Game()

if __name__ == '__main__':
    main()