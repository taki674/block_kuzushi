import sys
import math
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, Rect

class Block:
    def __init__(self, col, rect, speed=0):
        self.col = col
        self.rect = rect
        self.speed = speed
        self.dir = random.randint(-45, 45) + 270

    def draw_bl(self):
            pygame.draw.rect(SURFACE, self.col, self.rect)

class Ball(Block):
    def move(self):
        self.rect.centerx += math.cos(math.radians(self.dir))*self.speed
        self.rect.centery -= math.sin(math.radians(self.dir))*self.speed

    def draw_ba(self):
        pygame.draw.ellipse(SURFACE, self.col, self.rect)


class Score:
    def __init__(self, sum):
        self.sum = sum

#フレーム毎の処理
def tick():
    global BLOCKS
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                PADDLE.rect.centerx -= 6
            elif event.key == K_RIGHT:
                PADDLE.rect.centerx += 6
            
            #パドルが画面外にはみ出さないための処理
            if PADDLE.rect.left < 0:
                PADDLE.rect.left = 0
            if PADDLE.rect.right > 600:
                PADDLE.rect.right = 600

    #ゲームオーバーしない間
    if BALL.rect.centery < 1000:
        BALL.move()
        
        prevlen = len(BLOCKS)
        BLOCKS = [x for x in BLOCKS if not x.rect.colliderect(BALL.rect)]
        
        #ボールがブロックと衝突したときの処理
        if len(BLOCKS) != prevlen:
            BALL.dir *= -1
            SCORE.sum += 4800
        
        #ボールがパドルと衝突したときの処理
        if PADDLE.rect.colliderect(BALL.rect):
           BALL.dir = 90 + (PADDLE.rect.centerx - BALL.rect.centerx) / PADDLE.rect.width * 80
        
        #ボールが左右の壁にぶつかったときの処理
        if BALL.rect.centerx < 0 or BALL.rect.centerx > 600:
            BALL.dir = 180 - BALL.dir
        
        #ボールが天井にぶつかったときの処理
        if BALL.rect.centery < 0:
            BALL.dir = -BALL.dir
            BALL.speed = 15

pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode((600, 800))
FPSCLOCK = pygame.time.Clock()
BLOCKS = []
PADDLE = Block((242, 242, 0), Rect(300, 700, 100, 30))
BALL = Ball((242, 242, 0), Rect(300, 400, 20, 20), 10)
SCORE = Score(0)

def main():
    score_font = pygame.font.SysFont(None, 50)    
    myfont = pygame.font.SysFont(None, 80)
    mess_clear = myfont.render("Cleared!", True, (255, 255, 0))
    mess_over = myfont.render("Game Over!", True, (255, 255, 0))
    fps = 30
    
    #上から一つずつ増えていくようにブロックを用意
    colors = [(255, 0, 0), (255, 165, 0), (242, 242, 0), (0, 128, 0), (128, 0, 128), (0, 0, 250)]
    for ypos, color in enumerate(colors, start=0):
        for xpos in range(0, ypos+1):
            BLOCKS.append(Block(color, Rect(xpos*100 + 10, ypos*50 + 40, 80, 30)))

    while True:
        tick()

        #各オブジェクトの描画
        SURFACE.fill((0, 0, 0))
        BALL.draw_ba()
        PADDLE.draw_bl()
        for block in BLOCKS:
            block.draw_bl()
        
        #クリアの表示
        if len(BLOCKS) == 0:
            SURFACE.blit(mess_clear, (200, 400))
        
        #ゲームオーバーの表示
        if BALL.rect.centery > 800 and len(BLOCKS) > 0:
            SURFACE.blit(mess_over, (150, 400))
        
        #スコアの計算
        score_str = str(SCORE.sum).zfill(6)
        score_image = score_font.render("SCORE:" + score_str, True, (0, 255, 0))  
        SURFACE.blit(score_image, (0, 0))
        
        #更新
        pygame.display.update()
        FPSCLOCK.tick(fps)

if __name__ == '__main__':
    main() 