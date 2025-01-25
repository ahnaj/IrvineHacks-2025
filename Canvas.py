import pickle
import pyperclip
import time

from canvasapi import Canvas

API_URL = "https://canvas.eee.uci.edu"
api_token_url = "https://canvas.eee.uci.edu/profile/settings"

def write_token(token):
    with open("save.pkl", "wb") as file:
        pickle.dump(token, file)

def get_saved_token(): 
    try: 
        with open("save.pkl", "rb") as file:
            return pickle.load(file)
    except:
        return "" 
    
def get_username(token):
    canvas = Canvas(API_URL, token)
    user = canvas.get_user('self')
    print(f"Connected as {user.name}")
    return user

def check_valid_token(token):
    return token.strip() and connect_to_canvas(token)
    
def connect_to_canvas(api_key):
    canvas = Canvas(API_URL, api_key)
    try:
        user = canvas.get_user('self')
        print(f"Connected as {user.name}")
        return True
    except Exception as e:
        print(f"Failed to connect: {e}")
        return False