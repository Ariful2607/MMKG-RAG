import numpy as np

def cosine_similarity(a, b):
    a = np.asarray(a)
    b = np.asarray(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )