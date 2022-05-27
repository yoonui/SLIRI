import cv2
import mediapipe as mp
import numpy as np
import keyboard
import time
import platform
from make_sentence import join_jamos
from PIL import ImageFont, ImageDraw, Image
import assistant


def cv2_draw_label(image, text, point):
    x, y = point
    x, y = int(x), int(y)
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_image)
    if platform.system() == 'Darwin':
        font = 'AppleGothic.ttf'
    elif platform.system() == 'Windows': 
        font = 'malgun.ttf'
    elif platform.system() == 'Linux': 
        font = 'malgun.ttf'
    try:
        imageFont = ImageFont.truetype(font, 28)
    except:
        imageFont = ImageFont.load_default()
    draw.text((x, y), text, font=imageFont, fill=(0, 0, 0))
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    return image



max_num_hands = 1

gesture = {
    0:'ㄱ', 1:'ㄴ', 2:'ㄷ', 3:'ㄹ', 4:'ㅁ', 5:'ㅂ', 6:'ㅅ', 7:'ㅇ', 8:'ㅈ', 9:'ㅊ', 10:'ㅋ', 11:'ㅌ', 12:'ㅍ', 13:'ㅎ',
    14:'ㅏ', 15:'ㅑ', 16:'ㅓ', 17:'ㅕ', 18:'ㅗ', 19:'ㅛ', 20:'ㅜ', 21:'ㅠ', 22:'ㅡ', 23:'ㅣ', 24:'ㅐ', 25:'ㅔ', 26:'ㅚ',
    27:'ㅟ', 28:'ㅒ', 29:'ㅖ', 30:'ㅢ', 31:'SPACE', 32:'BACKSPACE', 33:'DUAL', 34:'END'
}

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands = max_num_hands,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
)

file = np.genfromtxt('./server/hand_recog/data.txt', delimiter=',')
angleFile = file[:,:-1]
labelFile = file[:,-1]
angle = angleFile.astype(np.float32)
label = labelFile.astype(np.float32)
knn = cv2.ml.KNearest_create()

knn.train(angle, cv2.ml.ROW_SAMPLE, label)
cap = cv2.VideoCapture(0)

startTime = time.time()
prev_index = 0
sentence = ''
recognizeDelay = 2

assistant_result = np.ones((200, 1500, 3), np.uint8) * 255
#cv2.imshow('ASSISTANT_RESULT', assistant_result)
command_list_1 = ['1.날씨', '2.날짜', '3.뉴스']
command_list_2 = ['1.강수확률', '2.강수량', '3.고민상담']
command_list_3 = ['1.미세먼지', '2.마을버스', '3.맛집']
command_list = np.ones((200, 150, 3), np.uint8) * 255

flag = 0

while True:
    ret, img = cap.read() #650 550
    img = cv2.resize(img, dsize=(650, 550))
    if not ret:
        continue
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)
    
    
    if result.multi_hand_landmarks is not None: # 13번 선택
        for res in result.multi_hand_landmarks:
            joint = np.zeros((21,3))
            for j,lm in enumerate(res.landmark):
                joint[j] = [lm.x, lm.y, lm.z]
            
            v1 = joint[[0, 1, 2, 3, 0, 5, 6, 7, 0,  9, 10, 11,  0, 13, 14, 15,  0, 17, 18, 19],:]
            v2 = joint[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],:]
            
            v = v2 - v1
            v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]
            compareV1 = v[[0, 1, 2, 4, 5, 6, 7,  8,  9, 10, 12, 13, 14, 16, 17],:]
            compareV2 = v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19],:]

            angle = np.arccos(np.einsum('nt,nt->n', compareV1, compareV2))
            angle = np.degrees(angle)
            
            data = np.array([angle], dtype=np.float32)
            ret, results, neighbours, dist = knn.findNearest(data, 3)
            index = int(results[0][0])
            if index in gesture.keys():
                if index != prev_index:
                    startTime = time.time()
                    prev_index = index
                else:
                    if time.time() - startTime > recognizeDelay:
                        if index == 1:
                            command_list = np.ones((200, 150, 3), np.uint8) * 255
                            command_list = cv2_draw_label(command_list, command_list_1[0], (10, 30))
                            command_list = cv2_draw_label(command_list, command_list_1[1], (10, 60))
                            command_list = cv2_draw_label(command_list, command_list_1[2], (10, 90))
                            sentence += gesture[index]
                        elif index == 0:
                            command_list = np.ones((200, 150, 3), np.uint8) * 255
                            command_list = cv2_draw_label(command_list, command_list_2[0], (10, 30))
                            command_list = cv2_draw_label(command_list, command_list_2[1], (10, 60))
                            command_list = cv2_draw_label(command_list, command_list_2[2], (10, 90))
                            sentence += gesture[index]
                            flag = 1
                        elif index == 4:
                            command_list = np.ones((200, 150, 3), np.uint8) * 255
                            command_list = cv2_draw_label(command_list, command_list_3[0], (10, 30))
                            command_list = cv2_draw_label(command_list, command_list_3[1], (10, 60))
                            command_list = cv2_draw_label(command_list, command_list_3[2], (10, 90))
                            sentence += gesture[index]
                        elif index == 31:
                            sentence += ' '
                        elif index == 32:
                            sentence = sentence[:-1]
                        elif index == 33:
                            if sentence[-1] == 'ㄱ':
                                temp_list = list(sentence)
                                temp_list[-1] = 'ㄲ'
                                sentence = ''.join(temp_list)
                            elif sentence[-1] == 'ㄷ':
                                temp_list = list(sentence)
                                temp_list[-1] = 'ㄸ'
                                sentence = ''.join(temp_list)
                            elif sentence[-1] == 'ㅂ':
                                temp_list = list(sentence)
                                temp_list[-1] = 'ㅃ'
                                sentence = ''.join(temp_list)
                            elif sentence[-1] == 'ㅅ':
                                temp_list = list(sentence)
                                temp_list[-1] = 'ㅆ'
                                sentence = ''.join(temp_list)
                            elif sentence[-1] == 'ㅈ':
                                temp_list = list(sentence)
                                temp_list[-1] = 'ㅉ'
                                sentence = ''.join(temp_list)
                            else:
                                pass
                        elif index == 34:
                            result_txt = ''
                            assistant_result = np.ones((200, 1500, 3), np.uint8) * 255
                            combined_sentence = join_jamos(sentence)
                            result_txt = assistant.assistant(combined_sentence)
                            assistant_result = cv2_draw_label(assistant_result, result_txt, (30, 30))
                            sentence = ''
                        elif index == 13:
                            result_txt = assistant.assistant("비")
                            assistant_result = np.ones((200, 1500, 3), np.uint8) * 255
                            assistant_result = cv2_draw_label(assistant_result, result_txt, (30, 30))
                        else:
                            sentence += gesture[index]
                        startTime = time.time()
                
            mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)
        
        
        final_sentence = join_jamos(sentence)
        img = cv2_draw_label(img, final_sentence, (30, 30))
        
        #cv2.namedWindow('HAND',cv2.WND_PROP_FULLSCREEN)
        #cv2.setWindowProperty('HAND', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.namedWindow('HAND', flags=cv2.WINDOW_GUI_NORMAL)
        
        
        cv2.imshow('HAND', img)
        cv2.waitKey(1)
        cv2.imshow('ASSISTANT RESULT', assistant_result)
        cv2.waitKey(1)
        cv2.imshow('COMMAND LIST', command_list)
        cv2.waitKey(1)
        
        if keyboard.is_pressed('q'):
            break