# import numpy as np
# from numpy.linalg import norm
# import threading
# from message_sender import notice1
# from message_sender import notice2
# from make_sentence import join_jamos
# from hand_recog import hand_recog
from assistant import assistant
from audio_classifier import audio_classifier

# letter = "L"
def front_sign_in():
    data = "완료"
    return data

def front_text_out(output):
    print(output)

def front_audio_in():
    return audio

# word = "날씨"

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

while 1:
    audio_vector = np.zeros(shape=(1, 110), dtype=np.int64)

    th1 = [threading.Thread(target=notice1) for i in range(999)]
    th2 = [threading.Thread(target=notice2) for i in range(999)]
    count_for_th1 = 0
    count_for_th2 = 0

    while 1:
        audio = front_audio_in() #프론트에서 오디오 데이터 받아옴

        audio_vector[0] = np.append(audio_vector[0][1:], audio) #audio가 하나의 정수라면, 아니면 수정하고

        audio_type = audio_classifier(audio_vector[0], ndoor, nfire)

        if audio_type == 1:
            if th1[count_for_th1].is_alive() == False:
                #print("초인종이 울렸습니다")
                count_for_th1 += 1
                th1[count_for_th1].start()

        elif audio_type == 2:
            if th2[count_for_th2].is_alive() == False:
                #print("화재경보가 울렸습니다")
                count_for_th2 += 1
                th2[count_for_th2].start()

        elif audio_type == 3:
            #프론트로 전달해야됨
            break

        else:
            continue


# def front_sign_in():
#     data = "완료"
#     return data


# def front_text_out(output):
#     print(output)


# def front_audio_in():
#     return audio

# # word = "날씨"

#     # door_bell = np.array([38, 61, 56, 52, 78, 152, 67, 59, 55, 63, 61, 74, 86, 96,
#     #                       154, 148, 133, 113, 106, 121, 129, 1440, 635, 418, 346, 310, 309, 259,
#     #                       283, 253, 238, 277, 239, 207, 178, 3930, 3378, 1337, 635, 524, 480, 421,
#     #                       372, 322, 310, 257, 227, 240, 218, 174, 147, 147, 126, 136, 126, 130,
#     #                       92, 112, 135, 136, 122, 107, 84, 86, 111, 91, 98, 116, 96, 87,
#     #                       116, 74, 116, 110, 84, 71, 68, 353, 1568, 604, 382, 274, 245, 234,
#     #                       187, 191, 149, 136, 148, 109, 110, 104, 3385, 1437, 655, 540, 391, 306,
#     #                       294, 259, 217, 169, 153, 139, 134, 105, 76, 75, 79, 97])
#     #
#     # fire_bell = np.array([38, 62, 61, 55, 752, 2402, 5007, 7327, 10762, 11411, 13894, 14925,
#     #                       15829, 16138, 17106, 17270, 15776, 16192, 17380, 15662, 14245, 16808, 19154, 15399,
#     #                       18168, 16246, 16871, 15285, 18651, 17013, 15506, 16092, 14529, 14724, 15549, 15580,
#     #                       14279, 16170, 13064, 14202, 13502, 15602, 15814, 16440, 15009, 14194, 16314, 15835,
#     #                       16039, 16557, 15159, 13107, 14851, 17189, 15060, 16172, 17848, 15310, 15561, 15243,
#     #                       14199, 16730, 15719, 14433, 14563, 15831, 16281, 14648, 15733, 15279, 15122, 13711,
#     #                       16254, 16978, 16318, 14531, 16876, 15337, 15775, 13949, 16185, 14565, 15232, 15570,
#     #                       14435, 15544, 13487, 15950, 16198, 16138, 14995, 15178, 16790, 15106, 14427, 15640,
#     #                       16183, 17807, 15936, 16256, 15525, 15117, 14785, 16013, 14546, 14626, 16300, 14704,
#     #                       14630, 15663])
#     #
# ndoor = door_bell / norm(door_bell)
# nfire = fire_bell / norm(fire_bell)

# while 1:
#     audio_vector = np.zeros(shape=(1, 110), dtype=np.int64)

#     th1 = [threading.Thread(target=notice1) for i in range(999)]
#     th2 = [threading.Thread(target=notice2) for i in range(999)]
#     count_for_th1 = 0
#     count_for_th2 = 0

#     while 1:
#         audio = front_audio_in()  # 프론트에서 오디오 데이터 받아옴

#         # audio가 하나의 정수라면, 아니면 수정하고
#         audio_vector[0] = np.append(audio_vector[0][1:], audio)

#         audio_type = audio_classifier(audio_vector[0], ndoor, nfire)

#         if audio_type == 1:
#             if th1[count_for_th1].is_alive() == False:
#                 #print("초인종이 울렸습니다")
#                 count_for_th1 += 1
#                 th1[count_for_th1].start()

#         elif audio_type == 2:
#             if th2[count_for_th2].is_alive() == False:
#                 #print("화재경보가 울렸습니다")
#                 count_for_th2 += 1
#                 th2[count_for_th2].start()

#         elif audio_type == 3:
#             # 프론트로 전달해야됨
#             break

#         else:
#             continue

#     letters = []  # 입력한 문자들을 리스트로 저장
#     word = ''

#     while 1:
#         sign = front_sign_in()  # 프론트에서 mediapipe로 계산된 데이터 전달 받음

#         if sign != 'none':  # 전달 받은 데이터가 유의미 할 경우
#             letter = hand_recog(sign)  # 전달 받은 데이터 인식 시도

#             if letter == '완료':  # 사용자가 완료 사인을 입력할 경우
#                 output = assistant(word)  # 조합된 단어 비서로 전달
#                 front_text_out(output)  # 웹으로 전달
#                 letters.clear()  # 저장된 문자들 삭제
#                 break

#             elif letter == '삭제':  # 사용자가 삭제를 위한 사인을 입력할 경우
#                 letters.pop()  # 마지막 입력한 문자 삭제
#                 word = join_jamos(letters)  # 문자들 재조합
#                 front_text_out(word)  # 웹으로 전달

#             elif letter != 'none':  # 전달 받은 데이터가 인식 가능할 경우
#                 letters.append(letter)  # 문자 저장소에 저장
#                 word = join_jamos(letters)  # 새로운 문자와 함께 조합
#                 front_text_out(word)  # 웹으로 전달

#             else:
#                 continue


ouput_text = assistant("날씨")
print(ouput_text)
