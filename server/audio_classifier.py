import numpy as np
from numpy.linalg import norm

def audio_classifier(y, ndoor, nfire):

    ny = y / norm(y)

    if np.dot(ndoor, ny) >= 0.9:
        return 1
    elif np.dot(nfire, ny) >= 0.9:
        return 2
    elif y == 0:
        return 3
    else:
        return 4
