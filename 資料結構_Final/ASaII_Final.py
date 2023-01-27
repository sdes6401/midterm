import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

import pygame
import random
import time, threading, sys

global image, results, isOpened, begin, debug

image = None        #照片
results = None      #骨架資訊的變數
isOpened = True     #控制執行續的變數
begin = False       #控制是否開始音樂的變數
debug = True        #看是否要顯示骨架

#設定畫面大小
display_X = 1280
display_Y = 720

#設定方框的尺寸
squareSize = 100

#設定遊戲難度
difficulty = 0

#設定起始動作
rand = 6

#設定起始分數
score = 0

pygame.init()
screen = pygame.display.set_mode((display_X, display_Y), 0, 32)
pygame.display.set_caption('test')
font = pygame.font.Font('freesansbold.ttf',32)

#設定遊戲時間
clock = pygame.time.Clock()
counterFont = pygame.font.SysFont(None, 100)
#設定初始秒數並渲染到畫面
counter = 60
counterText = counterFont.render(str(counter), True, (128, 0, 0))
timer_event = pygame.USEREVENT+1
#設定延遲 1000為一秒
pygame.time.set_timer(timer_event, 1000)



#設定各動作產生方框位置
hardLeftHandX=[730,240,800,380,900,850,840,680]
hardLeftHandY=[260,185,170,550,640,100,340,100]
hardLeftElbowX=[660,380,670,380,840,780,650,740]
hardLeftElbowY=[280,210,190,410,530,190,365,190]
hardLeftShoulderX=[680,480,550,380,800,680,450,780]
hardLeftShoulderY=[190,200,190,200,420,240,360,260]
hardLeftKneeX=[560,830,620,770,530,590,740,438]
hardLeftKneeY=[310,360,490,360,480,485,430,480]
hardLeftAnkleX=[420,1010,790,970,480,590,920,320]
hardLeftAnkleY=[320,380,600,490,620,630,150,575]

hardRightHandX=[730,240,800,380,900,440,840,870]
hardRightHandY=[260,185,170,550,640,190,340,620]
hardRightElbowX=[820,380,670,380,840,540,650,830]
hardRightElbowY=[290,210,190,410,530,320,365,520]
hardRightShoulderX=[800,480,550,380,800,620,450,820]
hardRightShoulderY=[200,200,190,200,420,210,360,400]
hardRightKneeX=[725,620,640,460,500,450,750,480]
hardRightKneeY=[510,460,450,420,220,320,430,520]
hardRightAnkleX=[730,620,585,680,380,440,920,480]
hardRightAnkleY=[620,640,650,440,100,190,150,575]

easyLeftHandX=[380,630,810,450,460,620,260,510]
easyLeftHandY=[540,300,265,140,410,220,140,280]
easyLeftElbowX=[270,530,750,530,490,500,410,515]
easyLeftElbowY=[410,270,320,260,350,220,140,165]
easyLeftShoulderX=[230,610,730,580,530,540,520,510]
easyLeftShoulderY=[280,240,230,300,280,170,125,80]
easyLeftKneeX=[220,470,560,620,630,600,545,580]
easyLeftKneeY=[410,450,450,440,500,490,340,400]
easyLeftAnkleX=[290,420,390,610,760,635,570,600]
easyLeftAnkleY=[590,590,440,560,550,630,510,570]

easyRightHandX=[460,680,570,450,460,620,270,690]
easyRightHandY=[540,290,330,140,410,220,125,250]
easyRightElbowX=[510,790,590,530,490,730,430,660]
easyRightElbowY=[400,260,240,260,350,220,125,170]
easyRightShoulderX=[470,720,730,580,530,690,610,630]
easyRightShoulderY=[270,240,230,300,280,170,220,70]
easyRightKneeX=[660,840,680,620,460,780,550,670]
easyRightKneeY=[460,440,410,440,430,410,340,390]
easyRightAnkleX=[920,960,640,610,450,625,570,670]
easyRightAnkleY=[570,590,540,560,570,445,510,250]

def actSelection():
    global rand
    rand = (int)(random.uniform(1, 9))
    print(rand)

#倒數函數
def countdown():
    global reciprocal
    while reciprocal > 0:
        reciprocal = reciprocal - 1
        time.sleep(1)

def changeAction():
    #判斷倒數時間為0時，換動作
    if reciprocal == 0:
        global score
        actSelection()
        score+=1
        
def H1():
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftHandX[0],hardLeftHandY[0]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftElbowX[0],hardLeftElbowY[0]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftShoulderX[0],hardLeftShoulderY[0]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftKneeX[0],hardLeftKneeY[0]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftAnkleX[0],hardLeftAnkleY[0]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightHandX[0],hardRightHandY[0]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightElbowX[0],hardRightElbowY[0]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightShoulderX[0],hardRightShoulderY[0]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightKneeX[0],hardRightKneeY[0]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightAnkleX[0],hardRightAnkleY[0]))
    
def H2():
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftHandX[1],hardLeftHandY[1]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftElbowX[1],hardLeftElbowY[1]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftShoulderX[1],hardLeftShoulderY[1]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftKneeX[1],hardLeftKneeY[1]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftAnkleX[1],hardLeftAnkleY[1]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightHandX[1],hardRightHandY[1]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightElbowX[1],hardRightElbowY[1]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightShoulderX[1],hardRightShoulderY[1]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightKneeX[1],hardRightKneeY[1]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightAnkleX[1],hardRightAnkleY[1]))
    
def H3():
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftHandX[2],hardLeftHandY[2]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftElbowX[2],hardLeftElbowY[2]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftShoulderX[2],hardLeftShoulderY[2]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftKneeX[2],hardLeftKneeY[2]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftAnkleX[2],hardLeftAnkleY[2]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightHandX[2],hardRightHandY[2]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightElbowX[2],hardRightElbowY[2]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightShoulderX[2],hardRightShoulderY[2]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightKneeX[2],hardRightKneeY[2]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightAnkleX[2],hardRightAnkleY[2]))
    
def H4():
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftHandX[3],hardLeftHandY[3]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftElbowX[3],hardLeftElbowY[3]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftShoulderX[3],hardLeftShoulderY[3]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftKneeX[3],hardLeftKneeY[3]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftAnkleX[3],hardLeftAnkleY[3]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightHandX[3],hardRightHandY[3]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightElbowX[3],hardRightElbowY[3]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightShoulderX[3],hardRightShoulderY[3]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightKneeX[3],hardRightKneeY[3]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightAnkleX[3],hardRightAnkleY[3]))
    
def H5():
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftHandX[4],hardLeftHandY[4]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftElbowX[4],hardLeftElbowY[4]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftShoulderX[4],hardLeftShoulderY[4]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftKneeX[4],hardLeftKneeY[4]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftAnkleX[4],hardLeftAnkleY[4]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightHandX[4],hardRightHandY[4]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightElbowX[4],hardRightElbowY[4]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightShoulderX[4],hardRightShoulderY[4]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightKneeX[4],hardRightKneeY[4]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightAnkleX[4],hardRightAnkleY[4]))
    
def H6():
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftHandX[5],hardLeftHandY[5]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftElbowX[5],hardLeftElbowY[5]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftShoulderX[5],hardLeftShoulderY[5]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftKneeX[5],hardLeftKneeY[5]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftAnkleX[5],hardLeftAnkleY[5]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightHandX[5],hardRightHandY[5]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightElbowX[5],hardRightElbowY[5]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightShoulderX[5],hardRightShoulderY[5]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightKneeX[5],hardRightKneeY[5]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightAnkleX[5],hardRightAnkleY[5]))
    
def H7():
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftHandX[6],hardLeftHandY[6]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftElbowX[6],hardLeftElbowY[6]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftShoulderX[6],hardLeftShoulderY[6]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftKneeX[6],hardLeftKneeY[6]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftAnkleX[6],hardLeftAnkleY[6]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightHandX[6],hardRightHandY[6]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightElbowX[6],hardRightElbowY[6]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightShoulderX[6],hardRightShoulderY[6]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightKneeX[6],hardRightKneeY[6]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightAnkleX[6],hardRightAnkleY[6]))
    
