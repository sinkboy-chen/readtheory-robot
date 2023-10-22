from selenium import webdriver
import requests
from requests.structures import CaseInsensitiveDict
import os

from answer import *
from session import *

# change
n = 4000

session = get_session()
answerkey = get_answerkey()
for i in range(n):
    if (i%10==0):
        save_answerkey(answerkey)
    parentId, answerIdList = get_question(session)
    if parentId in answerkey.keys():
        iscorrect, correct_answerId = submit_answer(session, answerkey[parentId], parentId)
    else:
        iscorrect, correct_answerId = submit_answer(session, answerIdList[0], parentId)
        answerkey[parentId] = correct_answerId
    print(f"question {i} out of {n} is {'correct' if iscorrect else 'not correct'}")
save_answerkey(answerkey)
