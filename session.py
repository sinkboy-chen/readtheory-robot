import requests
import pickle
from selenium import webdriver
import os

# login and return cookies
def login():
    username = input("username: ")
    password = input("password: ")
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://readtheory.org/auth/login")

    driver.find_element("id", "username").send_keys(username)
    driver.find_element("id", "password").send_keys(password)
    driver.find_element("name", "ajaxLogin").click()
    cookies = driver.get_cookies()

    # Close the browser
    driver.quit()
    return cookies

def save_cookie(session):
    with open('cookies.pkl', 'wb') as cookies_file:
        pickle.dump(session.cookies, cookies_file)
        
def get_session():
    # Check if cookies.pkl file exists
    if os.path.exists('cookies.pkl'):
        print("cookies.pkl file exists.")
        session = open_session()
    else:
        print("cookies.pkl file does not exist.")
        cookies = login() 
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        save_cookie(session)

    return session

    

def open_session():
    # Load cookies from the file using pickle
    with open('cookies.pkl', 'rb') as cookies_file:
        cookies = pickle.load(cookies_file)

    # Create a new session object
    session = requests.Session()

    # Assign the loaded cookies to the session
    session.cookies.update(cookies)

    return session
