import pygame as pg
from config import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img_right = pg.image.load(f'img/player images/player{num}.png')
            img_right = pg.transform.scale(img_right, (150, 300))
            img_left = pg.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.vel = vec(0, 5)
        self.pos = vec(x, y) * TILESIZE
        self.direction = 0
        self.jumped = False


    def get_keys(self):
        self.vel = vec(0, 5)
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
            self.counter += 1
            self.direction = -1

        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
            self.counter += 1
            self.direction = 1

        if keys[pg.K_UP] and self.jumped == False:
            self.jumped = True
            self.pos.y -= 200
        if not keys[pg.K_UP]:
            self.jumped = False

        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
        if keys[pg.K_LEFT] == False and keys[pg.K_RIGHT] == False:
            self.counter = 9
            self.index = 0
            self.image = self.images_right[self.index]

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

        #gravidade
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if not hits:
            self.vel.y += 5
            if self.vel.y > 30:
                self.vel.y = 30
            self.pos.y += self.vel.y

        #animation
        if self.counter > 10:
            self.index += 1
            self.counter = 0
        if self.index >= len(self.images_right):
            self.index = 1
        if self.direction == 1:
            self.image = self.images_right[self.index]
        if self.direction == -1:
            self.image = self.images_left[self.index]

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Dialogo:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        caixa_de_dialogo = pg.image.load('img/caixa de dialogo.png')
        self.screen.blit(caixa_de_dialogo, (140, 20))

        sysf = pg.font.SysFont('bold', 50)
        fala1 = sysf.render('Diego é Diego', 0, (255, 100, 100))
        x, y = caixa_de_dialogo.get_rect().centerx, caixa_de_dialogo.get_rect().centery
        self.screen.blit(fala1, (x, y))

class Fundo(pg.sprite.Sprite):

    def __init__(self, game):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load('img/fundo.jpg')
