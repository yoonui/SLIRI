import numpy as np
import pyaudio as pa
import struct
import matplotlib.pyplot as plt
import threading
from message_sender import notice1
from message_sender import notice2
from audio_classifier import audio_classifier
from numpy.linalg import norm
import sys
import base64

def audio_listner():
    door_bell = np.array([38, 61, 56, 52, 78, 152, 67, 59, 55, 63, 61, 74, 86, 96,
                        154, 148, 133, 113, 106, 121, 129, 1440, 635, 418, 346, 310, 309, 259,
                        283, 253, 238, 277, 239, 207, 178, 3930, 3378, 1337, 635, 524, 480, 421,
                        372, 322, 310, 257, 227, 240, 218, 174, 147, 147, 126, 136, 126, 130,
                        92, 112, 135, 136, 122, 107, 84, 86, 111, 91, 98, 116, 96, 87,
                        116, 74, 116, 110, 84, 71, 68, 353, 1568, 604, 382, 274, 245, 234,
                        187, 191, 149, 136, 148, 109, 110, 104, 3385, 1437, 655, 540, 391, 306,
                        294, 259, 217, 169, 153, 139, 134, 105, 76, 75, 79, 97])

    fire_bell = np.array([38, 62, 61, 55, 752, 2402, 5007, 7327, 10762, 11411, 13894, 14925,
                        15829, 16138, 17106, 17270, 15776, 16192, 17380, 15662, 14245, 16808, 19154, 15399,
                        18168, 16246, 16871, 15285, 18651, 17013, 15506, 16092, 14529, 14724, 15549, 15580,
                        14279, 16170, 13064, 14202, 13502, 15602, 15814, 16440, 15009, 14194, 16314, 15835,
                        16039, 16557, 15159, 13107, 14851, 17189, 15060, 16172, 17848, 15310, 15561, 15243,
                        14199, 16730, 15719, 14433, 14563, 15831, 16281, 14648, 15733, 15279, 15122, 13711,
                        16254, 16978, 16318, 14531, 16876, 15337, 15775, 13949, 16185, 14565, 15232, 15570,
                        14435, 15544, 13487, 15950, 16198, 16138, 14995, 15178, 16790, 15106, 14427, 15640,
                        16183, 17807, 15936, 16256, 15525, 15117, 14785, 16013, 14546, 14626, 16300, 14704,
                        14630, 15663])

    ndoor = door_bell / norm(door_bell)
    nfire = fire_bell / norm(fire_bell)

    th1 = [threading.Thread(target=notice1) for i in range(9999)]
    th2 = [threading.Thread(target=notice2) for i in range(9999)]
    count_for_th1 = 0
    count_for_th2 = 0

    CHUNK = 1024 * 2
    FORMAT = pa.paInt16
    CHANNELS = 1
    RATE = 44100  # in Hz

    p = pa.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK
    )

    plt.rcParams['toolbar'] = 'None'
    print(plt.rcParams)
    fig, ax = plt.subplots()
    fig.canvas.toolbar_visible = False
    fig.canvas.header_visible = False
    fig.canvas.footer_visible = False
    x = np.arange(0, 2 * CHUNK, 2)
    line, = ax.plot(x, np.random.rand(CHUNK), 'r')
    ax.set_ylim(-60000, 60000)
    ax.ser_xlim = (0, CHUNK)
    plt.axis('off')
    fig.show()

    audio_vector = np.zeros(shape=(1, 110), dtype=np.int64)

    while 1:
        data = stream.read(CHUNK)
        dataInt = struct.unpack(str(CHUNK) + 'h', data)

        #시각화
        line.set_ydata(dataInt)

        # 화면 그리는 코드
        
        fig.canvas.draw()
        fig.canvas.flush_events()

        audio_vector[0] = np.append(audio_vector[0][1:], max(dataInt))

        # ny = audio_vector[0] / norm(audio_vector[0])
        # print("초인종과의 유사도: ", np.dot(ndoor, ny))
        # print("화재경보음과의 유사도: ", np.dot(nfire, ny))

        if audio_classifier(audio_vector[0], ndoor, nfire) == 1:
            if th1[count_for_th1].is_alive() == False:
                print(base64.b64encode("초인종이 울렸습니다".encode('utf-8')))
                # print("초인종이 울렸습니다")
                count_for_th1 += 1
                th1[count_for_th1].start()

        elif audio_classifier(audio_vector[0], ndoor, nfire) == 2:
            if th2[count_for_th2].is_alive() == False:
                print(base64.b64encode("화재경보가 울렸습니다".encode('utf-8')))
                # print("화재경보가 울렸습니다")
                count_for_th2 += 1
                th2[count_for_th2].start()
        else:
            continue

audio_listner()


