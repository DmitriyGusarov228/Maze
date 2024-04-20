from pygame import *
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, size_x, size_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = speed
        self.size_x = size_x
        self.size_y = size_y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < (700 - 5 - self.size_x):
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < (500 - 5 - self.size_x):
            self.rect.y += self.speed

class Enemy(GameSprite):
    direction = 'left'
    def update(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        if self.rect.x <= 400:
            self.direction = 'right'
        if self.rect.x >= 600:
            self.direction = 'left'

class Wall(sprite.Sprite):  
    def __init__(self,  color1, color2, color3, wall_x, wall_y, wall_width, wall_height):  
        super().__init__()  
        self.color1 = color1  
        self.color2 = color2  
        self.color3 = color3  
        self.width = wall_width  
        self.height = wall_height  
        self.image = Surface((self.width, self.height)) 
        self.image.fill((color1, color2, color3))  
        self.rect = self.image.get_rect()  
        self.rect.x = wall_x  
        self.rect.y = wall_y  
    def draw_wall(self):  
        window.blit(self.image, (self.rect.x, self.rect.y))  

window = display.set_mode((700, 500))
display.set_caption('Лабиринт')
background = transform.scale(image.load('background.jpg'), (700, 500))
player = Player('hero.png', 10, 440, 50, 50, 5)
cyborg = Enemy('cyborg.png', 400, 300, 50, 50, 5)
treasure = GameSprite('treasure.png', 600, 100, 50, 50, 0)
wall1 = Wall(130, 223, 143, 100, 490, 500, 10)
wall2 = Wall(130, 223, 143, 100, 10, 500, 10)
wall3 = Wall(130, 223, 143, 500, 10, 10, 400)
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
font.init()
font = font.SysFont('Arial', 70)
win = font.render(
    'YOU WIN!', True, (255, 215, 0)
)
lose = font.render(
    'YOU LOSE!', True, (255, 215, 0)
)

game = True
FPS = 60
clock = time.Clock()

while game:
    window.blit(background, (0, 0))
    player.reset()
    player.update()
    cyborg.reset()
    cyborg.update()
    treasure.reset()
    wall1.draw_wall()
    wall2.draw_wall()
    wall3.draw_wall()

    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if sprite.collide_rect(player, cyborg) or sprite.collide_rect(player, wall1) or sprite.collide_rect(player, wall2) or sprite.collide_rect(player, wall3):
        window.blit(lose, (200, 200))
        mixer.music.load('kick.ogg')
        mixer.music.play()
        game = False

    if sprite.collide_rect(player, treasure):
        window.blit(win, (200, 200))
        mixer.music.load('money.ogg')
        mixer.music.play()
        game = False

    clock.tick(FPS)
    display.update()