import json
import pickle
import fbchat
from pathlib import Path
import importlib


# load in json file, if it exists
# ideally use this for loading in config files and cookie files
def load_json(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return

# dumps a dictionary to a file specified by filename
def save_json(filename, cookies):
    try:
        with open(filename, "w") as f:
            json.dump(cookies, f)
        return True
    except:
        return False


def get_login_credentials(filename):
    my_file = Path(filename)
    if my_file.is_file():
        mod = importlib.import_module(filename[:len(filename)-3])
        user_agent = mod.USER_AGENT
        username = mod.FB_EMAIL
        password = mod.FB_PASS
        return {'user_agent': user_agent, 
            'username':username, 
            'password':password}
    else:
        return

def load_session(cookies):
    if not cookies:
        return
    try:
        return fbchat.Session.from_cookies(cookies)
    except fbchat.FacebookError:
        return  # Failed loading from cookies

#delays a random amount between float1 and float2
def rand_delay(float1, float2):
	delay3 = random.uniform(float1, float2)
	time.sleep(delay3)
	