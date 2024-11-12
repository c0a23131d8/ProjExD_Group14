import os
import pygame as pg
import random
import sys
import time
import pygame
import math



WIDTH, HEIGHT = 1100, 650
start_time = None  
time_limit = 50
DELTA = {pg.K_UP: (0, -5),
         pg.K_DOWN: (0, +5),
         pg.K_LEFT: (-5, 0),
         pg.K_RIGHT: (+5, 0),
         }

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
    
# ボールとこうかとんの円形当たり判定を実装
def is_colliding(circle1, circle2):
    # 2つの円の中心間の距離を計算
    distance = math.hypot(circle1.centerx - circle2.centerx, circle1.centery - circle2.centery)
    # 2つの円の半径の合計が距離以下であれば衝突
    return distance <= (circle1.width / 2 + circle2.width / 2) * 0.8

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
    pg.quit()
    sys.exit() 

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
        stage3(screen,en_rct3,en_rct4)

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

def stage2(screen: pg.Surface, bird: Bird, balls: list):
    # 8%の確率で新しいボールを生成する
    if random.random() < 0.08:
        # ボールの発射位置を画面右端の上下50ピクセル以内でランダムに設定
        launch_y = HEIGHT // 2 + random.randint(-50, 50)
        # 新しいボールを生成し、こうかとんの中心をターゲットに設定
        ball = Ball((WIDTH - 100, launch_y), bird.rct.center)
        # ボールリストに生成したボールを追加
        balls.append(ball)
    for ball in balls[:]:
        if not ball.update(screen):
            balls.remove(ball)
        if is_colliding(ball.rect, bird.rct):
            gameover(screen)
            return

def stage3(screen, en_rct3, en_rct4):
    global bird, bombs  # main関数で定義されたbirdとbombsを参照

    bomb_speed = 8       # 弾の速度
    num_bombs = 1       # 円形に配置する弾の数
    angle_offset = 2 * math.pi / num_bombs  # 各弾の角度間隔
    last_angle_change =9000
    # 5秒ごとに基準角度を変えるための処理
    if time.time() - last_angle_change >= 5:
        base_angle = random.uniform(0, 2 * math.pi)  # ランダムな基準角度を生成
        last_angle_change = time.time()  # 最後に角度を変えた時間を更新

    # 敵から円形に弾を発射
    for en_rct in [en_rct3, en_rct4]:
        center_x, center_y = en_rct.center
        for i in range(num_bombs):
            angle = base_angle + angle_offset * i  # 基準角度を元に弾の角度を計算
            vx = bomb_speed * math.cos(angle)
            vy = bomb_speed * math.sin(angle)
            bomb = {
                "rect": pg.Rect(center_x, center_y, 30, 30),  # 弾の矩形
                "vx": vx,
                "vy": vy
            }
            bombs.append(bomb)  # 生成した弾をbombsリストに追加

    # 各弾の位置を更新し、画面に描画
    for bomb in bombs[:]:  # bombsリストを走査
        bomb["rect"].move_ip(bomb["vx"], bomb["vy"])  # 弾を移動
        pg.draw.ellipse(screen, (255, 0, 0), bomb["rect"])  # 弾を描画

        # こうかとんと弾の衝突判定
        if bird.rct.colliderect(bomb["rect"]):
            if not bird.is_invincible:  # 無敵モードでないときのみゲームオーバー
                gameover(screen)
                return

        # 画面外に出た弾をリストから削除
        if not screen.get_rect().colliderect(bomb["rect"]):
            bombs.remove(bomb)

    # こうかとん（プレイヤーキャラクター）を再描画
    screen.blit(bird.img, bird.rct)

    return last_angle_change  # 更新した角度変更時間を返す

