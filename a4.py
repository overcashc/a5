# Michael Yeung
# myeung2@uci.edu
# 71598323

from pathlib import Path
from Profile import Profile
from Profile import Post
from OpenWeather import OpenWeather
from LastFM import LastFM
from NaClProfile import NaClProfile
import ds_client

port = 3021
#server = "168.235.86.101" 
store_info = NaClProfile()
dir_and_name = ''
C_ran = False
O_ran = False
O_file = ''
uploading = False
file_exists_errorhandling = False
admin = False
'''
a4 variables for web api
'''
zipcode = "92617"
ccode = "US"
apikey = "de81f1cd5761b067f3b3625d8d635530"
apikey_fm = '33f7f26663017ea24945be21492594b2'
open_weather = OpenWeather(zipcode, ccode)
last_fm = LastFM()


'''
File explorer
'''
def L(path):    #print out files in dir
    for file in path.iterdir():
        if file.is_file():
            print(file)
    for file in path.iterdir():
        if file.is_dir():
            print(file)
          
def r(path, keep_directory=True):  #print out everything in dir
    for file in path.iterdir():
        if file.is_file():
            print(file)
    for file in path.iterdir():
        if file.is_dir():
            if keep_directory:
                print(file)
            r(file)

def f(path): #print out only files
    for file in path.iterdir():
        if file.is_file():
            print(file)

e_list = []
def e(path): #print out specific file type only
    file_type = user_input[-1][2:]
    for f in path.iterdir():
        if f.is_file():
            new_f = f.suffix
            if new_f[1:] == file_type:
                e_list.append(f)
    for file in path.iterdir():
        if file.is_dir():
            e(file)

def s(path): #print out files that have specific file_name without recursive
    file_name = user_input[0][2:] # s file_name
    for f in path.iterdir():
        if f.is_file() and f.name == file_name:
            print(f)

def rs(path): #print out files that have specific file name recursively
    file_name = user_input[1][2:] # s file_name
    for f in path.iterdir():
        if f.is_file() and f.name == file_name:
            print(f)
    for d in path.iterdir():
        if d.is_dir():
            rs(d)
    return
'''
ICS 32 Journal
'''
def tutorial():
    print("\nYou may now edit your info with the E command or view your info with the P command")
    print("\n***Follow this structure for E command: E [input command] \"your entry\"")
    print("***Follow this structure for the P command: P [input command] ")
    print("***To upload a post online, begin with creating your first post using E -addpost \"your entry\"")
    print("Keywords available for adding a post are @weather (weather description) and @lastfm (top artist)")
    print("\nAll input commands available for Editing are -usr -pwd -bio -addpost -delpost [ID]")
    print("All input commands available for Printing are -usr -pwd -bio -posts -post [ID] -all")
    print("\nDeleting a post follows a different structure: E -delpost [ID] (For example: E -delpost 1 will delete the 1st post)")
    print("Printing a specific post follows a different structure: P -post [ID] (For example P - post 1 will print the 1st post)")

def C(p):  #C create a new file  name.dsu
    global store_info
    global dir_and_name
    global C_ran
    global O_file
    global file_exists_errorhandling
    C_ran = True
    O_file = dir_and_name

    dir_C = (read_file[2:])
    name = user_input[-1][2:] + ".dsu"
    dir_and_name = dir_C + "\\" + name
    O_file = '  ' + dir_and_name 
    if Path(dir_and_name).is_file():  #Error handling for when a file already exists
        print("File already exists")
        file_exists_errorhandling = True
        return False
    new_file = open(dir_and_name, "w")
    new_file.write("")
    new_file.close()
    print(dir_and_name)
    store_info = NaClProfile(dsuserver=None, username=None, password=None) #to clear the previous profile
    store_info.bio = ''
    
    if admin == False: #asking for inputs for new file
        username_input = input("Please enter your username: ")
        password_input = input("Please enter your password: ")
        bio_input = input("Please enter a bio: ")
        
        store_info = NaClProfile('', username_input, password_input)
        store_info.bio = bio_input
    return True
    