def H8():
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftHandX[7],hardLeftHandY[7]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftElbowX[7],hardLeftElbowY[7]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftShoulderX[7],hardLeftShoulderY[7]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftKneeX[7],hardLeftKneeY[7]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftAnkleX[7],hardLeftAnkleY[7]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightHandX[7],hardRightHandY[7]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightElbowX[7],hardRightElbowY[7]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightShoulderX[7],hardRightShoulderY[7]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightKneeX[7],hardRightKneeY[7]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightAnkleX[7],hardRightAnkleY[7]))

def E1():
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftHandX[0],easyLeftHandY[0]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftElbowX[0],easyLeftElbowY[0]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftShoulderX[0],easyLeftShoulderY[0]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftKneeX[0],easyLeftKneeY[0]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftAnkleX[0],easyLeftAnkleY[0]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightHandX[0],easyRightHandY[0]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightElbowX[0],easyRightElbowY[0]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightShoulderX[0],easyRightShoulderY[0]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightKneeX[0],easyRightKneeY[0]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightAnkleX[0],easyRightAnkleY[0]))
    
def E2():
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftHandX[1],easyLeftHandY[1]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftElbowX[1],easyLeftElbowY[1]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftShoulderX[1],easyLeftShoulderY[1]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftKneeX[1],easyLeftKneeY[1]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftAnkleX[1],easyLeftAnkleY[1]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightHandX[1],easyRightHandY[1]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightElbowX[1],easyRightElbowY[1]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightShoulderX[1],easyRightShoulderY[1]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightKneeX[1],easyRightKneeY[1]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightAnkleX[1],easyRightAnkleY[1]))
    
def E3():
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftHandX[2],easyLeftHandY[2]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftElbowX[2],easyLeftElbowY[2]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftShoulderX[2],easyLeftShoulderY[2]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftKneeX[2],easyLeftKneeY[2]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftAnkleX[2],easyLeftAnkleY[2]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightHandX[2],easyRightHandY[2]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightElbowX[2],easyRightElbowY[2]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightShoulderX[2],easyRightShoulderY[2]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightKneeX[2],easyRightKneeY[2]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightAnkleX[2],easyRightAnkleY[2]))
    
def E4():
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftHandX[3],easyLeftHandY[3]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftElbowX[3],easyLeftElbowY[3]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftShoulderX[3],easyLeftShoulderY[3]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftKneeX[3],easyLeftKneeY[3]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftAnkleX[3],easyLeftAnkleY[3]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightHandX[3],easyRightHandY[3]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightElbowX[3],easyRightElbowY[3]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightShoulderX[3],easyRightShoulderY[3]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightKneeX[3],easyRightKneeY[3]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightAnkleX[3],easyRightAnkleY[3]))
    
def E5():
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftHandX[4],easyLeftHandY[4]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftElbowX[4],easyLeftElbowY[4]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftShoulderX[4],easyLeftShoulderY[4]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftKneeX[4],easyLeftKneeY[4]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftAnkleX[4],easyLeftAnkleY[4]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightHandX[4],easyRightHandY[4]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightElbowX[4],easyRightElbowY[4]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightShoulderX[4],easyRightShoulderY[4]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightKneeX[4],easyRightKneeY[4]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightAnkleX[4],easyRightAnkleY[4]))
    
def E6():
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftHandX[5],easyLeftHandY[5]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftElbowX[5],easyLeftElbowY[5]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftShoulderX[5],easyLeftShoulderY[5]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftKneeX[5],easyLeftKneeY[5]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftAnkleX[5],easyLeftAnkleY[5]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightHandX[5],easyRightHandY[5]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightElbowX[5],easyRightElbowY[5]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightShoulderX[5],easyRightShoulderY[5]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightKneeX[5],easyRightKneeY[5]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightAnkleX[5],easyRightAnkleY[5]))
    
def E7():
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftHandX[6],easyLeftHandY[6]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftElbowX[6],easyLeftElbowY[6]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftShoulderX[6],easyLeftShoulderY[6]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftKneeX[6],easyLeftKneeY[6]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftAnkleX[6],easyLeftAnkleY[6]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightHandX[6],easyRightHandY[6]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightElbowX[6],easyRightElbowY[6]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightShoulderX[6],easyRightShoulderY[6]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightKneeX[6],easyRightKneeY[6]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightAnkleX[6],easyRightAnkleY[6]))
    
def E8():
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftHandX[7],easyLeftHandY[7]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftElbowX[7],easyLeftElbowY[7]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftShoulderX[7],easyLeftShoulderY[7]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftKneeX[7],easyLeftKneeY[7]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftAnkleX[7],easyLeftAnkleY[7]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightHandX[7],easyRightHandY[7]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightElbowX[7],easyRightElbowY[7]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightShoulderX[7],easyRightShoulderY[7]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightKneeX[7],easyRightKneeY[7]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightAnkleX[7],easyRightAnkleY[7]))
     
