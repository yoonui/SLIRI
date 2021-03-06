import cv2
import mediapipe as mp
import numpy as np
import json
import time
import sys

gesture = {
    0:'ㄱ', 1:'ㄴ', 2:'ㄷ', 3:'ㄹ', 4:'ㅁ', 5:'ㅂ', 6:'ㅅ', 7:'ㅇ', 8:'ㅈ', 9:'ㅊ', 10:'ㅋ', 11:'ㅌ', 12:'ㅍ', 13:'ㅎ',
    14:'ㅏ', 15:'ㅑ', 16:'ㅓ', 17:'ㅕ', 18:'ㅗ', 19:'ㅛ', 20:'ㅜ', 21:'ㅠ', 22:'ㅡ', 23:'ㅣ', 24:'ㅐ', 25:'ㅔ', 26:'ㅚ',
    27:'ㅟ', 28:'ㅒ', 29:'ㅖ', 30:'ㅢ', 31:'SPACE', 32:'BACKSPACE', 33:'DUAL', 34:'END'
} 

f = open("./server/hand_recog/sentence.txt", 'a')
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

#json_file = 'input_data.json'
#temp_json = {"x":0.3372095823287964,"y":0.902660608291626,"z":5.018708861825871e-7},{"x":0.41383764147758484,"y":0.8607039451599121,"z":-0.027471745386719704},{"x":0.47277435660362244,"y":0.7686975598335266,"z":-0.03569439426064491},{"x":0.5075134634971619,"y":0.6851124167442322,"z":-0.042380355298519135},{"x":0.5439475774765015,"y":0.6318556070327759,"z":-0.04866192489862442},{"x":0.4368062913417816,"y":0.6360199451446533,"z":-0.0202465932816267},{"x":0.4738960266113281,"y":0.5392283797264099,"z":-0.039549604058265686},{"x":0.4956793189048767,"y":0.4786164462566376,"z":-0.055051326751708984},{"x":0.5134190320968628,"y":0.42677390575408936,"z":-0.06685959547758102},{"x":0.3871287405490875,"y":0.6172264218330383,"z":-0.02346825785934925},{"x":0.40324264764785767,"y":0.500792920589447,"z":-0.03965744376182556},{"x":0.4180578589439392,"y":0.42851823568344116,"z":-0.05348767712712288},{"x":0.4303758442401886,"y":0.3682805299758911,"z":-0.06389404833316803},{"x":0.33896133303642273,"y":0.6268112063407898,"z":-0.0312191192060709},{"x":0.3363065719604492,"y":0.5221719741821289,"z":-0.051034361124038696},{"x":0.3392335772514343,"y":0.45192837715148926,"z":-0.06793797761201859},{"x":0.3450028896331787,"y":0.3906233012676239,"z":-0.0802854374051094},{"x":0.2921903431415558,"y":0.6614280939102173,"z":-0.04165244847536087},{"x":0.2573757767677307,"y":0.5920097231864929,"z":-0.06416364759206772},{"x":0.23492537438869476,"y":0.5432913899421692,"z":-0.07699637115001678},{"x":0.21870076656341553,"y":0.49346932768821716,"z":-0.08524598926305771}

temp_json = sys.argv[1]
#print(temp_json)

#print("type of temp_json")
#print(type(temp_json))
#print("type of data(asd)")
#print(type(asd))

#with open(json_file) as json_data_temp:
#    json_data = json.load(json_data_temp)
#print(json_data)

joint = np.zeros((21,3))

for i in range(21):
    joint[i] = [temp_json[i]["x"], temp_json[i]["y"], temp_json[i]["z"]]
    print(joint[i])

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
        f.write(sentence)
        sentence = ''
    else:
        sentence += gesture[index]
    startTime = time.time()

print(sentence)
f.close()
        