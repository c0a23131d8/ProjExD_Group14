import os
import pygame as pg
import random
import sys
import time
import math

WIDTH, HEIGHT = 1100, 650

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Ball:
    def __init__(self, pos: tuple[int, int], target_pos: tuple[int, int]):
        self.image = pg.transform.rotozoom(pg.image.load("fig/ball.png"), 0, 0.1)
        self.rect = self.image.get_rect(center=pos)

        # こうかとんに向かって進むようにするための速度を計算
        dx, dy = target_pos[0] - pos[0], target_pos[1] - pos[1]
        distance = math.hypot(dx, dy)
        self.speed = (dx / distance * 5, dy / distance * 5)  # 速度の正規化

    def update(self, screen: pg.Surface):
        """
        ボールを画面内で移動させる
        """
        self.rect.move_ip(self.speed)
        screen.blit(self.image, self.rect)

        # 画面外に出たボールを削除
        if self.rect.left > WIDTH or self.rect.right < 0 or self.rect.top > HEIGHT or self.rect.bottom < 0:
            return False  # 削除フラグ
        return True


def check_bound(obj_rct: pg.rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if obj_rct.left < WIDTH*2/5 or WIDTH*3/5 < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    
    return yoko, tate

class Bird:
    delta = {  
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0),
    }
    img0 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    img = pg.transform.flip(img0, True, False)  
    imgs = {  
        (+5, 0): img,  
        (+5, -5): pg.transform.rotozoom(img, 45, 0.9),  
        (0, -5): pg.transform.rotozoom(img, 90, 0.9),  
        (-5, -5): pg.transform.rotozoom(img0, -45, 0.9),  
        (-5, 0): img0,  
        (-5, +5): pg.transform.rotozoom(img0, 45, 0.9),  
        (0, +5): pg.transform.rotozoom(img, -90, 0.9),  
        (+5, +5): pg.transform.rotozoom(img, -45, 0.9),  
    }

    def __init__(self, xy: tuple[int, int]):
        self.img = __class__.imgs[(+5, 0)]
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy

    def change_img(self, num: int, screen: pg.Surface):
        self.img = pg.transform.rotozoom(pg.image.load(f"fig/{num}.png"), 0, 0.9)
        screen.blit(self.img, self.rct)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rct.move_ip(sum_mv)
        if check_bound(self.rct) != (True, True):
            self.rct.move_ip(-sum_mv[0], -sum_mv[1])
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.imgs[tuple(sum_mv)]
        screen.blit(self.img, self.rct)

def gameover(screen):
    black = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(black, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    black.set_alpha(100)
    screen.blit(black, (0, 0))
    cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.2)
    cry_rct = cry_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(cry_img, cry_rct)
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("GameOver", True, (0, 150, 255))
    txt_rct = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(txt, txt_rct)
    pg.display.update()
    time.sleep(5)

def stage2(screen: pg.Surface, bird: Bird, balls: list):###########################st02
    # イデアの画像を表示
    idea_img = pg.transform.rotozoom(pg.image.load("fig/en1.png"), 0, 0.5)
    idea_rect = idea_img.get_rect(center=(WIDTH - 100, HEIGHT // 2)) 
    screen.blit(idea_img, idea_rect)

    # こうかとんに向かってボールを発射
    if random.random() < 0.25:  # 50%の確率で新しいボールを生成
        ball = Ball(idea_rect.center, bird.rct.center)  # 左端のイデアの位置からこうかとんに向かって発射
        balls.append(ball)

    # ボールを更新し、画面に表示する
    for ball in balls[:]:
        if not ball.update(screen):
            balls.remove(ball)  # 画面外に出たボールをリストから削除
        if ball.rect.colliderect(bird.rct):
            gameover(screen)  # 衝突時にゲームオーバー
            return

def main():
    pg.display.set_caption("避けろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.transform.rotozoom(pg.image.load("fig/bg.png"), 0, 1.9)
    bird = Bird([WIDTH / 2, HEIGHT / 2])
    
    clock = pg.time.Clock()
    tmr = 0
    balls = []  # ボールのリスト

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        bird.update(key_lst, screen)
        stage2(screen, bird, balls)  # stage2にscreen, bird, ballsを渡す

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
