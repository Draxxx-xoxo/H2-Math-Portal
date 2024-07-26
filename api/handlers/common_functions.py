import numpy as np
import random

def vector_calculate_area(string):

    a = (1, 2, 5)
    b = (3, 4, 2)
    c = (5, 6 ,1)

    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    cross = np.cross(b - a, c - a)
    area = 0.5 * np.linalg.norm(cross)

    print(area)


def string_format(string, id):

    if id == "6c7d000b-f24e-47ab-bfad-b9b9042b4981":
        a = r"$ \begin{pmatrix} 1 \\ 2 \\ 5 \end{pmatrix} $"
        b = r"$ \begin{pmatrix} 3 \\ 4 \\ 2 \end{pmatrix} $"
        c = r"$ \begin{pmatrix} 5 \\ 6 \\ 1 \end{pmatrix} $"
        string = string.format(a = a, b = b, c = c)
    elif id == "cbde540a-5226-417d-83dd-89d73d7ab3ad":
        a = r"$ \begin{pmatrix} 1 \\ 2 \\ 5 \end{pmatrix} $"
        b = r"$ \begin{pmatrix} 3 \\ 4 \\ 2 \end{pmatrix} $"
        string = string.format(a = a, b = b)
    elif id == "e214d1c2-0733-48c9-b626-85f1f95475c3":
        a = r"$\int (3 - 2x)^4 \, dx$"
        string = string.format(a = a)


    return string


def initalise_quiz(supabase, quiz_id):

    questions_lis = []

    questions = supabase.table("quiz").select("question_1, question_2, question_3, question_4, question_5").eq("quiz_id", quiz_id).execute()

    for question in questions.data[0]:

        if questions.data[0][question] == None:
            continue
        else:
            response = supabase.table("questions").select("*").eq("question_id", questions.data[0][question]).execute()
            question_ = response.data[0]['question']
            marks = response.data[0]['marks']
            topic = response.data[0]['topic']
            id = response.data[0]['question_id'] 

            question_ = string_format(question_, id)

            question_dict = {
                "question": question_,
                "marks": marks,
                "topic": topic
            }

            questions_lis.append(question_dict)

    return questions_lis


