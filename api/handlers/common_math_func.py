import numpy as np
from sympy import symbols, integrate # type: ignore
import ast

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
    

def projection_vector(a, b, answer):

# It is given that a =  and b = . Given that the projection vector of a on b is xi + yj + zk, find the values of x, y and z.

    a = np.array(a)
    b = np.array(b)

    projection = np.round(np.dot(a, b) / np.dot(b, b) * b, decimals=2)

    print(a)
    print(b)
    print(projection)

    try:
        answer = ast.literal_eval(answer)
        answer = np.array(answer)
        if np.array_equal(answer, projection):
            return True
        else:
            return False
    except:
        return False
    


def integration():
    x = symbols('x')

    # Define the expression
    expr = (3 - 2*x)**4

    # Perform the integration
    result = integrate(expr, x)

    # Print the result
    print(result)