# 弾避けゲーム

## 実行環境の必要条件
* python >= 3.10
* pygame >= 2.1

## ゲームの概要
* こうかとんが限られた範囲で弾を避ける


## ゲームの遊び方
* 矢印キーでこうかとんを操作
* 制限時間内で弾に当たらないように避ける

## ゲームの実装
### 共通基本機能
* 背景画像と主人公キャラクターの描画
* 移動範囲制限
* 敵キャラの位置固定
* 制限時間とスコア



### 分担追加機能
* ステージ1弾幕
* ステージ2弾幕
def stage2(screen: pg.Surface, bird: Bird, balls: list):  ###########################st02
    # イデアの画像を表示
    idea_img = pg.transform.rotozoom(pg.image.load("fig/en1.png"), 0, 0.5)  # イデアの画像を読み込み、サイズを0.5倍に縮小
    idea_rect = idea_img.get_rect(center=(WIDTH - 100, HEIGHT // 2))  # イデアの画像を画面の右側に中央配置
    screen.blit(idea_img, idea_rect)  # イデアの画像を画面に描画

    # こうかとんに向かってボールを発射
    if random.random() < 0.25:  # 25%の確率で新しいボールを生成
        ball = Ball(idea_rect.center, bird.rct.center)  # 左端のイデアの位置からこうかとんの位置へ向けてボールを発射
        balls.append(ball)  # 発射したボールをボールのリストに追加

    # ボールを更新し、画面に表示する
    for ball in balls[:]:  # ボールのリストをコピーしてループ（リストを変更する場合のため）
        if not ball.update(screen):  # ボールを更新し、画面に描画。画面外に出た場合はFalseを返す
            balls.remove(ball)  # 画面外に出たボールをリストから削除
        if ball.rect.colliderect(bird.rct):  # ボールがこうかとんに衝突したかチェック
            gameover(screen)  # 衝突時にゲームオーバー画面を表示
            return  # ゲームオーバーの場合は関数を終了

            
* ステージ3弾幕
* 制限時間設定
* 弾避け機能


### ToDo
- 

### メモ
* main()をちょこっと変えた。