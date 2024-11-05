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
通常の球とレーザービームの二種類が出される。

通常の球は、プレイヤーに追従するようになっており、さらにランダムに決まった範囲で出るようになっているので、よけるのは難しいなってものになっている。
レーザーは敵のカウントダウンに合わせて、出るようになっており、真ん中固定で出されるようになっている。


            
* ステージ3弾幕
* 制限時間設定
* 弾避け機能


### ToDo
- 

### メモ
* 