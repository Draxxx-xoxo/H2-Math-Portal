import numpy as np
from numpy import random
import random as rand
from handlers.common_math_func import vector_calculate_area, projection_vector, calculate_coordinates, parallel_intersection, parse_asciimath, substitute_and_evaluate
from datetime import datetime, timedelta
from handlers.wolframe_api import wolframe_api
import json
import pytz

def read_json():
    with open("data/equations.json", "r") as file:
        data = json.load(file)
    return data
    
def string_format(string, id, a_, b_, c_, ab, ac):

    if id == "6c7d000b-f24e-47ab-bfad-b9b9042b4981":
        a = f"`(({a_[0]}), ({a_[1]}), ({a_[2]}))`"
        b = f"`(({b_[0]}), ({b_[1]}), ({b_[2]}))`"
        c = f"`(({c_[0]}), ({c_[1]}), ({c_[2]}))`"
        string = string.format(a = a, b = b, c = c)
    elif id == "cbde540a-5226-417d-83dd-89d73d7ab3ad":
        a = f"`(({a_[0]}), ({a_[1]}), ({a_[2]}))`"
        b = f"`(({b_[0]}), ({b_[1]}), ({b_[2]}))`"
        string = string.format(a = a, b = b)
    elif id == "e214d1c2-0733-48c9-b626-85f1f95475c3":
        a = f"`int {a_} dx`"
        string = string.format(a = a)
    elif id == "4420ab72-e9b9-4870-975f-fa3a4ea6da37":
        a = f"`{a_}`"
        string = string.format(a = a)
    elif id == "b4d10953-c763-4dd2-bc60-221e4a0d658a":
        a = f"`({a_[0]}, {a_[1]}, {a_[2]})`"
        b = f"`({b_[0]}, {b_[1]}, {b_[2]})`"
        string = string.format(a = a, c = b, ab = ab, ac = ac)
    elif id == "79c0e3e6-403d-4db8-80d8-5fe01d54faa3":
        a = f"`l_1 = r = ((x_0), (y_0), (z_0)) + t((a), (b), (c))`"
        b = f"`l_2 = r = ((x_0), (y_0), (z_0)) + t((a), (b), (c))`"
        string = string.format(a = a, b = b)


    return string

def values(id):
    value_dict = {
        "answer": "",
        "correct": False
    }

    if id == "6c7d000b-f24e-47ab-bfad-b9b9042b4981":
        a = random.randint(20, size=(3))
        b = random.randint(20, size=(3))
        c = random.randint(20, size=(3))


        value_dict.update({
            "a": a.tolist(),
            "b": b.tolist(),
            "c": c.tolist(),
        })

    elif id == "cbde540a-5226-417d-83dd-89d73d7ab3ad":
        a = random.randint(20, size=(3))
        b = random.randint(20, size=(3))

        value_dict.update({
            "a": a.tolist(),
            "b": b.tolist(),
        })

    elif id == "b4d10953-c763-4dd2-bc60-221e4a0d658a":
        a = random.randint(20, size=(3))
        b = random.randint(20, size=(3))
        ab = rand.randint(1, 10)
        ac = rand.randint(1, 10)

        value_dict.update({
            "a": a.tolist(),
            "b": b.tolist(),
            "ab": ab,
            "ac": ac
        })
    elif id == "79c0e3e6-403d-4db8-80d8-5fe01d54faa3":
        a = random.randint(10, size=(3))
        ad = random.randint(10, size=(3))
        b = random.randint(10, size=(3))
        bd = random.randint(10, size=(3))

        value_dict.update({
            "a": a.tolist(),
            "b": b.tolist(),
            "ab": ad.tolist(),
            "ac": bd.tolist()
        })
    
    elif id == "4420ab72-e9b9-4870-975f-fa3a4ea6da37":
        a = random.randint(2, 10, size=(5))
        data = read_json()
        equations = data['differentiation']['equations']
        equation = random.choice(equations)

        equation = equation.format(a = a[0], b = a[1], c = a[2], d = a[3], e = a[4])

        query = "Differentiate " + equation + " with respect to x"

        correct_answer = wolframe_api(query)

        value_dict.update({
            "a": a.tolist(),
            "equation": equation,
            "correct_answer": correct_answer
        })
    
    elif id == "e214d1c2-0733-48c9-b626-85f1f95475c3":
        a = random.randint(2, 10, size=(5))
        data = read_json()
        equations = data['integration']['equations']
        equation = random.choice(equations)

        equation = equation.format(a = a[0], b = a[1], c = a[2], d = a[3], e = a[4])

        query = "Integrate" + equation + " with respect to x"

        correct_answer = wolframe_api(query)

        value_dict.update({
            "a": a.tolist(),
            "equation": equation,
            "correct_answer": correct_answer
        })

    return value_dict

    

