import os
import pygame as pg
import random
import sys
import time
import math


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP: (0, -5),
         pg.K_DOWN: (0, +5),
         pg.K_LEFT: (-5, 0),
         pg.K_RIGHT: (+5, 0),
         }

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if obj_rct.left < WIDTH*2/5 or WIDTH*3/5 < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    
    return yoko,tate

class Bird:
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0),
    }
    img0 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    img = pg.transform.flip(img0, True, False)  # デフォルトのこうかとん（右向き）
    imgs = {  # 0度から反時計回りに定義
        (+5, 0): img,  # 右
        (+5, -5): pg.transform.rotozoom(img, 45, 0.9),  # 右上
        (0, -5): pg.transform.rotozoom(img, 90, 0.9),  # 上
        (-5, -5): pg.transform.rotozoom(img0, -45, 0.9),  # 左上
        (-5, 0): img0,  # 左
        (-5, +5): pg.transform.rotozoom(img0, 45, 0.9),  # 左下
        (0, +5): pg.transform.rotozoom(img, -90, 0.9),  # 下
        (+5, +5): pg.transform.rotozoom(img, -45, 0.9),  # 右下
    }

    def __init__(self, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数 xy：こうかとん画像の初期位置座標タプル
        """
        self.img = __class__.imgs[(+5, 0)]
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy
        self.has_barrier = False
        self.is_invincible = False

    def change_img(self, num: int, screen: pg.Surface):
        """
        こうかとん画像を切り替え，画面に転送する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 screen：画面Surface
        """
        self.img = pg.transform.rotozoom(pg.image.load(f"fig/{num}.png"), 0, 0.9)
        screen.blit(self.img, self.rct)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
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

        if self.has_barrier:
            self.activate_barrier(screen)
        if self.is_invincible:
            self.activate_invincibility(screen)

    def activate_barrier(self, screen):
        pg.draw.circle(screen, (0, 0, 255), self.rct.center, self.rct.width, width=5)

    def activate_invincibility(self, screen):
        pg.draw.circle(screen, (255, 215, 0), self.rct.center, self.rct.width, width=5)


def gameover(screen):
    black = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(black, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    black.set_alpha(100)
    screen.blit(black, (0, 0))
    cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.2)
    cry_rct = cry_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(cry_img, cry_rct)
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (0, 150, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH // 2, HEIGHT // 2
    screen.blit(txt, txt_rct)
    pg.display.update()
    time.sleep(5)

def enemy(num, screen: pg.surface):
    if num == 1:
        en_img1 = pg.transform.rotozoom(pg.image.load("fig/DQMJ2.webp"), 0, 0.6)
        en_rct1 = en_img1.get_rect()
        en_rct1.centerx = 150
        en_rct1.centery = HEIGHT/2
        screen.blit(en_img1,en_rct1)
        

    elif num == 2:
        en_img2 = pg.transform.rotozoom(pg.image.load("fig/en1.png"), 0, 0.4)
        en_rct2 = en_img2.get_rect()
        en_rct2.centerx = WIDTH-150
        en_rct2.centery = HEIGHT/2
        screen.blit(en_img2,en_rct2)
        stage2()

    elif num == 3:
        en_img3 = pg.transform.rotozoom(pg.image.load("fig/en5.png"),0,1)
        en_img4 = pg.transform.rotozoom(pg.image.load("fig/en6.png"),0,1)
        en_rct3 = en_img3.get_rect()
        en_rct3.centerx = 150
        en_rct3.centery = HEIGHT/2
        en_rct4 = en_img4.get_rect()
        en_rct4.centerx = WIDTH-150
        en_rct4.centery = HEIGHT/2
        screen.blit(en_img3,en_rct3)
        screen.blit(en_img4,en_rct4)
        stage3()

    elif num == 4:
        en_img5 = pg.transform.rotozoom(pg.image.load("fig/en7.png"),0,0.6)
        en_rct5 = en_img5.get_rect()
        en_rct5.centerx = 150
        en_rct5.centery = HEIGHT/2
        screen.blit(en_img5,en_rct5)
        stageEX()


def stage1(bird_rct, screen, tmr):
    global bombs
    bomb_speed = 10 # 弾の速度

    if tmr % (50 * 3) == 0:
        bombs = []
        center_x = 150  # 弾幕の中心X座標（敵から）
        center_y = HEIGHT // 2  # 弾幕の中心Y座標（画面中央）
        num_bombs = 7 # 三日月状の弾の数
        angle_offset = math.radians(15)  # 各弾の角度間隔

        for i in range(num_bombs):
            angle = math.pi + angle_offset * (i - num_bombs // 2)
            vx = bomb_speed * math.cos(angle)*-1
            vy = bomb_speed * math.sin(angle)
            bomb = {
                "rect": pg.Rect(center_x, center_y, 15, 15),  # 弾の矩形（小さい円形）
                "vx": vx,
                "vy": vy
            }
            bombs.append(bomb)

    # 各弾の位置を更新し、画面に描画する
    for bomb in bombs[:]:
        bomb["rect"].move_ip(bomb["vx"], bomb["vy"])
        pg.draw.ellipse(screen, (255, 0, 0), bomb["rect"])

        # こうかとんと弾の衝突判定
        if bird_rct.colliderect(bomb["rect"]):
            gameover(screen)

        # 画面外に出た弾をリストから削除
        if not screen.get_rect().colliderect(bomb["rect"]):
            bombs.remove(bomb)

def stage2():
    return 0

def stage3():
    return 0

def stageEX():
    return 0

def timescore():
    return 0



def main():
    pg.display.set_caption("避けろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.transform.rotozoom(pg.image.load("fig/bg.jpg"), 0, 1.0)    
    bird = Bird([WIDTH / 2, HEIGHT / 2])
    stage = 1
    start_time = time.time()
    
    clock = pg.time.Clock()
    tmr = 0
    while True:
        elapsed_time = time.time() - start_time
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        bird.update(key_lst, screen)

        # 30秒後にバリアが有効、60秒後に無敵が有効
        if elapsed_time > 30 and not bird.has_barrier:
            bird.has_barrier = True
        if elapsed_time > 60 and not bird.is_invincible:
            bird.is_invincible = True

        enemy(stage, screen)
        if stage == 1:
            stage1(bird.rct, screen, tmr)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
# a

