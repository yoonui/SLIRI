import numpy as np
from numpy.linalg import norm

def audio_classifier(y, ndoor, nfire):

    ny = y / norm(y)
    # np.dot(ndoor, ny)

    if np.dot(ndoor, ny) >= 0.9:
        return 1
    elif np.dot(nfire, ny) >= 0.9 and max(y) >= 10000:
        return 2
    else:
        return 3
