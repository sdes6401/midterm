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
            
def HardActions(i):
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftHandX[i],hardLeftHandY[i]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftElbowX[i],hardLeftElbowY[i]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftShoulderX[i],hardLeftShoulderY[i]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftKneeX[i],hardLeftKneeY[i]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardLeftAnkleX[i],hardLeftAnkleY[i]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightHandX[i],hardRightHandY[i]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightElbowX[i],hardRightElbowY[i]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightShoulderX[i],hardRightShoulderY[i]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightKneeX[i],hardRightKneeY[i]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (hardRightAnkleX[i],hardRightAnkleY[i]))    
    
def EasyActions(i):
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftHandX[i],easyLeftHandY[i]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftElbowX[i],easyLeftElbowY[i]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftShoulderX[i],easyLeftShoulderY[i]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftKneeX[i],easyLeftKneeY[i]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyLeftAnkleX[i],easyLeftAnkleY[i]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightHandX[i],easyRightHandY[i]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightElbowX[i],easyRightElbowY[i]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightShoulderX[i],easyRightShoulderY[i]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightKneeX[i],easyRightKneeY[i]))
    s = pygame.Surface((squareSize,squareSize), pygame.SRCALPHA)
    s.fill((0,255,0,100))
    screen.blit(s, (easyRightAnkleX[i],easyRightAnkleY[i]))
    
def JudgeHardPose(i):
    (leftIndexX>=hardLeftHandX[i]) and (leftIndexX<=hardLeftHandX[i]+squareSize) and (leftIndexY>=hardLeftHandY[i]) and (leftIndexY<=hardLeftHandY[i]+squareSize) and \
    (leftElbowX>=hardLeftElbowX[i]) and (leftElbowX<=hardLeftElbowX[i]+squareSize) and (leftElbowY>=hardLeftElbowY[i]) and (leftElbowY<=hardLeftElbowY[i]+squareSize) and \
    (leftShoulderX>=hardLeftShoulderX[i]) and (leftShoulderX<=hardLeftShoulderX[i]+squareSize) and (leftShoulderY>=hardLeftShoulderY[i]) and (leftShoulderY<=hardLeftShoulderY[i]+squareSize) and \
    (leftKneeX>=hardLeftKneeX[i]) and (leftKneeX<=hardLeftKneeX[i]+squareSize) and (leftKneeY>=hardLeftKneeY[i]) and (leftKneeY<=hardLeftKneeY[i]+squareSize) and \
    (leftAnkleX>=hardLeftAnkleX[i]) and (leftAnkleX<=hardLeftAnkleX[i]+squareSize) and (leftAnkleY>=hardLeftAnkleY[i]) and (leftAnkleY<=hardLeftAnkleY[i]+squareSize) and \
    (rightIndexX>=hardRightHandX[i]) and (rightIndexX<=hardRightHandX[i]+squareSize) and (rightIndexY>=hardRightHandY[i]) and (rightIndexY<=hardRightHandY[i]+squareSize) and \
    (rightElbowX>=hardRightElbowX[i]) and (rightElbowX<=hardRightElbowX[i]+squareSize) and (rightElbowY>=hardRightElbowY[i]) and (rightElbowY<=hardRightElbowY[i]+squareSize) and \
    (rightShoulderX>=hardRightShoulderX[i]) and (rightShoulderX<=hardRightShoulderX[i]+squareSize) and (rightShoulderY>=hardRightShoulderY[i]) and (rightShoulderY<=hardRightShoulderY[i]+squareSize) and \
    (rightKneeX>=hardRightKneeX[i]) and (rightKneeX<=hardRightKneeX[i]+squareSize) and (rightKneeY>=hardRightKneeY[i]) and (rightKneeY<=hardRightKneeY[i]+squareSize) and \
    (rightAnkleX>=hardRightAnkleX[i]) and (rightAnkleX<=hardRightAnkleX[i]+squareSize) and (rightAnkleY>=hardRightAnkleY[i]) and (rightAnkleY<=hardRightAnkleY[i]+squareSize)
    
def JudgeEasyPose(i):
    (leftIndexX>=easyLeftHandX[i]) and (leftIndexX<=easyLeftHandX[i]+squareSize) and (leftIndexY>=easyLeftHandY[i]) and (leftIndexY<=easyLeftHandY[i]+squareSize) and \
    (leftElbowX>=easyLeftElbowX[i]) and (leftElbowX<=easyLeftElbowX[i]+squareSize) and (leftElbowY>=easyLeftElbowY[i]) and (leftElbowY<=easyLeftElbowY[i]+squareSize) and \
    (leftShoulderX>=easyLeftShoulderX[i]) and (leftShoulderX<=easyLeftShoulderX[i]+squareSize) and (leftShoulderY>=easyLeftShoulderY[i]) and (leftShoulderY<=easyLeftShoulderY[i]+squareSize) and \
    (leftKneeX>=easyLeftKneeX[i]) and (leftKneeX<=easyLeftKneeX[i]+squareSize) and (leftKneeY>=easyLeftKneeY[i]) and (leftKneeY<=easyLeftKneeY[i]+squareSize) and \
    (leftAnkleX>=easyLeftAnkleX[i]) and (leftAnkleX<=easyLeftAnkleX[i]+squareSize) and (leftAnkleY>=easyLeftAnkleY[i]) and (leftAnkleY<=easyLeftAnkleY[i]+squareSize) and \
    (rightIndexX>=easyRightHandX[i]) and (rightIndexX<=easyRightHandX[i]+squareSize) and (rightIndexY>=easyRightHandY[i]) and (rightIndexY<=easyRightHandY[i]+squareSize) and \
    (rightElbowX>=easyRightElbowX[i]) and (rightElbowX<=easyRightElbowX[i]+squareSize) and (rightElbowY>=easyRightElbowY[i]) and (rightElbowY<=easyRightElbowY[i]+squareSize) and \
    (rightShoulderX>=easyRightShoulderX[i]) and (rightShoulderX<=easyRightShoulderX[i]+squareSize) and (rightShoulderY>=easyRightShoulderY[i]) and (rightShoulderY<=easyRightShoulderY[i]+squareSize) and \
    (rightKneeX>=easyRightKneeX[i]) and (rightKneeX<=easyRightKneeX[i]+squareSize) and (rightKneeY>=easyRightKneeY[i]) and (rightKneeY<=easyRightKneeY[i]+squareSize) and \
    (rightAnkleX>=easyRightAnkleX[i]) and (rightAnkleX<=easyRightAnkleX[i]+squareSize) and (rightAnkleY>=easyRightAnkleY[i]) and (rightAnkleY<=easyRightAnkleY[i]+squareSize)
     
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
            EasyActions(rand)
            if  JudgeEasyPose(rand-1):
                #倒數五秒
                reciprocal = 5
                #使用多執行緒，抓取點的時候一起倒數時間
                t = threading.Thread(target=countdown)
                t.start()
                changeAction()
        if  difficulty==2:
            HardActions(rand)
            if  JudgeHardPose(rand-1):
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