def stageEX():
    global game_over, circle_bomb_timer, random_bomb_timer, cross_bomb_timer, chase_bomb_timer
    clock = pygame.time.Clock()

    running = True

    pygame.init()

    # 背景画像の読み込み
    background_image = pygame.image.load("fig/bg.jpg")  # 背景画像
    background_width, background_height = background_image.get_size()

    # 画面サイズを背景画像のサイズに設定
    WIDTH, HEIGHT = 1100 , 650
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("StageEX")

    # 色の設定
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    PURPLE = (128, 0, 128)  # 円形爆弾の色
    GREEN = (0, 255, 0)  # ランダム生成の爆弾の色
    BLUE = (0, 0, 255)  # 追尾弾の色

    # ボスキャラの画像の読み込みとサイズ変更
    boss_image = pygame.image.load("fig/en7.png")
    boss_image = pygame.transform.scale(boss_image, (boss_image.get_width() // 4, boss_image.get_height() // 4))  # サイズをさらに小さく
    boss_rect = boss_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # プレイヤーキャラクターの画像の読み込みとサイズ変更
    player_image = pygame.image.load("fig/9.png")  # プレイヤーキャラクターの画像
    player_image = pygame.transform.scale(player_image, (30, 30))  # サイズを調整
    player_rect = player_image.get_rect(center=(WIDTH // 2, HEIGHT - 50))  # 初期位置を設定

    # 爆弾の設定
    BOMB_RADIUS = 10
    bombs = []
    chase_bombs = []  # 追尾弾のリスト

    # タイマーの初期化
    circle_bomb_timer = pygame.time.get_ticks()
    random_bomb_timer = pygame.time.get_ticks()
    cross_bomb_timer = pygame.time.get_ticks()
    chase_bomb_timer = pygame.time.get_ticks()

    # ゲームオーバーフラグ
    game_over = False
    font = pygame.font.SysFont(None, 55)

    # スコアの初期化
    score = 0
    start_time = pygame.time.get_ticks()  # ゲーム開始時刻

    def draw_circle_bomb(x, y):
        pygame.draw.circle(screen, PURPLE, (x, y), BOMB_RADIUS)  # 円形爆弾を紫に描画

    def draw_random_bomb(x, y):
        pygame.draw.circle(screen, GREEN, (x, y), BOMB_RADIUS)  # ランダム爆弾を緑に描画

    def draw_chase_bomb(x, y):
        pygame.draw.circle(screen, BLUE, (x, y), BOMB_RADIUS)  # 追尾弾を青に描画

    def draw_game_over():
        screen.fill(BLACK)
        text = font.render("Game Over", True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    def draw_score():
        text = font.render(f"Score: {score}", True, RED)
        screen.blit(text, (10, 10))  # スコアを画面の左上に描画

    while running:
        # 背景画像を描画
        screen.blit(background_image, (0, 0))
        
        # ボスキャラを描画
        screen.blit(boss_image, boss_rect)

        # 現在の時刻を取得
        current_time = pygame.time.get_ticks()

        # スコアを更新（経過時間に比例）
        elapsed_time = (current_time - start_time) // 1000  # 経過時間を秒単位で取得
        score = elapsed_time  # スコアを経過時間に設定

        # 円形に爆弾を飛ばす（5秒ごと）
        if current_time - circle_bomb_timer >= 3000:
            circle_bomb_timer = current_time
            for angle in range(0, 360, 45):  # 45度間隔で爆弾を配置
                rad = math.radians(angle)
                x = boss_rect.centerx + 100 * math.cos(rad)
                y = boss_rect.centery + 100 * math.sin(rad)
                bombs.append((x, y, 'circle'))  # 爆弾タイプを指定

        # ランダムな位置に爆弾を描画（0.5秒ごとに3個）
        if current_time - random_bomb_timer >= 500:  # 生成間隔を0.5秒に設定
            random_bomb_timer = current_time
            for _ in range(3):  # 3個生成
                while True:
                    x = random.randint(0, WIDTH)
                    y = random.randint(0, HEIGHT)
                    # ボスの領域内に生成されないか確認
                    if not boss_rect.collidepoint((x, y)):
                        bombs.append((x, y, 'random'))  # 爆弾タイプを指定
                        break

        # 十字型に爆弾を描画（3秒ごと）
        if current_time - cross_bomb_timer >= 3000:
            cross_bomb_timer = current_time
            for i in range(-200, 201, 50):
                bombs.append((boss_rect.centerx + i, boss_rect.centery, 'cross'))  # 爆弾タイプを指定
                bombs.append((boss_rect.centerx, boss_rect.centery + i, 'cross'))  # 爆弾タイプを指定

        # 追尾弾を生成（2秒ごとに10個）
        if current_time - chase_bomb_timer >= 2000:
            chase_bomb_timer = current_time
            for _ in range(10):  # 3つの追尾弾を生成
                chase_bombs.append([boss_rect.centerx, boss_rect.centery])  # ボスの位置から生成

        # 追尾弾の動き
        for chase_bomb in chase_bombs:
            # 追尾弾がプレイヤーの位置に向かって移動
            chase_bomb[0] += (player_rect.centerx - chase_bomb[0]) * 0.05  # X方向の移動
            chase_bomb[1] += (player_rect.centery - chase_bomb[1]) * 0.05  # Y方向の移動

        # 爆弾を描画し、プレイヤーとの接触を確認
        for bomb in bombs:
            if bomb[2] == 'circle':
                draw_circle_bomb(bomb[0], bomb[1])  # 円形爆弾を描画
            elif bomb[2] == 'random':
                draw_random_bomb(bomb[0], bomb[1])  # ランダム爆弾を描画
            
            # 爆弾とプレイヤーの当たり判定
            if player_rect.colliderect(pygame.Rect(bomb[0] - BOMB_RADIUS, bomb[1] - BOMB_RADIUS, BOMB_RADIUS * 2, BOMB_RADIUS * 2)):
                game_over = True

        # 追尾弾を描画し、プレイヤーとの接触を確認
        for chase_bomb in chase_bombs:
            draw_chase_bomb(chase_bomb[0], chase_bomb[1])  # 追尾弾を描画
            # 追尾弾とプレイヤーの当たり判定
            if player_rect.colliderect(pygame.Rect(chase_bomb[0] - BOMB_RADIUS, chase_bomb[1] - BOMB_RADIUS, BOMB_RADIUS * 2, BOMB_RADIUS * 2)):
                game_over = True

        # ボスキャラとプレイヤーの当たり判定
        if boss_rect.colliderect(player_rect):
            game_over = True

        # ゲームオーバーの処理
        if game_over:
            draw_game_over()
        else:
            # スコアを描画
            draw_score()

            # プレイヤーを描画
            screen.blit(player_image, player_rect)  # プレイヤー画像を描画

            # キーの状態をチェックして移動を行う
            keys = pygame.key.get_pressed()  # 押されているキーを取得
            if keys[pygame.K_UP]:
                player_rect.y -= 5  # 上に移動
            if keys[pygame.K_DOWN]:
                player_rect.y += 5  # 下に移動
            if keys[pygame.K_LEFT]:
                player_rect.x -= 5  # 左に移動
            if keys[pygame.K_RIGHT]:
                player_rect.x += 5  # 右に移動

            # プレイヤーが画面外に出ないように制限
            player_rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))  # 画面内に留まるように制限

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 画面を更新
        pygame.display.flip()
        clock.tick(60)  # フレームレートを設定（60 FPS）

    pygame.quit()


def timescore(screen, stage):
    global start_time
    if start_time is None:
        start_time = time.time() 

    spent_time = time.time() - start_time
    end_time = max(0, time_limit - spent_time)

    font = pg.font.Font(None, 36)
    time_text = font.render(f" Time : {int(end_time)} s", True, (255, 255, 255))
    screen.blit(time_text, (10, 10))

    # EXステージでのクリア表示
    if stage == 4 and end_time <= 0:
        black_scr = pg.Surface((WIDTH, HEIGHT))
        pg.draw.rect(black_scr, (0, 0, 0), black_scr.get_rect())
        black_scr.set_alpha(180)
        screen.blit(black_scr, (0, 0))

        kk_img = pg.transform.rotozoom(pg.image.load("fig/6.png"), 0, 0.9)
        kk_rct = kk_img.get_rect()
        kk_rct.center = WIDTH / 2 + 200, HEIGHT / 2
        screen.blit(kk_img, kk_rct)
        kk_rct.center = WIDTH / 2 - 200, HEIGHT / 2
        screen.blit(kk_img, kk_rct)

        clear_font = pg.font.Font(None, 80)
        clear_text = clear_font.render("Game clear!!", True, (255, 0, 0))
        clear_rect = clear_text.get_rect()
        clear_rect.center = WIDTH / 2, HEIGHT / 2
        screen.blit(clear_text, clear_rect)
        pg.display.update()

        time.sleep(3)
        pg.quit()
        sys.exit() 

    elif end_time <= 0:
        black_scr = pg.Surface((WIDTH, HEIGHT))
        black_scr.fill((0, 0, 0))
        black_scr.set_alpha(180)
        screen.blit(black_scr, (0, 0))
    
        msg_font = pg.font.Font(None, 40)
        msg_text = msg_font.render("Press 'N' to proceed to the next stage", True, (255, 255, 255))
        msg_rect = msg_text.get_rect()
        msg_rect.center = WIDTH / 2, HEIGHT / 2
        screen.blit(msg_text, msg_rect)
        pg.display.update()

        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN and event.key == pg.K_n:
                    waiting = False
                    start_time = None

        return stage + 1

    return stage

def main():
    global bird,bombs # birdをグローバル変数として定義
    pg.display.set_caption("避けろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.transform.rotozoom(pg.image.load("fig/bg.jpg"), 0, 1.0)    
    bird = Bird([WIDTH / 2, HEIGHT / 2])
    stage = 3
    start_time = time.time()
    bombs = []  # ボムのリスト
    
    clock = pg.time.Clock()
    tmr = 0
    balls = []  # ボールのリスト

    while True:
        elapsed_time = time.time() - start_time
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        bird.update(key_lst, screen)

        # 20秒後にバリアが有効、40秒後に無敵が有効
        if elapsed_time > 20 and not bird.has_barrier:
            bird.has_barrier = True
        if elapsed_time > 40 and not bird.is_invincible:
            bird.is_invincible = True

        enemy(stage, screen)
        if stage == 1:
            stage1(bird.rct, screen, tmr)
        elif stage == 2:
            bird.has_barrier = False
            bird.is_invincible = False
            stage2(screen,bird,balls)
        elif stage == 3:
            bird.has_barrier = False
            bird.is_invincible = False
        elif stage == 4:
            bird.has_barrier = False
            bird.is_invincible = False
            stageEX()

        sum_mv = [0, 0]

        bird.update(key_lst, screen)
        enemy(stage,screen)
        stage = timescore(screen, stage)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()


