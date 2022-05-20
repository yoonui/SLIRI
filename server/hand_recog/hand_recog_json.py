import cv2
import mediapipe as mp
import numpy as np
import json
import time
import platform
from PIL import ImageFont, ImageDraw, Image

import base64
import sys


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
    draw.text((x, y), text, font=imageFont, fill=(255, 255, 255))
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    return image

max_num_hands = 1

gesture = {
    0:'ㄱ', 1:'ㄴ', 2:'ㄷ', 3:'ㄹ', 4:'ㅁ', 5:'ㅂ', 6:'ㅅ', 7:'ㅇ', 8:'ㅈ', 9:'ㅊ', 10:'ㅋ', 11:'ㅌ', 12:'ㅍ', 13:'ㅎ',
    14:'ㅏ', 15:'ㅑ', 16:'ㅓ', 17:'ㅕ', 18:'ㅗ', 19:'ㅛ', 20:'ㅜ', 21:'ㅠ', 22:'ㅡ', 23:'ㅣ', 24:'ㅐ', 25:'ㅔ', 26:'ㅚ',
    27:'ㅟ', 28:'ㅒ', 29:'ㅖ', 30:'ㅢ', 31:'SPACE', 32:'BACKSPACE', 33:'DUAL'
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

startTime = time.time()
prev_index = 0
sentence = ''
recognizeDelay = 2

json_file = './server/hand_recog/input_data.json'

with open(json_file) as json_data_temp:
    json_data = json.load(json_data_temp)

joint = np.zeros((21,3))

for j in range(21):
    joint[j] = [json_data[0][j]['x'], json_data[0][j]['y'], json_data[0][j]['x']]

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
    # 31:'SPACE', 32:'BACKSPACE', 33:'DUAL', 34:'END'
    # ㄱ, ㄷ, ㅂ, ㅅ, ㅈ
    # ㄱ : 0, ㄷ : 2, ㅂ : 5, ㅅ : 6, ㅈ:8
    if index == 31:
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
        # send sentence
        sentence = ''
    else:
        sentence += gesture[index]
    startTime = time.time()

print(base64.b64encode(sentence.encode('utf-8')))

#f.close()
        