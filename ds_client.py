# Michael Yeung
# myeung2@uci.edu
# 71598323
import socket
import ds_protocol
import json
import sys

def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    try:
      client.connect((server, port))
    except:
      print("Please enter a valid IP address. The system will now exit.")
      sys.exit()
    join_func = ds_protocol.join(username, password) # join function
    client.sendall(join_func.encode('utf-8')) #send username and password to server
    srv_msg = client.recv(4096).decode('utf-8')
    variables = ds_protocol.extract_json(srv_msg) #extracting token & message
    print(variables)#debug
    print(variables[1]) 
    srv_msg = json.loads(srv_msg) 
    try:
      token = variables[0]  
      post_message = ds_protocol.post(token, message) # post function
      client.sendall(post_message.encode('utf-8')) #sending message to server
      srv_msg2 = client.recv(4096).decode('utf-8')
      print(srv_msg2) #debug
      post_response = ds_protocol.extract_msg(srv_msg2)
      print(f"{post_response}:", message)
      bio_func = ds_protocol.bio(token, bio) # bio function
      client.sendall(bio_func.encode('utf-8')) #sending bio to server
    except KeyError:
      print("Please try again with the correct username or password.")

send('168.235.86.101', 3021, 'spiderman', 'pass123', 'Hello', 'this is a bio') #debug