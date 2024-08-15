import numpy as np
import ast
from sympy import sympify, latex
import logging
from py_asciimath.translator.translator import ASCIIMath2Tex
from sympy import symbols, sqrt, sympify 
from sympy.parsing.latex import parse_latex

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

def calculate_coordinates(a, c, ab, ac, answer):
    # Calculate n = ac - ab
    n = ac - ab
    
    # Convert a and c to numpy arrays
    a = np.array(a)
    c = np.array(c)
    
    # Calculate coordinates of B using the section formula
    b = (ab * c + n * a) / (ab + ac)

    try:
        answer = ast.literal_eval(answer)
        answer = np.array(answer)
        print(b, answer)
        if np.array_equal(answer, b):
            return True
        else:
            return False
    except:
        return False
    
# Function to determine if two vectors are parallel
def are_parallel(d1, d2):
    cross_product = np.cross(d1, d2)
    return np.allclose(cross_product, np.zeros(3))

# Function to check if lines intersect
def check_intersection(r1, d1, r2, d2):
    A = np.vstack((d1, -d2, np.cross(d1, d2)))
    if np.linalg.matrix_rank(A) < 3:
        # If the matrix rank is less than 3, the lines are either parallel or intersect
        t = np.linalg.lstsq(A[:2,:2], r2 - r1, rcond=None)[0]
        intersection_point = r1 + t[0] * d1
        if np.allclose(intersection_point, r2 + t[1] * d2):
            return "Intersecting", intersection_point
        else:
            return "Skew", None
    return "Skew", None

def parallel_intersection(r1, r2, d1, d2, answer):
    # Check if the lines are parallel
    if are_parallel(d1, d2):
        result = "Parallel"
        intersection_point = None
    else:
        # Check if the lines intersect or are skew
        result, intersection_point = check_intersection(r1, d1, r2, d2)

    if result == answer[0] and intersection_point == answer[1]:
        return True
    else:
        return False
    

def parse_asciimath(ascii_expr):

    asciimath2tex = ASCIIMath2Tex(log=False, inplace=True)
    ascii_expr = asciimath2tex.translate(
        ascii_expr,
        displaystyle=False,
        from_file=False,
        pprint=False,
    )

    ascii_expr = ascii_expr[1:-1]
    sympy_expr = parse_latex(ascii_expr)

    print(sympy_expr)

    return sympy_expr

def substitute_and_evaluate(expr, values):
    # Substitute values into the expression
    substituted_expr = expr.subs(values)
    # Evaluate the substituted expression
    evaluated_result = substituted_expr.evalf()
    return evaluated_result




