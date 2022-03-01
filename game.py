import pygame
import random
import sys


pygame.init()
SIZE = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('ПИНГ-ПОНГ вышибала')

all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
kill_borders = pygame.sprite.Group()
balls = pygame.sprite.Group()
bricks = pygame.sprite.Group()


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.choice((-6, -5, -4, 4, 5, 6))
        self.vy = random.choice((-6, -5, -4, 4, 5, 6))
        self.add(balls)
        

    def update(self):
        if play_go:
            self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if pygame.sprite.spritecollideany(self, kill_borders):
            self.kill()
        spr = pygame.sprite.spritecollide(self, bricks, 0)
        for i in spr:
            i.hard = (-1, 0, 1)[i.hard]


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2, kill):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            if kill:
                self.add(kill_borders)
            else:
                self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            if kill:
                self.add(kill_borders)
            else:
                self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
            
            
class Brick(pygame.sprite.Sprite):
    ColorsBrick = ((0, 0, 255), (0, 255, 0), (255, 0, 0))
    
    def __init__(self, x, y, w, h, hard):
        super().__init__(all_sprites)
        self.add(bricks)
        self.image = pygame.Surface((w, h))
        self.image.fill(self.ColorsBrick[hard])
        self.b1 = Border(x, y, x + w -1, y, 0)
        self.b2 = Border(x, y, x, y + h - 1, 0)
        self.b3 = Border(x, y + h - 1, x + w - 1, y + h - 1, 0)
        self.b4 = Border(x + w - 1, y, x + w - 1, y + h - 1, 0)
        self.rect = pygame.Rect(x, y, w, h)
        self.vx = x
        self.vy = y
        self.hard = hard
        
    def update(self):
        global N_bricks
        if self.hard == -1:
            self.b1.kill()
            self.b2.kill()
            self.b3.kill()
            self.b4.kill()
            self.kill()

        else:
            self.image.fill(self.ColorsBrick[self.hard])


class Racket:
    def __init__(self, dl):
        self.b1 = Border(1, HEIGHT - 20, dl, HEIGHT - 20, 0)
        self.b2 = Border(1, HEIGHT - 20, 1, HEIGHT - 10, 0)
        self.b3 = Border(dl, HEIGHT - 20, dl, HEIGHT - 10, 0)
        self.x = 1
        self.x1 = (dl + 1) // 2
        self.y = HEIGHT - 20
        self.dl = dl
        self.move(WIDTH // 2 - self.x1 + 1)
    
    
    def move(self, x):
        self.x1 += x - self.x
        self.x = x
        self.b1.rect.x = x
        self.b2.rect.x = x
        self.b3.rect.x = x + self.dl - 1
        pygame.mouse.set_pos([self.x1, self.y])
    


def new_play():
    
    for i in balls:
        i.kill()
    for i in bricks:
        i.kill()
    rackt.move((WIDTH - rackt.dl) // 2)    
    Ball(10, rackt.x1 - 10,  rackt.y - 21)
    play_go = 0
    N_balls = 3
    for i in range(7):
        Brick(50 + i * 60, 50, 60, 15, random.randint(0, 2))
    for i in range(7):
        Brick(30 + i * 60, 50 + 15, 60, 15, random.randint(0, 2))
    for i in range(7):
        Brick(40 + i * 60, 50 + 30, 60, 15, random.randint(0, 2))
    N_bricks = 21
    return play_go, N_balls, N_bricks


def terminate():
    pygame.quit()
    sys.exit()
    
    
def start_screen():
    intro_text = ["Добро пожаловать в ИГРУ", "Пинг-понг вышибала или разбей кирпич",
                  "", "", "", "", "", "", "", "",
                  "Для продолжения  нажми на любую кнопку", "или кликни мышью"]

    fon = pygame.Surface((WIDTH, HEIGHT))
    fon.fill(pygame.Color('#79b6fc'))
    pygame.draw.rect(fon, (255, 0, 0), (5, 5, WIDTH - 10, HEIGHT - 10), 1)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, (0, 0, 0))
        intro_rect = string_rendered.get_rect()
        text_x = WIDTH // 2 - string_rendered.get_width() // 2
        text_coord += 10
        text_coord += intro_rect.height
        screen.blit(string_rendered,(text_x, text_coord))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)
        
        
def end_screen():
    text = ["ИГРА ОКОНЧЕНА", "",
            "", "", "", "", "", "", "", "",
            "Для продолжения  нажми на любую кнопку", "или кликни мышью"]
    if N_balls:
        text[2] = "Полный успех!!! Урррааааа!!!"
    else:
        text[2] = "Не огорчайтесь"
        text[3] = "Поробуйте еще"
        
    fon = pygame.Surface((WIDTH, HEIGHT))
    fon.fill(pygame.Color('#a3fc79'))
    pygame.draw.rect(fon, (255, 0, 0), (5, 5, WIDTH - 10, HEIGHT - 10), 1)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in text:
        string_rendered = font.render(line, 1, (0, 0, 0))
        intro_rect = string_rendered.get_rect()
        text_x = WIDTH // 2 - string_rendered.get_width() // 2
        text_coord += 10
        text_coord += intro_rect.height
        screen.blit(string_rendered,(text_x, text_coord))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)
        
        
rackt = Racket(WIDTH // 5)
Border(5, 5, WIDTH - 5, 5, 0)
Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5, 1)
Border(5, 5, 5, HEIGHT - 5, 0)
Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5, 0)    
fps = 50 # количество кадров в секунду
clock = pygame.time.Clock()
running = True
start_screen()
play_go, N_balls, N_bricks = new_play()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_go:
                play_go = 0
            else:
                play_go = 1
                pygame.mouse.set_pos([rackt.x1, rackt.y])
        if event.type == pygame.MOUSEMOTION:
            if play_go:
                x = event.pos[0] - rackt.x1 + rackt.x
                x = 6 if x < 6 else x if x < WIDTH - rackt.dl - 5 else WIDTH - rackt.dl - 5
                rackt.move(x)
    screen.fill((255, 255, 255))
    
    all_sprites.draw(screen)
    all_sprites.update()
    
    clock.tick(fps)  
    pygame.display.flip()
    
    if not bricks:
        end_screen()
        play_go, N_balls, N_bricks = new_play()
    if not balls:
        if N_balls:
            N_balls -= 1
            play_go = 0
            
            Ball(10, rackt.x1 - 10,  rackt.y - 21)
        else:
            end_screen()
            play_go, N_balls, N_bricks = new_play()
        
        pygame.display.flip()

pygame.quit()