def R(p): #Read contents of .dsu file only & print empty if contents are empty, and if not .dsu file print ERROR
    x = read_file.split('\\')
    if x[-1][-4:] == '.dsu':
        R_file = open(p, 'r')
        contents = R_file.read().splitlines()
        R_file.close()
        if contents == '':
            print("EMPTY")
        else:
            print(' '.join(contents))
    else: 
        print("The file you are trying to read is not a dsu file")
    
def D(p): #Only delete .dsu files, prints confirmation, if not dsu file print ERROR
    Opened_File = '' + O_file
    if read_file[2:] == Opened_File[2:]: #Prevents deleting an open file
        print("The file must be closed to delete")
        return
    if p.suffix == '.dsu':
        p.unlink()
        print(p, end="")
        print(" DELETED")
    else: 
        print("The file you are trying to delete must be a dsu file")

def O(p): #Open .dsu file 
    global O_file
    global O_ran
    global uploading
    if not p.is_file():
        print("The file you entered does not exist") 
        return
    with open(read_file[2:]) as f: #checking if the file follows profile format
        line = f.readlines()
        if '\"dsuserver\"'not in line[0]: 
            print("The dsu file is not following Profile format")
            return False
    O_ran = True
    O_file = read_file
    store_info.load_profile(p)
    upload_entry = input("Would you like to publish an existing post from this journal to the ICS 32 Distributed Social? Please Enter: yes or no\n")
    if upload_entry == 'yes':
        uploading = True
        posts = store_info.get_posts()
        number = 1
        for dict in posts:
            print(f"{number}.  ",end = '')
            print(dict['entry'])
            number += 1
        entry = input("Please enter the number of the entry you would like to upload, for example [1]\n")
        index = int(entry) - 1
        posts = store_info.get_posts()
        dict_2 = posts[index]
        get_ip = input("What is the ip address of the server you'd like to publish to? (Class server 168.235.86.101)\n")
        store_info.dsuserver = get_ip
        ds_client.send(store_info.dsuserver, port, store_info.username, store_info.password, dict_2['entry'], store_info.bio)
    return True
    
def E(): #Edit info in dsu file
    for x in user_input:
        if 'usr' in x:
            split_user = x.split("\"")
            username = split_user[1]
            store_info.username = username
        if 'pwd' in x:
            split_user = x.split("\"")
            password = split_user[1]
            store_info.password = password
        if 'bio' in x:
            split_user = x.split("\"")
            bio = split_user[1]
            store_info.bio = bio
        if "addpost" in x:
            split_user = x.split("\"")
            entry = split_user[1]
            if '@weather' and 'lastfm' in entry:
                transcluded_entry_1 = test_api(entry, apikey, open_weather)
                transcluded_entry = test_api(transcluded_entry_1, apikey_fm, last_fm)
            else:
                if '@weather' in entry:
                    transcluded_entry = test_api(entry, apikey, open_weather)
                else:
                    transcluded_entry = test_api(entry, apikey_fm, last_fm)
            post = Post(transcluded_entry)
            #store_info.add_post(post)
            upload_entry = input("Would you like to publish this entry to the ICS 32 Distributed Social? Please Enter: yes or no\n")  
            if upload_entry == 'yes':
                get_ip = input("What is the ip address of the server you'd like to publish to? (Class server 168.235.86.101) \n")
                store_info.dsuserver = get_ip
                msg, bio = ds_client.send(store_info.dsuserver, port, store_info.username, store_info.password, transcluded_entry, store_info.bio)
                store_info._posts.append(Post(msg))
                store_info.bio = bio
        if "delpost" in x:
            index = int(x[-1]) - 1
            store_info.del_post(index)