def create_session(supabase, user_id, quiz_id):

    questions = supabase.table("quiz").select("question_1, question_2, question_3, question_4, question_5").eq("quiz_id", quiz_id).execute()

    response = supabase.table("session_quiz").insert({"user": user_id, "quiz_id": quiz_id}).execute()
    session_id = response.data[0]['session_id']

    len_questions = 0

    for question in questions.data[0]:

        if questions.data[0][question] == None:
            continue
        else:
            response = supabase.table("question").select("*").eq("question_id", questions.data[0][question]).execute()
            id = response.data[0]['question_id'] 
            
            values_json = values(id)
            

            response = (
                supabase.table("session_quiz")
                .update({question: values_json})
                .eq("session_id", session_id)
                .execute()
            )

            len_questions += 1

    return session_id, len_questions


def initalise_quiz(supabase, session_id, quiz_id):

    tz = pytz.timezone('Asia/Singapore')
    start_time = datetime.now(tz)

    res = supabase.table("quiz").select("time_limit").eq("quiz_id", quiz_id).execute()
    minutes = res.data[0]['time_limit']
    end_time = start_time + timedelta(minutes=minutes)


    supabase.table("session_quiz").update({"start_time": str(start_time), "is_active": True, "end_time": str(end_time)}).eq("session_id", session_id).execute()


    

def retrieve_correct(quiz_id, question_no, supabase, session_id, quiz_len):

    correct_dict = {}

    for i in range(1, quiz_len + 1):
        value_dict = supabase.table("session_quiz").select(f"question_{i}").eq("session_id", session_id).execute()
        value_dict = value_dict.data[0][f"question_{i}"]
        correct = value_dict['correct']
    
        correct_dict[f"question_{i}"] = correct
        
    return correct_dict


def retrieve_question(quiz_id, question_no, supabase, session_id):

    questions_lis = []

    quiz = supabase.table("quiz").select(f"question_{question_no}", "question_count", "time_limit").eq("quiz_id", quiz_id).execute()
    quiz_len = quiz.data[0]['question_count']

    question_id = quiz.data[0][f"question_{question_no}"]
    question = supabase.table("question").select("*").eq("question_id", question_id).execute()
    question_ = question.data[0]['question']
    marks = question.data[0]['marks']
    topic = question.data[0]['topic']

    value_dict = supabase.table("session_quiz").select(f"question_{question_no}", "end_time").eq("session_id", session_id).execute()
    end_time = value_dict.data[0]['end_time']
    value_dict = value_dict.data[0][f"question_{question_no}"]
    correct = value_dict['correct']
    user_answer = value_dict['answer']
    #correct_answer = value_dict['correct_answer']

    a = None
    b = None
    c = None
    ab = None
    ac = None

    if question_id == "6c7d000b-f24e-47ab-bfad-b9b9042b4981":

        a = np.array(value_dict['a'])
        b = np.array(value_dict['b'])
        c = np.array(value_dict['c'])
        
    elif question_id == "cbde540a-5226-417d-83dd-89d73d7ab3ad":
            
        a = np.array(value_dict['a'])
        b = np.array(value_dict['b'])
    
    elif question_id == "b4d10953-c763-4dd2-bc60-221e4a0d658a":
        a = np.array(value_dict['a'])
        b = np.array(value_dict['b'])
        ab = value_dict['ab']
        ac = value_dict['ac']
    elif question_id == "79c0e3e6-403d-4db8-80d8-5fe01d54faa3":
        a = np.array(value_dict['a'])
        b = np.array(value_dict['b'])
    elif question_id == "e214d1c2-0733-48c9-b626-85f1f95475c3":
        equation = value_dict['equation']
        a = equation
    elif question_id == "4420ab72-e9b9-4870-975f-fa3a4ea6da37":
        equation = value_dict['equation']
        a = equation

    question_ = string_format(question_, question_id, a, b, c, ab, ac)

    question_dict = {
        "question": question_,
        "marks": marks,
        "topic": topic,
        "id": question_id,
        "correct": correct,
        "user_answer": user_answer
    }

    questions_lis.append(question_dict)

    correct_dict = retrieve_correct(quiz_id, question_no, supabase, session_id, quiz_len)

    return questions_lis, quiz_len, correct_dict, end_time


