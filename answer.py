import requests
from requests.structures import CaseInsensitiveDict
import os
import pickle

def get_question(session):
    url = "https://readtheory.org/app/student/quiz"
    resp = session.get(url)
    content = resp.text
    content = resp.text.split("window.rt_bridge_page_data.questions[")
    
    for i in range(1, len(content), 2):
        if "correctAnswerId" not in content[i]:
            index = i
            break

    parentId = content[i].split('parentId":')[-1].split(",")[0]
    answerIds = content[i].split('answerList":')[1].split(";")[0]
    answerIds = answerIds[:-1]
    answerIds = answerIds.split('"answerId":')
    answerIdList = [x.split(",")[0] for x in answerIds[1:]]

    return parentId, answerIdList


def submit_answer(session, answerId, parentId):
    url = "https://readtheory.org/reading/answerQuestion"
    headers = CaseInsensitiveDict()
    headers["authority"] = "readtheory.org"
    headers["content-type"] = "application/x-www-form-urlencoded"
    headers["x-requested-with"] = "XMLHttpRequest"
    data = f"isSelected=true&answerId={answerId}&parentId={parentId}"
    resp = session.post(url, headers=headers, data=data)
    iscorrect = resp.text.split('"correct":')[1].split(",")[0]
    if iscorrect=="true":
        iscorrect = 1
    else :
        iscorrect = 0
    correct_answerId = resp.text.split('correctAnswerId":')[1].split(",")[0]
    return iscorrect, correct_answerId

def get_answerkey():
    # answerkey dictionary
    if os.path.exists('answerkey.pkl'):
        print("answerkey.pkl file exists.")
        with open('answerkey.pkl', 'rb') as answerkey_file:
            answerkey = pickle.load(answerkey_file)
    else:
        print("answerkey.pkl file does not exist.")
        answerkey = {}

    return answerkey

def save_answerkey(answerkey):
    with open('answerkey.pkl', 'wb') as answerkey_file:
        pickle.dump(answerkey, answerkey_file)

    print(f"saved answerkey with {len(answerkey)} answers")