def P(): #Printing info in dsu file
    for x in user_input:
        if 'usr' in x:
            print("Username: " + store_info.username)
        if 'pwd' in x:
            print("Password: " + store_info.password)
        if 'bio' in x:
            print("Bio: " + store_info.bio)
        if "posts" in x:
            posts = store_info.get_posts()
            number = 1
            for dict in posts:
                print(f"{number}.  ",end = '')
                print(dict['entry'])
                number += 1
        elif "post" in x:
            try:
                index = int(x[-1]) - 1
                posts = store_info.get_posts()
                dict_2 = posts[index]
                print(dict_2['entry'])
            except:
                print("Please check your formating or the post may not exist")
        if "all" in x:
            print("Username: " + store_info.username)
            print("Password: " + store_info.password)
            print("Bio: " + store_info.bio)
            print("Posts: ")
            posts = store_info.get_posts()
            number = 1
            for dict in posts:
                print(f"{number}.  ",end = '')
                print(dict['entry'])
                number  += 1

def test_api(message:str, apikey:str, webapi): #returns the transcluded msg for E -addpost and uploading to journal
    webapi.set_apikey(apikey)
    webapi.load_data()
    result = webapi.transclude(message)
    return result

def _openweather_test():
    open_weather.set_apikey(apikey)
    open_weather.load_data()
    print(f"The temperature for {zipcode} is {open_weather.temperature} degrees")
    print(f"The high for today in {zipcode} will be {open_weather.high_temperature} degrees")
    print(f"The low for today in {zipcode} will be {open_weather.low_temperature} degrees")
    print(f"The coordinates for {zipcode} are {open_weather.longitude} longitude and {open_weather.latitude} latitude")
    print(f"The current weather for {zipcode} is {open_weather.description}")
    print(f"The current humidity for {zipcode} is {open_weather.humidity}")
    print(f"The sun will set in {open_weather.city} at {open_weather.sunset}")
'''
main
'''
def run(): 
    while True:
        global read_file
        global user_input
        global admin
        
        user_input = input().split(' -') # L C://
        if user_input[0] == 'admin':
            admin = True
            continue
        command = user_input[0][0:1]
        p = Path(user_input[0][2:])
        read_file = user_input[0]
        user_input.pop(0)
        if command == 'Q':
            return False
        # user_input = [-r]
        if command == 'L':
            if len(user_input) == 0:
                L(p)
            elif len(user_input) == 1:
                if user_input[0] == 'r':
                    r(p)
                if user_input[0] == 'f':
                    f(p)
                if user_input[0][0] == 's':
                    s(p)
            elif len(user_input) == 2:
                if user_input [0] == 'r' and user_input[1] == 'f':
                    r(p, False)
                if user_input [0] == 'r' and user_input[-1][0] == 's':
                    rs(p)
                if user_input [0] == 'r' and user_input[-1][0] == 'e':
                    e(p)
                    for file_e in e_list:
                        print(file_e)
        if command == 'C' and user_input[0][0] == 'n':
            worked = C(p)
            if not admin and worked:
                tutorial()
        if command == 'R':
            R(p)
        if command == 'D':
            D(p)
        if command == 'O':
            worked = O(p)
            if not admin and p.is_file() and worked and not uploading:
                tutorial()
        if command == 'E': # Edit info in dsu file
            E()
        if command == 'P': # Print info in dsu file
            P()
        if command == 'T': #testing open weather api
            _openweather_test()
        if command == '': # Error handling
            print("You entered nothing")

        if C_ran == True:  #saving profile info
            store_info.save_profile(dir_and_name)
        if O_ran == True:
            store_info.save_profile(O_file[2:])

if __name__ == '__main__':
    print("Welcome to ICS 32 Journal! At any time Enter Q to quit the program. \n\nPlease choose to either Open or Create a dsu file")
    print("\nTo create enter: C /path/to/your/file -n YOUR_FILE_NAME")
    print("To open enter O /path/to/your/file/YOUR_FILE_NAME.dsu")
    print("To upload an existing journal, begin with opening a journal and following the prompt")
    run()
    print("Thank you for using the program. Have a great day!")