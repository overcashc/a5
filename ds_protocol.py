# Michael Yeung
# myeung2@uci.edu
# 71598323

import json
import time
import sys

def join(username: str, password: str): 
  '''
  This function will organize the username and password in json format
  '''
  join_str = {"join": {"username": username, "password": password, "token": ""}}
  json_join_str = json.dumps(join_str)
  return json_join_str

def post(token: str, message: str): 
  '''
  This function will organize the token and message in json format
  '''
  send_msg = {"token": token, "post": {"entry": message,"timestamp": time.time()}}  
  json_send_msg = json.dumps(send_msg)
  return json_send_msg

def bio(token: str, bio: str): 
  '''
  This function will organize the token and bio in json format
  '''
  send_bio = {"token": token, "bio": {"entry": bio,"timestamp": time.time()}}
  json_send_bio = json.dumps(send_bio)
  return json_send_bio

def extract_json(json_msg: str):
  '''
  Call the json.loads function to change the json_msg from a str to a dict and extracts the token & message using key value pairing
  '''
  try:
    json_obj = json.loads(json_msg)
    token = json_obj["response"]["token"]
    response = json_obj["response"]["message"]
  except json.JSONDecodeError:
    print("Json cannot be decoded.")
  except KeyError:
    print("Please retry again with the correct username and password")
    sys.exit()
  return token, response

def extract_msg(json_msg: str):
  '''
  Calls the json.loads function to change the json_msg from a str to a dict and extracts the "post published to ds server" msg
  '''
  try:
    json_obj = json.loads(json_msg)
    message = json_obj["response"]["message"]
  except json.JSONDecodeError:
    print("Json cannot be decoded")
  return message