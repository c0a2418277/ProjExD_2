import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA ={
    pg.K_UP:(0, -5), 
    pg.K_DOWN:(0, +5),
   pg.K_LEFT:(-5, 0),
   pg.K_RIGHT:(+5, 0),

}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数が：こうかとんRectまたは爆弾Rect
    戻り値：判定結果タプル（横、縦）
    画面外ならTrue、外ならFalues
    """
    yoko, tate = True, True
    if rct.left <0 or WIDTH < rct.right:
        yoko = False
    if rct.top <0 or HEIGHT < rct.bottom:
        tate = False

    return yoko,tate


def gameover(screen: pg.Surface) -> None:
    kuro =pg.Surface((WIDTH, HEIGHT))
    kuro.fill((0,0,0)) #色指定
    kuro.set_alpha(150) #半透明
    screen.blit(kuro,(0,0))

    kk_cry = pg.image.load("fig/8.png") #画像を表示
    kk_cry1_rect =kk_cry.get_rect(center = (WIDTH//3, HEIGHT//2)) #大きさと場所を設定
    kk_cry2_rect = kk_cry.get_rect(center =(2*WIDTH//3, HEIGHT//2 ))
    screen.blit(kk_cry,kk_cry1_rect)
    screen.blit(kk_cry,kk_cry2_rect)

    fonto =pg.font.Font(None,80)
    txt = fonto.render("Game Over", True, (225,225,225)) #文字
    txt_rect = txt.get_rect(center=(WIDTH//2,HEIGHT//2)) #大きさ

    screen.blit(txt,txt_rect)

    pg.display.update()

    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    vx, vy = +5, +5
    bb_rct =bb_img.get_rect()
    kuro = pg.Surface((200, 200))
    kuro.fill((0, 0, 0))
    kuro.set_alpha(128)  

    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    clock = pg.time.Clock()
    tmr = 0       
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
           
        if kk_rct.colliderect(bb_rct):
            print("Game over")
            return
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        bb_rct.move_ip(vx,vy)
        yoko, tate =check_bound(bb_rct)
        if not yoko:
            vx*= -1
        if not tate:
            vy *= -1
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