#取得骨架
def get_pose():
    global image, results, isOpened, begin, debug

    cap = cv2.VideoCapture(0)

    cap.set(3, display_X)
    cap.set(4, display_Y)
    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:

        while cap.isOpened() and isOpened:
            success, imagein = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            imagein.flags.writeable = False
            imagetemp = cv2.cvtColor(imagein, cv2.COLOR_BGR2RGB)
            results = pose.process(imagetemp)
            imagein.flags.writeable = True
            if debug:
                imagein = cv2.cvtColor(imagein, cv2.COLOR_RGB2BGR)
                mp_drawing.draw_landmarks(
                    imagein,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            else:
                imagein = cv2.cvtColor(imagein, cv2.COLOR_RGB2BGR)

            image = cv2.resize(imagein, (display_X, display_Y))
            begin = True
    cap.release()
threading.Thread(target=get_pose).start()

#   game begin
while isOpened:  
    if begin:
        # 刷新背景(背景為鏡頭影像)
        str_encode = cv2.flip(image, 1)
        background_image = pygame.image.frombuffer(str_encode.tobytes(), str_encode.shape[1::-1],"RGB")
        screen.blit(background_image,[0,0])

        # 取得人體骨架位置(左右手)
        try:
            leftIndexX = (1-results.pose_landmarks.landmark[19].x)*display_X
            leftIndexY = results.pose_landmarks.landmark[19].y*display_Y
            leftElbowX = (1-results.pose_landmarks.landmark[13].x)*display_X
            leftElbowY = results.pose_landmarks.landmark[13].y*display_Y
            leftShoulderX = (1-results.pose_landmarks.landmark[11].x)*display_X
            leftShoulderY = results.pose_landmarks.landmark[11].y*display_Y
            leftKneeX = (1-results.pose_landmarks.landmark[25].x)*display_X
            leftKneeY = results.pose_landmarks.landmark[25].y*display_Y
            leftAnkleX = (1-results.pose_landmarks.landmark[27].x)*display_X
            leftAnkleY = results.pose_landmarks.landmark[27].y*display_Y
            
            rightIndexX = (1-results.pose_landmarks.landmark[20].x)*display_X
            rightIndexY = results.pose_landmarks.landmark[20].y*display_Y
            rightElbowX = (1-results.pose_landmarks.landmark[14].x)*display_X
            rightElbowY = results.pose_landmarks.landmark[14].y*display_Y
            rightShoulderX = (1-results.pose_landmarks.landmark[12].x)*display_X
            rightShoulderY = results.pose_landmarks.landmark[12].y*display_Y
            rightKneeX = (1-results.pose_landmarks.landmark[26].x)*display_X
            rightKneeY = results.pose_landmarks.landmark[26].y*display_Y
            rightAnkleX = (1-results.pose_landmarks.landmark[28].x)*display_X
            rightAnkleY = results.pose_landmarks.landmark[28].y*display_Y
        except:       
            leftIndexX = 0
            leftIndexY = 0
            leftElbowX = 0
            leftElbowY = 0
            leftShoulderX = 0
            leftShoulderY = 0
            leftKneeX = 0
            leftKneeY = 0
            leftAnkleX = 0
            leftAnkleY = 0
            
            rightIndexX = 0
            rightIndexY = 0
            rightElbowX = 0
            rightElbowY = 0
            rightShoulderX = 0
            rightShoulderY = 0
            rightKneeX = 0
            rightKneeY = 0
            rightAnkleX = 0
            rightAnkleY = 0
            
        #顯示簡單
        if  difficulty==0:
            selectEasy = font.render('EASY', True, (255, 255, 255),(0, 255, 0))
            new_selectEasy = pygame.transform.rotozoom(selectEasy, 0, 5)
            screen.blit(new_selectEasy, (100, 260))
            #顯示困難
            selectHard = font.render('HARD', True, (255, 255, 255),(255, 0, 0))
            new_selectHard = pygame.transform.rotozoom(selectHard, 0, 5)
            screen.blit(new_selectHard, (740, 260))
            
            if  (leftIndexX>=100) and (leftIndexX<=540) and (leftIndexY>=260) and (leftIndexY<=420) and \
                (rightIndexX>=100) and (rightIndexX<=540) and (rightIndexY>=260) and (rightIndexY<=420):
                difficulty = 1
                
            if  (leftIndexX>=740) and (leftIndexX<=1210) and (leftIndexY>=260) and (leftIndexY<=420) and \
                (rightIndexX>=740) and (rightIndexX<=1210) and (rightIndexY>=260) and (rightIndexY<=420):
                difficulty = 2   
        if  difficulty==1:
            if(rand==1):
                E1()
                if  (leftIndexX>=easyLeftHandX[0]) and (leftIndexX<=easyLeftHandX[0]+squareSize) and (leftIndexY>=easyLeftHandY[0]) and (leftIndexY<=easyLeftHandY[0]+squareSize) and \
                    (leftElbowX>=easyLeftElbowX[0]) and (leftElbowX<=easyLeftElbowX[0]+squareSize) and (leftElbowY>=easyLeftElbowY[0]) and (leftElbowY<=easyLeftElbowY[0]+squareSize) and \
                    (leftShoulderX>=easyLeftShoulderX[0]) and (leftShoulderX<=easyLeftShoulderX[0]+squareSize) and (leftShoulderY>=easyLeftShoulderY[0]) and (leftShoulderY<=easyLeftShoulderY[0]+squareSize) and \
                    (leftKneeX>=easyLeftKneeX[0]) and (leftKneeX<=easyLeftKneeX[0]+squareSize) and (leftKneeY>=easyLeftKneeY[0]) and (leftKneeY<=easyLeftKneeY[0]+squareSize) and \
                    (leftAnkleX>=easyLeftAnkleX[0]) and (leftAnkleX<=easyLeftAnkleX[0]+squareSize) and (leftAnkleY>=easyLeftAnkleY[0]) and (leftAnkleY<=easyLeftAnkleY[0]+squareSize) and \
                    (rightIndexX>=easyRightHandX[0]) and (rightIndexX<=easyRightHandX[0]+squareSize) and (rightIndexY>=easyRightHandY[0]) and (rightIndexY<=easyRightHandY[0]+squareSize) and \
                    (rightElbowX>=easyRightElbowX[0]) and (rightElbowX<=easyRightElbowX[0]+squareSize) and (rightElbowY>=easyRightElbowY[0]) and (rightElbowY<=easyRightElbowY[0]+squareSize) and \
                    (rightShoulderX>=easyRightShoulderX[0]) and (rightShoulderX<=easyRightShoulderX[0]+squareSize) and (rightShoulderY>=easyRightShoulderY[0]) and (rightShoulderY<=easyRightShoulderY[0]+squareSize) and \
                    (rightKneeX>=easyRightKneeX[0]) and (rightKneeX<=easyRightKneeX[0]+squareSize) and (rightKneeY>=easyRightKneeY[0]) and (rightKneeY<=easyRightKneeY[0]+squareSize) and \
                    (rightAnkleX>=easyRightAnkleX[0]) and (rightAnkleX<=easyRightAnkleX[0]+squareSize) and (rightAnkleY>=easyRightAnkleY[0]) and (rightAnkleY<=easyRightAnkleY[0]+squareSize):
                    #倒數五秒
                    reciprocal = 5
                    #使用多執行緒，抓取點的時候一起倒數時間
                    t = threading.Thread(target=countdown)
                    t.start()
                    changeAction()
            if(rand==2):
                E2()
                if  (leftIndexX>=easyLeftHandX[1]) and (leftIndexX<=easyLeftHandX[1]+squareSize) and (leftIndexY>=easyLeftHandY[1]) and (leftIndexY<=easyLeftHandY[1]+squareSize) and \
                    (leftElbowX>=easyLeftElbowX[1]) and (leftElbowX<=easyLeftElbowX[1]+squareSize) and (leftElbowY>=easyLeftElbowY[1]) and (leftElbowY<=easyLeftElbowY[1]+squareSize) and \
                    (leftShoulderX>=easyLeftShoulderX[1]) and (leftShoulderX<=easyLeftShoulderX[1]+squareSize) and (leftShoulderY>=easyLeftShoulderY[1]) and (leftShoulderY<=easyLeftShoulderY[1]+squareSize) and \
                    (leftKneeX>=easyLeftKneeX[1]) and (leftKneeX<=easyLeftKneeX[1]+squareSize) and (leftKneeY>=easyLeftKneeY[1]) and (leftKneeY<=easyLeftKneeY[1]+squareSize) and \
                    (leftAnkleX>=easyLeftAnkleX[1]) and (leftAnkleX<=easyLeftAnkleX[1]+squareSize) and (leftAnkleY>=easyLeftAnkleY[1]) and (leftAnkleY<=easyLeftAnkleY[1]+squareSize) and \
                    (rightIndexX>=easyRightHandX[1]) and (rightIndexX<=easyRightHandX[1]+squareSize) and (rightIndexY>=easyRightHandY[1]) and (rightIndexY<=easyRightHandY[1]+squareSize) and \
                    (rightElbowX>=easyRightElbowX[1]) and (rightElbowX<=easyRightElbowX[1]+squareSize) and (rightElbowY>=easyRightElbowY[1]) and (rightElbowY<=easyRightElbowY[1]+squareSize) and \
                    (rightShoulderX>=easyRightShoulderX[1]) and (rightShoulderX<=easyRightShoulderX[1]+squareSize) and (rightShoulderY>=easyRightShoulderY[1]) and (rightShoulderY<=easyRightShoulderY[1]+squareSize) and \
                    (rightKneeX>=easyRightKneeX[1]) and (rightKneeX<=easyRightKneeX[1]+squareSize) and (rightKneeY>=easyRightKneeY[1]) and (rightKneeY<=easyRightKneeY[1]+squareSize) and \
                    (rightAnkleX>=easyRightAnkleX[1]) and (rightAnkleX<=easyRightAnkleX[1]+squareSize) and (rightAnkleY>=easyRightAnkleY[1]) and (rightAnkleY<=easyRightAnkleY[1]+squareSize):
                    #倒數五秒
                    reciprocal = 5
                    #使用多執行緒，抓取點的時候一起倒數時間
                    t = threading.Thread(target=countdown)
                    t.start()
                    changeAction()
            if(rand==3):
                E3()
                if  (leftIndexX>=easyLeftHandX[2]) and (leftIndexX<=easyLeftHandX[2]+squareSize) and (leftIndexY>=easyLeftHandY[2]) and (leftIndexY<=easyLeftHandY[2]+squareSize) and \
                    (leftElbowX>=easyLeftElbowX[2]) and (leftElbowX<=easyLeftElbowX[2]+squareSize) and (leftElbowY>=easyLeftElbowY[2]) and (leftElbowY<=easyLeftElbowY[2]+squareSize) and \
                    (leftShoulderX>=easyLeftShoulderX[2]) and (leftShoulderX<=easyLeftShoulderX[2]+squareSize) and (leftShoulderY>=easyLeftShoulderY[2]) and (leftShoulderY<=easyLeftShoulderY[2]+squareSize) and \
                    (leftKneeX>=easyLeftKneeX[2]) and (leftKneeX<=easyLeftKneeX[2]+squareSize) and (leftKneeY>=easyLeftKneeY[2]) and (leftKneeY<=easyLeftKneeY[2]+squareSize) and \
                    (leftAnkleX>=easyLeftAnkleX[2]) and (leftAnkleX<=easyLeftAnkleX[2]+squareSize) and (leftAnkleY>=easyLeftAnkleY[2]) and (leftAnkleY<=easyLeftAnkleY[2]+squareSize) and \
                    (rightIndexX>=easyRightHandX[2]) and (rightIndexX<=easyRightHandX[2]+squareSize) and (rightIndexY>=easyRightHandY[2]) and (rightIndexY<=easyRightHandY[2]+squareSize) and \
                    (rightElbowX>=easyRightElbowX[2]) and (rightElbowX<=easyRightElbowX[2]+squareSize) and (rightElbowY>=easyRightElbowY[2]) and (rightElbowY<=easyRightElbowY[2]+squareSize) and \
                    (rightShoulderX>=easyRightShoulderX[2]) and (rightShoulderX<=easyRightShoulderX[2]+squareSize) and (rightShoulderY>=easyRightShoulderY[2]) and (rightShoulderY<=easyRightShoulderY[2]+squareSize) and \
                    (rightKneeX>=easyRightKneeX[2]) and (rightKneeX<=easyRightKneeX[2]+squareSize) and (rightKneeY>=easyRightKneeY[2]) and (rightKneeY<=easyRightKneeY[2]+squareSize) and \
                    (rightAnkleX>=easyRightAnkleX[2]) and (rightAnkleX<=easyRightAnkleX[2]+squareSize) and (rightAnkleY>=easyRightAnkleY[2]) and (rightAnkleY<=easyRightAnkleY[2]+squareSize):
                    #倒數五秒
                    reciprocal = 5
                    #使用多執行緒，抓取點的時候一起倒數時間
                    t = threading.Thread(target=countdown)
                    t.start()
                    changeAction()
            if(rand==4):
                E4()
                if  (leftIndexX>=easyLeftHandX[3]) and (leftIndexX<=easyLeftHandX[3]+squareSize) and (leftIndexY>=easyLeftHandY[3]) and (leftIndexY<=easyLeftHandY[3]+squareSize) and \
                    (leftElbowX>=easyLeftElbowX[3]) and (leftElbowX<=easyLeftElbowX[3]+squareSize) and (leftElbowY>=easyLeftElbowY[3]) and (leftElbowY<=easyLeftElbowY[3]+squareSize) and \
                    (leftShoulderX>=easyLeftShoulderX[3]) and (leftShoulderX<=easyLeftShoulderX[3]+squareSize) and (leftShoulderY>=easyLeftShoulderY[3]) and (leftShoulderY<=easyLeftShoulderY[3]+squareSize) and \
                    (leftKneeX>=easyLeftKneeX[3]) and (leftKneeX<=easyLeftKneeX[3]+squareSize) and (leftKneeY>=easyLeftKneeY[3]) and (leftKneeY<=easyLeftKneeY[3]+squareSize) and \
                    (leftAnkleX>=easyLeftAnkleX[3]) and (leftAnkleX<=easyLeftAnkleX[3]+squareSize) and (leftAnkleY>=easyLeftAnkleY[3]) and (leftAnkleY<=easyLeftAnkleY[3]+squareSize) and \
                    (rightIndexX>=easyRightHandX[3]) and (rightIndexX<=easyRightHandX[3]+squareSize) and (rightIndexY>=easyRightHandY[3]) and (rightIndexY<=easyRightHandY[3]+squareSize) and \
                    (rightElbowX>=easyRightElbowX[3]) and (rightElbowX<=easyRightElbowX[3]+squareSize) and (rightElbowY>=easyRightElbowY[3]) and (rightElbowY<=easyRightElbowY[3]+squareSize) and \
                    (rightShoulderX>=easyRightShoulderX[3]) and (rightShoulderX<=easyRightShoulderX[3]+squareSize) and (rightShoulderY>=easyRightShoulderY[3]) and (rightShoulderY<=easyRightShoulderY[3]+squareSize) and \
                    (rightKneeX>=easyRightKneeX[3]) and (rightKneeX<=easyRightKneeX[3]+squareSize) and (rightKneeY>=easyRightKneeY[3]) and (rightKneeY<=easyRightKneeY[3]+squareSize) and \
                    (rightAnkleX>=easyRightAnkleX[3]) and (rightAnkleX<=easyRightAnkleX[3]+squareSize) and (rightAnkleY>=easyRightAnkleY[3]) and (rightAnkleY<=easyRightAnkleY[3]+squareSize):
                    #倒數五秒
                    reciprocal = 5
                    #使用多執行緒，抓取點的時候一起倒數時間
                    t = threading.Thread(target=countdown)
                    t.start()
                    changeAction()
            if(rand==5):
                E5()
                if  (leftIndexX>=easyLeftHandX[4]) and (leftIndexX<=easyLeftHandX[4]+squareSize) and (leftIndexY>=easyLeftHandY[4]) and (leftIndexY<=easyLeftHandY[4]+squareSize) and \
                    (leftElbowX>=easyLeftElbowX[4]) and (leftElbowX<=easyLeftElbowX[4]+squareSize) and (leftElbowY>=easyLeftElbowY[4]) and (leftElbowY<=easyLeftElbowY[4]+squareSize) and \
                    (leftShoulderX>=easyLeftShoulderX[4]) and (leftShoulderX<=easyLeftShoulderX[4]+squareSize) and (leftShoulderY>=easyLeftShoulderY[4]) and (leftShoulderY<=easyLeftShoulderY[4]+squareSize) and \
                    (leftKneeX>=easyLeftKneeX[4]) and (leftKneeX<=easyLeftKneeX[4]+squareSize) and (leftKneeY>=easyLeftKneeY[4]) and (leftKneeY<=easyLeftKneeY[4]+squareSize) and \
                    (leftAnkleX>=easyLeftAnkleX[4]) and (leftAnkleX<=easyLeftAnkleX[4]+squareSize) and (leftAnkleY>=easyLeftAnkleY[4]) and (leftAnkleY<=easyLeftAnkleY[4]+squareSize) and \
                    (rightIndexX>=easyRightHandX[4]) and (rightIndexX<=easyRightHandX[4]+squareSize) and (rightIndexY>=easyRightHandY[4]) and (rightIndexY<=easyRightHandY[4]+squareSize) and \
                    (rightElbowX>=easyRightElbowX[4]) and (rightElbowX<=easyRightElbowX[4]+squareSize) and (rightElbowY>=easyRightElbowY[4]) and (rightElbowY<=easyRightElbowY[4]+squareSize) and \
                    (rightShoulderX>=easyRightShoulderX[4]) and (rightShoulderX<=easyRightShoulderX[4]+squareSize) and (rightShoulderY>=easyRightShoulderY[4]) and (rightShoulderY<=easyRightShoulderY[4]+squareSize) and \
                    (rightKneeX>=easyRightKneeX[4]) and (rightKneeX<=easyRightKneeX[4]+squareSize) and (rightKneeY>=easyRightKneeY[4]) and (rightKneeY<=easyRightKneeY[4]+squareSize) and \
                    (rightAnkleX>=easyRightAnkleX[4]) and (rightAnkleX<=easyRightAnkleX[4]+squareSize) and (rightAnkleY>=easyRightAnkleY[4]) and (rightAnkleY<=easyRightAnkleY[4]+squareSize):
                    #倒數五秒
                    reciprocal = 5
                    #使用多執行緒，抓取點的時候一起倒數時間
                    t = threading.Thread(target=countdown)
                    t.start()
                    changeAction()
            if(rand==6):
                E6()
                if  (leftIndexX>=easyLeftHandX[5]) and (leftIndexX<=easyLeftHandX[5]+squareSize) and (leftIndexY>=easyLeftHandY[5]) and (leftIndexY<=easyLeftHandY[5]+squareSize) and \
                    (leftElbowX>=easyLeftElbowX[5]) and (leftElbowX<=easyLeftElbowX[5]+squareSize) and (leftElbowY>=easyLeftElbowY[5]) and (leftElbowY<=easyLeftElbowY[5]+squareSize) and \
                    (leftShoulderX>=easyLeftShoulderX[5]) and (leftShoulderX<=easyLeftShoulderX[5]+squareSize) and (leftShoulderY>=easyLeftShoulderY[5]) and (leftShoulderY<=easyLeftShoulderY[5]+squareSize) and \
                    (leftKneeX>=easyLeftKneeX[5]) and (leftKneeX<=easyLeftKneeX[5]+squareSize) and (leftKneeY>=easyLeftKneeY[5]) and (leftKneeY<=easyLeftKneeY[5]+squareSize) and \
                    (leftAnkleX>=easyLeftAnkleX[5]) and (leftAnkleX<=easyLeftAnkleX[5]+squareSize) and (leftAnkleY>=easyLeftAnkleY[5]) and (leftAnkleY<=easyLeftAnkleY[5]+squareSize) and \
                    (rightIndexX>=easyRightHandX[5]) and (rightIndexX<=easyRightHandX[5]+squareSize) and (rightIndexY>=easyRightHandY[5]) and (rightIndexY<=easyRightHandY[5]+squareSize) and \
                    (rightElbowX>=easyRightElbowX[5]) and (rightElbowX<=easyRightElbowX[5]+squareSize) and (rightElbowY>=easyRightElbowY[5]) and (rightElbowY<=easyRightElbowY[5]+squareSize) and \
                    (rightShoulderX>=easyRightShoulderX[5]) and (rightShoulderX<=easyRightShoulderX[5]+squareSize) and (rightShoulderY>=easyRightShoulderY[5]) and (rightShoulderY<=easyRightShoulderY[5]+squareSize) and \
                    (rightKneeX>=easyRightKneeX[5]) and (rightKneeX<=easyRightKneeX[5]+squareSize) and (rightKneeY>=easyRightKneeY[5]) and (rightKneeY<=easyRightKneeY[5]+squareSize) and \
                    (rightAnkleX>=easyRightAnkleX[5]) and (rightAnkleX<=easyRightAnkleX[5]+squareSize) and (rightAnkleY>=easyRightAnkleY[5]) and (rightAnkleY<=easyRightAnkleY[5]+squareSize):
                    #倒數五秒
                    reciprocal = 5
                    #使用多執行緒，抓取點的時候一起倒數時間
                    t = threading.Thread(target=countdown)
                    t.start()
                    changeAction()
            if(rand==7):
                E7()
                if  (leftIndexX>=easyLeftHandX[6]) and (leftIndexX<=easyLeftHandX[6]+squareSize) and (leftIndexY>=easyLeftHandY[6]) and (leftIndexY<=easyLeftHandY[6]+squareSize) and \
                    (leftElbowX>=easyLeftElbowX[6]) and (leftElbowX<=easyLeftElbowX[6]+squareSize) and (leftElbowY>=easyLeftElbowY[6]) and (leftElbowY<=easyLeftElbowY[6]+squareSize) and \
                    (leftShoulderX>=easyLeftShoulderX[6]) and (leftShoulderX<=easyLeftShoulderX[6]+squareSize) and (leftShoulderY>=easyLeftShoulderY[6]) and (leftShoulderY<=easyLeftShoulderY[6]+squareSize) and \
                    (leftKneeX>=easyLeftKneeX[6]) and (leftKneeX<=easyLeftKneeX[6]+squareSize) and (leftKneeY>=easyLeftKneeY[6]) and (leftKneeY<=easyLeftKneeY[6]+squareSize) and \
                    (leftAnkleX>=easyLeftAnkleX[6]) and (leftAnkleX<=easyLeftAnkleX[6]+squareSize) and (leftAnkleY>=easyLeftAnkleY[6]) and (leftAnkleY<=easyLeftAnkleY[6]+squareSize) and \
                    (rightIndexX>=easyRightHandX[6]) and (rightIndexX<=easyRightHandX[6]+squareSize) and (rightIndexY>=easyRightHandY[6]) and (rightIndexY<=easyRightHandY[6]+squareSize) and \
                    (rightElbowX>=easyRightElbowX[6]) and (rightElbowX<=easyRightElbowX[6]+squareSize) and (rightElbowY>=easyRightElbowY[6]) and (rightElbowY<=easyRightElbowY[6]+squareSize) and \
                    (rightShoulderX>=easyRightShoulderX[6]) and (rightShoulderX<=easyRightShoulderX[6]+squareSize) and (rightShoulderY>=easyRightShoulderY[6]) and (rightShoulderY<=easyRightShoulderY[6]+squareSize) and \
                    (rightKneeX>=easyRightKneeX[6]) and (rightKneeX<=easyRightKneeX[6]+squareSize) and (rightKneeY>=easyRightKneeY[6]) and (rightKneeY<=easyRightKneeY[6]+squareSize) and \
                    (rightAnkleX>=easyRightAnkleX[6]) and (rightAnkleX<=easyRightAnkleX[6]+squareSize) and (rightAnkleY>=easyRightAnkleY[6]) and (rightAnkleY<=easyRightAnkleY[6]+squareSize):
                    #倒數五秒
                    reciprocal = 5
                    #使用多執行緒，抓取點的時候一起倒數時間
                    t = threading.Thread(target=countdown)
                    t.start()
                    changeAction()
            if(rand==8):
                E8()
                if  (leftIndexX>=easyLeftHandX[7]) and (leftIndexX<=easyLeftHandX[7]+squareSize) and (leftIndexY>=easyLeftHandY[7]) and (leftIndexY<=easyLeftHandY[7]+squareSize) and \
                    (leftElbowX>=easyLeftElbowX[7]) and (leftElbowX<=easyLeftElbowX[7]+squareSize) and (leftElbowY>=easyLeftElbowY[7]) and (leftElbowY<=easyLeftElbowY[7]+squareSize) and \
                    (leftShoulderX>=easyLeftShoulderX[7]) and (leftShoulderX<=easyLeftShoulderX[7]+squareSize) and (leftShoulderY>=easyLeftShoulderY[7]) and (leftShoulderY<=easyLeftShoulderY[7]+squareSize) and \
                    (leftKneeX>=easyLeftKneeX[7]) and (leftKneeX<=easyLeftKneeX[7]+squareSize) and (leftKneeY>=easyLeftKneeY[7]) and (leftKneeY<=easyLeftKneeY[7]+squareSize) and \
                    (leftAnkleX>=easyLeftAnkleX[7]) and (leftAnkleX<=easyLeftAnkleX[7]+squareSize) and (leftAnkleY>=easyLeftAnkleY[7]) and (leftAnkleY<=easyLeftAnkleY[7]+squareSize) and \
                    (rightIndexX>=easyRightHandX[7]) and (rightIndexX<=easyRightHandX[7]+squareSize) and (rightIndexY>=easyRightHandY[7]) and (rightIndexY<=easyRightHandY[7]+squareSize) and \
                    (rightElbowX>=easyRightElbowX[7]) and (rightElbowX<=easyRightElbowX[7]+squareSize) and (rightElbowY>=easyRightElbowY[7]) and (rightElbowY<=easyRightElbowY[7]+squareSize) and \
                    (rightShoulderX>=easyRightShoulderX[7]) and (rightShoulderX<=easyRightShoulderX[7]+squareSize) and (rightShoulderY>=easyRightShoulderY[7]) and (rightShoulderY<=easyRightShoulderY[7]+squareSize) and \
                    (rightKneeX>=easyRightKneeX[7]) and (rightKneeX<=easyRightKneeX[7]+squareSize) and (rightKneeY>=easyRightKneeY[7]) and (rightKneeY<=easyRightKneeY[7]+squareSize) and \
                    (rightAnkleX>=easyRightAnkleX[7]) and (rightAnkleX<=easyRightAnkleX[7]+squareSize) and (rightAnkleY>=easyRightAnkleY[7]) and (rightAnkleY<=easyRightAnkleY[7]+squareSize):
                    #倒數五秒
                    reciprocal = 5
                    #使用多執行緒，抓取點的時候一起倒數時間
                    t = threading.Thread(target=countdown)
                    t.start()
                    changeAction()
        if  difficulty==2:
            if(rand==1):
                H1()
                if  (leftIndexX>=hardLeftHandX[0]) and (leftIndexX<=hardLeftHandX[0]+squareSize) and (leftIndexY>=hardLeftHandY[0]) and (leftIndexY<=hardLeftHandY[0]+squareSize) and \
                    (leftElbowX>=hardLeftElbowX[0]) and (leftElbowX<=hardLeftElbowX[0]+squareSize) and (leftElbowY>=hardLeftElbowY[0]) and (leftElbowY<=hardLeftElbowY[0]+squareSize) and \
                    (leftShoulderX>=hardLeftShoulderX[0]) and (leftShoulderX<=hardLeftShoulderX[0]+squareSize) and (leftShoulderY>=hardLeftShoulderY[0]) and (leftShoulderY<=hardLeftShoulderY[0]+squareSize) and \
                    (leftKneeX>=hardLeftKneeX[0]) and (leftKneeX<=hardLeftKneeX[0]+squareSize) and (leftKneeY>=hardLeftKneeY[0]) and (leftKneeY<=hardLeftKneeY[0]+squareSize) and \
                    (leftAnkleX>=hardLeftAnkleX[0]) and (leftAnkleX<=hardLeftAnkleX[0]+squareSize) and (leftAnkleY>=hardLeftAnkleY[0]) and (leftAnkleY<=hardLeftAnkleY[0]+squareSize) and \
                    (rightIndexX>=hardRightHandX[0]) and (rightIndexX<=hardRightHandX[0]+squareSize) and (rightIndexY>=hardRightHandY[0]) and (rightIndexY<=hardRightHandY[0]+squareSize) and \
                    (rightElbowX>=hardRightElbowX[0]) and (rightElbowX<=hardRightElbowX[0]+squareSize) and (rightElbowY>=hardRightElbowY[0]) and (rightElbowY<=hardRightElbowY[0]+squareSize) and \
                    (rightShoulderX>=hardRightShoulderX[0]) and (rightShoulderX<=hardRightShoulderX[0]+squareSize) and (rightShoulderY>=hardRightShoulderY[0]) and (rightShoulderY<=hardRightShoulderY[0]+squareSize) and \
                    (rightKneeX>=hardRightKneeX[0]) and (rightKneeX<=hardRightKneeX[0]+squareSize) and (rightKneeY>=hardRightKneeY[0]) and (rightKneeY<=hardRightKneeY[0]+squareSize) and \
                    (rightAnkleX>=hardRightAnkleX[0]) and (rightAnkleX<=hardRightAnkleX[0]+squareSize) and (rightAnkleY>=hardRightAnkleY[0]) and (rightAnkleY<=hardRightAnkleY[0]+squareSize):
                    #倒數五秒
                    reciprocal = 5
                    #使用多執行緒，抓取點的時候一起倒數時間
                    t = threading.Thread(target=countdown)
                    t.start()
                    changeAction()
            if(rand==2):
                H2()
                if  (leftIndexX>=hardLeftHandX[1]) and (leftIndexX<=hardLeftHandX[1]+squareSize) and (leftIndexY>=hardLeftHandY[1]) and (leftIndexY<=hardLeftHandY[1]+squareSize) and \
                    (leftElbowX>=hardLeftElbowX[1]) and (leftElbowX<=hardLeftElbowX[1]+squareSize) and (leftElbowY>=hardLeftElbowY[1]) and (leftElbowY<=hardLeftElbowY[1]+squareSize) and \
                    (leftShoulderX>=hardLeftShoulderX[1]) and (leftShoulderX<=hardLeftShoulderX[1]+squareSize) and (leftShoulderY>=hardLeftShoulderY[1]) and (leftShoulderY<=hardLeftShoulderY[1]+squareSize) and \
                    (leftKneeX>=hardLeftKneeX[1]) and (leftKneeX<=hardLeftKneeX[1]+squareSize) and (leftKneeY>=hardLeftKneeY[1]) and (leftKneeY<=hardLeftKneeY[1]+squareSize) and \
                    (leftAnkleX>=hardLeftAnkleX[1]) and (leftAnkleX<=hardLeftAnkleX[1]+squareSize) and (leftAnkleY>=hardLeftAnkleY[1]) and (leftAnkleY<=hardLeftAnkleY[1]+squareSize) and \
                    (rightIndexX>=hardRightHandX[1]) and (rightIndexX<=hardRightHandX[1]+squareSize) and (rightIndexY>=hardRightHandY[1]) and (rightIndexY<=hardRightHandY[1]+squareSize) and \
                    (rightElbowX>=hardRightElbowX[1]) and (rightElbowX<=hardRightElbowX[1]+squareSize) and (rightElbowY>=hardRightElbowY[1]) and (rightElbowY<=hardRightElbowY[1]+squareSize) and \
                    (rightShoulderX>=hardRightShoulderX[1]) and (rightShoulderX<=hardRightShoulderX[1]+squareSize) and (rightShoulderY>=hardRightShoulderY[1]) and (rightShoulderY<=hardRightShoulderY[1]+squareSize) and \
                    (rightKneeX>=hardRightKneeX[1]) and (rightKneeX<=hardRightKneeX[1]+squareSize) and (rightKneeY>=hardRightKneeY[1]) and (rightKneeY<=hardRightKneeY[1]+squareSize) and \
                    (rightAnkleX>=hardRightAnkleX[1]) and (rightAnkleX<=hardRightAnkleX[1]+squareSize) and (rightAnkleY>=hardRightAnkleY[1]) and (rightAnkleY<=hardRightAnkleY[1]+squareSize):
                    #倒數五秒
                    reciprocal = 5
                    #使用多執行緒，抓取點的時候一起倒數時間
                    t = threading.Thread(target=countdown)
                    t.start()
                    changeAction()
            if(rand==3):
                H3()
                if  (leftIndexX>=hardLeftHandX[2]) and (leftIndexX<=hardLeftHandX[2]+squareSize) and (leftIndexY>=hardLeftHandY[2]) and (leftIndexY<=hardLeftHandY[2]+squareSize) and \
                    (leftElbowX>=hardLeftElbowX[2]) and (leftElbowX<=hardLeftElbowX[2]+squareSize) and (leftElbowY>=hardLeftElbowY[2]) and (leftElbowY<=hardLeftElbowY[2]+squareSize) and \
                    (leftShoulderX>=hardLeftShoulderX[2]) and (leftShoulderX<=hardLeftShoulderX[2]+squareSize) and (leftShoulderY>=hardLeftShoulderY[2]) and (leftShoulderY<=hardLeftShoulderY[2]+squareSize) and \
                    (leftKneeX>=hardLeftKneeX[2]) and (leftKneeX<=hardLeftKneeX[2]+squareSize) and (leftKneeY>=hardLeftKneeY[2]) and (leftKneeY<=hardLeftKneeY[2]+squareSize) and \
                    (leftAnkleX>=hardLeftAnkleX[2]) and (leftAnkleX<=hardLeftAnkleX[2]+squareSize) and (leftAnkleY>=hardLeftAnkleY[2]) and (leftAnkleY<=hardLeftAnkleY[2]+squareSize) and \
                    (rightIndexX>=hardRightHandX[2]) and (rightIndexX<=hardRightHandX[2]+squareSize) and (rightIndexY>=hardRightHandY[2]) and (rightIndexY<=hardRightHandY[2]+squareSize) and \
                    (rightElbowX>=hardRightElbowX[2]) and (rightElbowX<=hardRightElbowX[2]+squareSize) and (rightElbowY>=hardRightElbowY[2]) and (rightElbowY<=hardRightElbowY[2]+squareSize) and \
                    (rightShoulderX>=hardRightShoulderX[2]) and (rightShoulderX<=hardRightShoulderX[2]+squareSize) and (rightShoulderY>=hardRightShoulderY[2]) and (rightShoulderY<=hardRightShoulderY[2]+squareSize) and \
                    (rightKneeX>=hardRightKneeX[2]) and (rightKneeX<=hardRightKneeX[2]+squareSize) and (rightKneeY>=hardRightKneeY[2]) and (rightKneeY<=hardRightKneeY[2]+squareSize) and \
                    (rightAnkleX>=hardRightAnkleX[2]) and (rightAnkleX<=hardRightAnkleX[2]+squareSize) and (rightAnkleY>=hardRightAnkleY[2]) and (rightAnkleY<=hardRightAnkleY[2]+squareSize):
                    #倒數五秒
                    reciprocal = 5
                    #使用多執行緒，抓取點的時候一起倒數時間
                    t = threading.Thread(target=countdown)
                    t.start()
                    changeAction()
            if(rand==4):
                H4()
                if  (leftIndexX>=hardLeftHandX[3]) and (leftIndexX<=hardLeftHandX[3]+squareSize) and (leftIndexY>=hardLeftHandY[3]) and (leftIndexY<=hardLeftHandY[3]+squareSize) and \
                    (leftElbowX>=hardLeftElbowX[3]) and (leftElbowX<=hardLeftElbowX[3]+squareSize) and (leftElbowY>=hardLeftElbowY[3]) and (leftElbowY<=hardLeftElbowY[3]+squareSize) and \
                    (leftShoulderX>=hardLeftShoulderX[3]) and (leftShoulderX<=hardLeftShoulderX[3]+squareSize) and (leftShoulderY>=hardLeftShoulderY[3]) and (leftShoulderY<=hardLeftShoulderY[3]+squareSize) and \
                    (leftKneeX>=hardLeftKneeX[3]) and (leftKneeX<=hardLeftKneeX[3]+squareSize) and (leftKneeY>=hardLeftKneeY[3]) and (leftKneeY<=hardLeftKneeY[3]+squareSize) and \
                    (leftAnkleX>=hardLeftAnkleX[3]) and (leftAnkleX<=hardLeftAnkleX[3]+squareSize) and (leftAnkleY>=hardLeftAnkleY[3]) and (leftAnkleY<=hardLeftAnkleY[3]+squareSize) and \
                    (rightIndexX>=hardRightHandX[3]) and (rightIndexX<=hardRightHandX[3]+squareSize) and (rightIndexY>=hardRightHandY[3]) and (rightIndexY<=hardRightHandY[3]+squareSize) and \
                    (rightElbowX>=hardRightElbowX[3]) and (rightElbowX<=hardRightElbowX[3]+squareSize) and (rightElbowY>=hardRightElbowY[3]) and (rightElbowY<=hardRightElbowY[3]+squareSize) and \
                    (rightShoulderX>=hardRightShoulderX[3]) and (rightShoulderX<=hardRightShoulderX[3]+squareSize) and (rightShoulderY>=hardRightShoulderY[3]) and (rightShoulderY<=hardRightShoulderY[3]+squareSize) and \
                    (rightKneeX>=hardRightKneeX[3]) and (rightKneeX<=hardRightKneeX[3]+squareSize) and (rightKneeY>=hardRightKneeY[3]) and (rightKneeY<=hardRightKneeY[3]+squareSize) and \
                    (rightAnkleX>=hardRightAnkleX[3]) and (rightAnkleX<=hardRightAnkleX[3]+squareSize) and (rightAnkleY>=hardRightAnkleY[3]) and (rightAnkleY<=hardRightAnkleY[3]+squareSize):
                    #倒數五秒
                    reciprocal = 5
                    #使用多執行緒，抓取點的時候一起倒數時間
                    t = threading.Thread(target=countdown)
                    t.start()
                    changeAction()
            if(rand==5):
                H5()
                if  (leftIndexX>=hardLeftHandX[4]) and (leftIndexX<=hardLeftHandX[4]+squareSize) and (leftIndexY>=hardLeftHandY[4]) and (leftIndexY<=hardLeftHandY[4]+squareSize) and \
                    (leftElbowX>=hardLeftElbowX[4]) and (leftElbowX<=hardLeftElbowX[4]+squareSize) and (leftElbowY>=hardLeftElbowY[4]) and (leftElbowY<=hardLeftElbowY[4]+squareSize) and \
                    (leftShoulderX>=hardLeftShoulderX[4]) and (leftShoulderX<=hardLeftShoulderX[4]+squareSize) and (leftShoulderY>=hardLeftShoulderY[4]) and (leftShoulderY<=hardLeftShoulderY[4]+squareSize) and \
                    (leftKneeX>=hardLeftKneeX[4]) and (leftKneeX<=hardLeftKneeX[4]+squareSize) and (leftKneeY>=hardLeftKneeY[4]) and (leftKneeY<=hardLeftKneeY[4]+squareSize) and \
                    (leftAnkleX>=hardLeftAnkleX[4]) and (leftAnkleX<=hardLeftAnkleX[4]+squareSize) and (leftAnkleY>=hardLeftAnkleY[4]) and (leftAnkleY<=hardLeftAnkleY[4]+squareSize) and \
                    (rightIndexX>=hardRightHandX[4]) and (rightIndexX<=hardRightHandX[4]+squareSize) and (rightIndexY>=hardRightHandY[4]) and (rightIndexY<=hardRightHandY[4]+squareSize) and \
                    (rightElbowX>=hardRightElbowX[4]) and (rightElbowX<=hardRightElbowX[4]+squareSize) and (rightElbowY>=hardRightElbowY[4]) and (rightElbowY<=hardRightElbowY[4]+squareSize) and \
                    (rightShoulderX>=hardRightShoulderX[4]) and (rightShoulderX<=hardRightShoulderX[4]+squareSize) and (rightShoulderY>=hardRightShoulderY[4]) and (rightShoulderY<=hardRightShoulderY[4]+squareSize) and \
                    (rightKneeX>=hardRightKneeX[4]) and (rightKneeX<=hardRightKneeX[4]+squareSize) and (rightKneeY>=hardRightKneeY[4]) and (rightKneeY<=hardRightKneeY[4]+squareSize) and \
                    (rightAnkleX>=hardRightAnkleX[4]) and (rightAnkleX<=hardRightAnkleX[4]+squareSize) and (rightAnkleY>=hardRightAnkleY[4]) and (rightAnkleY<=hardRightAnkleY[4]+squareSize):
                    #倒數五秒
                    reciprocal = 5
                    #使用多執行緒，抓取點的時候一起倒數時間
                    t = threading.Thread(target=countdown)
                    t.start()
                    changeAction()
            if(rand==6):
                H6()
                if  (leftIndexX>=hardLeftHandX[5]) and (leftIndexX<=hardLeftHandX[5]+squareSize) and (leftIndexY>=hardLeftHandY[5]) and (leftIndexY<=hardLeftHandY[5]+squareSize) and \
                    (leftElbowX>=hardLeftElbowX[5]) and (leftElbowX<=hardLeftElbowX[5]+squareSize) and (leftElbowY>=hardLeftElbowY[5]) and (leftElbowY<=hardLeftElbowY[5]+squareSize) and \
                    (leftShoulderX>=hardLeftShoulderX[5]) and (leftShoulderX<=hardLeftShoulderX[5]+squareSize) and (leftShoulderY>=hardLeftShoulderY[5]) and (leftShoulderY<=hardLeftShoulderY[5]+squareSize) and \
                    (leftKneeX>=hardLeftKneeX[5]) and (leftKneeX<=hardLeftKneeX[5]+squareSize) and (leftKneeY>=hardLeftKneeY[5]) and (leftKneeY<=hardLeftKneeY[5]+squareSize) and \
                    (leftAnkleX>=hardLeftAnkleX[5]) and (leftAnkleX<=hardLeftAnkleX[5]+squareSize) and (leftAnkleY>=hardLeftAnkleY[5]) and (leftAnkleY<=hardLeftAnkleY[5]+squareSize) and \
                    (rightIndexX>=hardRightHandX[5]) and (rightIndexX<=hardRightHandX[5]+squareSize) and (rightIndexY>=hardRightHandY[5]) and (rightIndexY<=hardRightHandY[5]+squareSize) and \
                    (rightElbowX>=hardRightElbowX[5]) and (rightElbowX<=hardRightElbowX[5]+squareSize) and (rightElbowY>=hardRightElbowY[5]) and (rightElbowY<=hardRightElbowY[5]+squareSize) and \
                    (rightShoulderX>=hardRightShoulderX[5]) and (rightShoulderX<=hardRightShoulderX[5]+squareSize) and (rightShoulderY>=hardRightShoulderY[5]) and (rightShoulderY<=hardRightShoulderY[5]+squareSize) and \
                    (rightKneeX>=hardRightKneeX[5]) and (rightKneeX<=hardRightKneeX[5]+squareSize) and (rightKneeY>=hardRightKneeY[5]) and (rightKneeY<=hardRightKneeY[5]+squareSize) and \
                    (rightAnkleX>=hardRightAnkleX[5]) and (rightAnkleX<=hardRightAnkleX[5]+squareSize) and (rightAnkleY>=hardRightAnkleY[5]) and (rightAnkleY<=hardRightAnkleY[5]+squareSize):
                    #倒數五秒
                    reciprocal = 5
                    #使用多執行緒，抓取點的時候一起倒數時間
                    t = threading.Thread(target=countdown)
                    t.start()
                    changeAction()
            if(rand==7):
                H7()
                if  (leftIndexX>=hardLeftHandX[6]) and (leftIndexX<=hardLeftHandX[6]+squareSize) and (leftIndexY>=hardLeftHandY[6]) and (leftIndexY<=hardLeftHandY[6]+squareSize) and \
                    (leftElbowX>=hardLeftElbowX[6]) and (leftElbowX<=hardLeftElbowX[6]+squareSize) and (leftElbowY>=hardLeftElbowY[6]) and (leftElbowY<=hardLeftElbowY[6]+squareSize) and \
                    (leftShoulderX>=hardLeftShoulderX[6]) and (leftShoulderX<=hardLeftShoulderX[6]+squareSize) and (leftShoulderY>=hardLeftShoulderY[6]) and (leftShoulderY<=hardLeftShoulderY[6]+squareSize) and \
                    (leftKneeX>=hardLeftKneeX[6]) and (leftKneeX<=hardLeftKneeX[6]+squareSize) and (leftKneeY>=hardLeftKneeY[6]) and (leftKneeY<=hardLeftKneeY[6]+squareSize) and \
                    (leftAnkleX>=hardLeftAnkleX[6]) and (leftAnkleX<=hardLeftAnkleX[6]+squareSize) and (leftAnkleY>=hardLeftAnkleY[6]) and (leftAnkleY<=hardLeftAnkleY[6]+squareSize) and \
                    (rightIndexX>=hardRightHandX[6]) and (rightIndexX<=hardRightHandX[6]+squareSize) and (rightIndexY>=hardRightHandY[6]) and (rightIndexY<=hardRightHandY[6]+squareSize) and \
                    (rightElbowX>=hardRightElbowX[6]) and (rightElbowX<=hardRightElbowX[6]+squareSize) and (rightElbowY>=hardRightElbowY[6]) and (rightElbowY<=hardRightElbowY[6]+squareSize) and \
                    (rightShoulderX>=hardRightShoulderX[6]) and (rightShoulderX<=hardRightShoulderX[6]+squareSize) and (rightShoulderY>=hardRightShoulderY[6]) and (rightShoulderY<=hardRightShoulderY[6]+squareSize) and \
                    (rightKneeX>=hardRightKneeX[6]) and (rightKneeX<=hardRightKneeX[6]+squareSize) and (rightKneeY>=hardRightKneeY[6]) and (rightKneeY<=hardRightKneeY[6]+squareSize) and \
                    (rightAnkleX>=hardRightAnkleX[6]) and (rightAnkleX<=hardRightAnkleX[6]+squareSize) and (rightAnkleY>=hardRightAnkleY[6]) and (rightAnkleY<=hardRightAnkleY[6]+squareSize):
                    #倒數五秒
                    reciprocal = 5
                    #使用多執行緒，抓取點的時候一起倒數時間
                    t = threading.Thread(target=countdown)
                    t.start()
                    changeAction()
            if(rand==8):
                H8()
                if  (leftIndexX>=hardLeftHandX[7]) and (leftIndexX<=hardLeftHandX[7]+squareSize) and (leftIndexY>=hardLeftHandY[7]) and (leftIndexY<=hardLeftHandY[7]+squareSize) and \
                    (leftElbowX>=hardLeftElbowX[7]) and (leftElbowX<=hardLeftElbowX[7]+squareSize) and (leftElbowY>=hardLeftElbowY[7]) and (leftElbowY<=hardLeftElbowY[7]+squareSize) and \
                    (leftShoulderX>=hardLeftShoulderX[7]) and (leftShoulderX<=hardLeftShoulderX[7]+squareSize) and (leftShoulderY>=hardLeftShoulderY[7]) and (leftShoulderY<=hardLeftShoulderY[7]+squareSize) and \
                    (leftKneeX>=hardLeftKneeX[7]) and (leftKneeX<=hardLeftKneeX[7]+squareSize) and (leftKneeY>=hardLeftKneeY[7]) and (leftKneeY<=hardLeftKneeY[7]+squareSize) and \
                    (leftAnkleX>=hardLeftAnkleX[7]) and (leftAnkleX<=hardLeftAnkleX[7]+squareSize) and (leftAnkleY>=hardLeftAnkleY[7]) and (leftAnkleY<=hardLeftAnkleY[7]+squareSize) and \
                    (rightIndexX>=hardRightHandX[7]) and (rightIndexX<=hardRightHandX[7]+squareSize) and (rightIndexY>=hardRightHandY[7]) and (rightIndexY<=hardRightHandY[7]+squareSize) and \
                    (rightElbowX>=hardRightElbowX[7]) and (rightElbowX<=hardRightElbowX[7]+squareSize) and (rightElbowY>=hardRightElbowY[7]) and (rightElbowY<=hardRightElbowY[7]+squareSize) and \
                    (rightShoulderX>=hardRightShoulderX[7]) and (rightShoulderX<=hardRightShoulderX[7]+squareSize) and (rightShoulderY>=hardRightShoulderY[7]) and (rightShoulderY<=hardRightShoulderY[7]+squareSize) and \
                    (rightKneeX>=hardRightKneeX[7]) and (rightKneeX<=hardRightKneeX[7]+squareSize) and (rightKneeY>=hardRightKneeY[7]) and (rightKneeY<=hardRightKneeY[7]+squareSize) and \
                    (rightAnkleX>=hardRightAnkleX[7]) and (rightAnkleX<=hardRightAnkleX[7]+squareSize) and (rightAnkleY>=hardRightAnkleY[7]) and (rightAnkleY<=hardRightAnkleY[7]+squareSize):
                    #倒數五秒
                    reciprocal = 5
                    #使用多執行緒，抓取點的時候一起倒數時間
                    t = threading.Thread(target=countdown)
                    t.start()
                    changeAction()
        if  difficulty==3:
            endText = counterFont.render("Game Over", True, (128, 0, 0),(255, 255, 255))
            screen.blit(endText, (450,260))
            scoreTest = counterFont.render(f"Score: {score}", True, (0, 0, 128),(255, 255, 255))
            screen.blit(scoreTest, (490,460))
        
        #測試用 產生一點 左手在那點維持五秒可觸發倒數並加分
        #s = pygame.Surface((100,100), pygame.SRCALPHA)
        #s.fill((0,255,0,100))
        #screen.blit(s, (100,100))
        #if (leftIndexX>=100) and (leftIndexX<=200) and (leftIndexY>=100) and (leftIndexY<=200) :
        #    reciprocal = 5
        #    t = threading.Thread(target=countdown)
        #    t.start()
        #    if reciprocal == 0:
        #        print("1YAYAYAYAAYAYAYAYA")
        
        pygame.display.update()
        #關閉程式的程式碼``
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isOpened=False
                pygame.quit()
                sys.exit()
            elif event.type == timer_event and (difficulty == 1 or difficulty == 2):
                counter -= 1
                #每次減少一秒就重新渲染秒數
                counterText = counterFont.render(str(counter), True, (128, 0, 0))
                if counter == 0:  
                    difficulty=3
        if counter>0:            
            screen.blit(counterText, (1130,60))
            pygame.display.flip()