def check_answer(points, supabase, id, answer, session_id, question_no):

    value_dict = supabase.table("session_quiz").select(f"question_{question_no}", "user").eq("session_id", session_id).execute()
    user_id = value_dict.data[0]['user']
    value_dict = value_dict.data[0][f"question_{question_no}"]


    results = False
    if id == "6c7d000b-f24e-47ab-bfad-b9b9042b4981":
        a = value_dict['a']
        b = value_dict['b']
        c = value_dict['c']
        results = vector_calculate_area(a, b, c, answer)
    elif id == "cbde540a-5226-417d-83dd-89d73d7ab3ad":
        a = value_dict['a']
        b = value_dict['b']
        results = projection_vector(a, b, answer)
    elif id == "b4d10953-c763-4dd2-bc60-221e4a0d658a":
        a = value_dict['a']
        b = value_dict['b']
        ab = value_dict['ab']
        ac = value_dict['ac']
        results = calculate_coordinates(a, b, ab, ac, answer)
    elif id == "79c0e3e6-403d-4db8-80d8-5fe01d54faa3":
        a = value_dict['a']
        b = value_dict['b']
        ab = value_dict['ab']
        ac = value_dict['ac']
        results = parallel_intersection(a, b, ab, ac, answer)
    elif id == "e214d1c2-0733-48c9-b626-85f1f95475c3":
        correct_answer = value_dict['correct_answer']
        correct_answer_parse = parse_asciimath(correct_answer)
        correct_results = substitute_and_evaluate(correct_answer_parse, {"x": 5})

        try:
            input_answer = parse_asciimath(answer)
            final_results = substitute_and_evaluate(input_answer, {"x": 5})
        except:
            results = False
        
        if final_results == correct_results:
            results = True
        else: 
            results = False

        print(correct_answer)
        print(input_answer)
        print(correct_answer_parse)
        print(correct_results)
        print(final_results)

    elif id == "4420ab72-e9b9-4870-975f-fa3a4ea6da37":
        correct_answer = value_dict['correct_answer']
        correct_answer_parse = parse_asciimath(correct_answer)
        correct_results = substitute_and_evaluate(correct_answer_parse, {"x": 5})

        try:
            input_answer = parse_asciimath(answer)
            results = substitute_and_evaluate(input_answer, {"x": 5})
        except:
            results = False
        
        if results == correct_results:
            results = True
        else: 
            results = False
        
        print(correct_answer)
        print(input_answer)
        print(correct_answer_parse)
        print(correct_results)
        print(results)



    if results == True:
        add_points(points, supabase, user_id)
        value_dict["answer"] = answer
        value_dict["correct"] = True

        supabase.table("session_quiz").update({f"question_{question_no}": value_dict}).eq("session_id", session_id).execute() 
    else:
        value_dict["answer"] = answer
        supabase.table("session_quiz").update({f"question_{question_no}": value_dict}).eq("session_id", session_id).execute()

    return results

def add_points(points, supabase, user_id):

    fetch_points = supabase.table("leaderboard").select("points").eq("user", user_id).execute()

    points = fetch_points.data[0]['points'] + int(points)
    tz = pytz.timezone('Asia/Singapore')
    updated_at = datetime.now(tz)


    supabase.table("leaderboard").update({"points": points, "updated_at": str(updated_at)}).eq("user", user_id).execute()





 