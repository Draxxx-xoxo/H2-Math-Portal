import numpy as np

def vector_calculate_area(a, b, c, answer):

    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    cross = np.cross(b - a, c - a)
    area = 0.5 * np.linalg.norm(cross)

    print(area)
    print(answer)

    try:
        if area == float(answer):
            return True
        else:
            return False
    except:
        return False