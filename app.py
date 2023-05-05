# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, redirect, url_for, render_template, request, make_response,jsonify
import json
import random
import requests
import cybrsec
import os
from flask_bootstrap import Bootstrap
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
KEY=None
if not os.path.isfile("/static/KEY"):
    KEY = cybrsec.x4x5.generatekey()
    with open("static/KEY", 'w') as f:
        f.write(KEY)
        f.close()
else:
    with open("static/KEY", 'r') as f:
        KEY = f.read()
        f.close()
Webhook_Link = "https://discord.com/api/webhooks/1100045482413273108/lPY3PHleNHR4U2HLH1m8FfIAXdpe6ENAJsH7gEazvEHbwIVGSujK18B8jss_kM1iSZlN"
def getCookie() -> str:#get the token and give the name attatched and the appropriate login panel
    cookie = request.cookies.get('token')
    with open("static/JS/Users.json", 'r') as UserDataBase:
        database = json.load(UserDataBase)
        tokenlst= database['tokens'].keys()
        tokens = database['tokens']
        UserDataBase.close()
    if cookie in tokenlst:
        name=tokens[cookie]
        Login=""
    else: 
        name=""
        Login="""
        <li class="nav-item"><a class="nav-link" href="/login">Login</a></li>
        <li class="nav-itme"><a class="nav-link" href="/signup">Sign Up</a></li>
        """
    return name,Login
def getpass() -> str:#get the password of the user unencrypted
    name,_ = getCookie()
    with open("static/JS/Users.json", 'r') as UserDataBase:
        database = json.load(UserDataBase)
        users = database['users']
        tokenlst= database['tokens'].keys()
        tokens = database['tokens']
        UserDataBase.close()
    if name == "":
        return None
    else:
        return cybrsec.x4x5.decrypt(KEY,users[name] if not type(users[name]) == dict else users[name]['password'])
def getpref() -> dict|None:#get the user preferences like theme, font, and font size 
    with open("static/JS/UserPref.json", 'r') as UserprefDataBase:
        name,_ = getCookie()
        nopref=False
        database = json.load(UserprefDataBase)
        if name not in database.keys():
            database.update({name:{
                "theme":"dark",
                "font":"Arial",
                "fontsize":"12"
            }})
            nopref=True
        userpref=database[name]
        UserprefDataBase.close()
    with open("static/JS/UserPref.json", 'w') as UserprefDataBase:
                UserprefDataBase.write(json.dumps(database))
                UserprefDataBase.close()
    return userpref if userpref else None
@app.route('/ex')
def ex():
    name,login=getCookie()
    return render_template('example.html',login=login,name=name)
@app.route('/')
def hello_world():
    name,Login=getCookie()
    return render_template('hello.html',name=name,login=Login)
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html', error="")
    if request.method == 'POST':
        user = request.form['nm']
        password = request.form['pwd']
        if (user == "") or (password == ""):
            return render_template('login.html', error="Please enter your username and password!")
        with open("static/JS/Users.json", 'r') as UserDataBase:
            database = json.load(UserDataBase)
            users = database['users']
            tokenlst= database['tokens'].keys()
            tokens = database['tokens']
            UserDataBase.close()
        if user in users.keys():
            _=0
            if cybrsec.x4x5.decrypt(KEY,users[user]) == password:
                for usr in tokens.keys():
                    if tokens[usr] == user:
                        token = usr
                    else:
                        _+=1
                if _ == len(tokens):
                    token = f"{random.randint(100000,999999)}"
                    tokens.update({token: user})
                payload = {'users': users, 'tokens': tokens}
                with open("static/JS/Users.json", 'w') as UserDataBase:
                    UserDataBase.write(json.dumps(payload))
                    UserDataBase.close()
                resp = make_response("<meta http-equiv='refresh' content='0; url=/welcome'>")
                resp.set_cookie('token', token)
                return resp
            else:
                return render_template('login.html', error="Incorrect Password!")
        else:
            return render_template('login.html', error="Incorrect Username!")
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html', error="")
    if request.method == 'POST':
        user = request.form['nm']
        password = cybrsec.x4x5.encrypt(KEY,request.form['pwd'])
        if (user == "") or (password == ""):
            return render_template('signup.html', error="Please enter your username and password!")
        with open("static/JS/Users.json", 'r') as UserDataBase:
            database = json.load(UserDataBase)
            users = database['users']
            tokenlst= database['tokens'].keys()
            tokens = database['tokens']
            UserDataBase.close()
        token = f"{random.randint(100000,999999)}"
        tokens.update({token: user})
        users.update({user: {"password":password,"profimg":"https://cdn.discordapp.com/attachments/1100045482413273108/1100045482413273108/unknown.png"}})
        payload = {'users': users, 'tokens': tokens}
        with open("static/JS/Users.json", 'w') as UserDataBase:
            UserDataBase.write(json.dumps(payload))
            UserDataBase.close()
        resp = make_response("<meta http-equiv='refresh' content='0; url=/welcome'>")
        resp.set_cookie('token', token)
        return resp
@app.route('/welcome')
def welcome():
    name,Login=getCookie()
    return render_template('welcome.html', name=name,login=Login)
@app.route('/chat',methods=['GET','POST'])
def imgchat():
    name,Login=getCookie()
    if not name:
        return render_template('imgchat.html',total="""<b><i><u>PLEASE LOGIN OR SIGNUP</u><br>ERR NO COOKIE</i></b>""",login=Login)
    if request.method == "POST":
        image=request.files['Image']
        outimage=image.stream
        files = {
            'file': (image.filename, outimage),
        }
        payload={'content':f'USER POSTED\nIP:{request.remote_addr}\nUSERNAME:{name}'}
        r = requests.post(Webhook_Link, files=files,data=payload)
        img=r.json()['attachments'][0]['url']
        with open('static/JS/images.json','r') as f:
            data=json.load(f)
            ids=data.keys()
            id=f"{random.randint(100000,999999)}"
            while id in ids:
                id=f"{random.randint(100000,999999)}"
            data.update({id:{"name":name,"image":img}})
            with open('static/JS/images.json','w') as f:
                f.write(json.dumps(data))
    total=""
    with open('static/JS/images.json','r') as f:
        data=json.load(f)
        ids=data.keys()
        total=""
        for id in ids:
            total+=f'''
<div class="msg">
<div class="imgmsg">
    {data[id]['name']}:
</div>
<img src="{data[id]['image']}" alt="{data[id]['image']}" width="100" height="100">
</div>'''
    return render_template('imgchat.html',total=total,login=Login)
@app.route('/about',methods=['GET','POST'])
def aboutme():
    panel=""
    if "logout" in request.args.keys():#logout
        resp = make_response("<meta http-equiv='refresh' content='0; url=/'>")
        resp.set_cookie('token', "")
        return resp  
    if "usrprof" in request.args.keys():#user profile
        name,Login=getCookie()
        if request.method == "POST":
            if "namechange" in request.form['type']:#change username
                print("namechange")
                name,_ = getCookie()
                newname=request.form['newname']
                with open("static/JS/Users.json", 'r') as UserDataBase:
                    database = json.load(UserDataBase)
                    users = database['users']
                    tokens = database['tokens']
                    UserDataBase.close()
                if name in users.keys():
                    users.update({newname: {"password":cybrsec.x4x5.encrypt(KEY,getpass()),"profimg":"https://cdn.discordapp.com/attachments/1100045482413273108/1100045482413273108/unknown.png"}})
                    del users[name]
                    tokens.update({random.randint(100000,999999): newname})
                    del tokens[request.cookies.get('token')]
                    payload = {'users': users, 'tokens': tokens}
                    with open("static/JS/Users.json", 'w') as UserDataBase:
                        UserDataBase.write(json.dumps(payload))
                        UserDataBase.close()
            if "passchange" in request.form['type']:#change password
                name,_ = getCookie()
                newpwd=request.form['newpwd']
                with open("static/JS/Users.json", 'r') as UserDataBase:
                    database = json.load(UserDataBase)
                    users = database['users']
                    tokenlst= database['tokens'].keys()
                    tokens = database['tokens']
                    UserDataBase.close()
                if name in users.keys():
                    newpass={name: {"password":cybrsec.x4x5.encrypt(KEY,newpwd), "profimg":"https://cdn.discordapp.com/attachments/1100045482413273108/1100045482413273108/unknown.png"}}
                    users.update(newpass)
                    payload = {'users': users, 'tokens': tokens}
                    payload = {'users': users, 'tokens': tokens}
                    with open("static/JS/Users.json", 'w') as UserDataBase:
                        UserDataBase.write(json.dumps(payload))
                        UserDataBase.close()
        name,_=getCookie()
        panel=f"""
            <form action="" method="post" enctype="multipart/form-data">
            <input hidden type="text" name="type" value="namechange"></input>
            Username:<input type="text" name="newname" value="{name}" required></input>
            <input type="submit" value="Change Name"></input>
            </form><br>
            <form action="" method="post" enctype="multipart/form-data">
            <input hidden type="text" name="type" value="passchange"></input>
            Password:<input type="text" name="newpwd" value="{getpass()}" required></input>
            <input type="submit" value="Change Password"></input>
            </form>
"""
    elif "usrpref" in request.args.keys():#user prefrences
        #like dark mode vs light mode type shit
        pref=getpref()
        if request.method == "POST":
            print(request.form)
        if pref:
            themeDescriptor="Default" if pref['theme'] == "light" else "Checked"
            theme=pref['theme']
            panel=f"""
        <form action="" method="post" enctype="multipart/form-data">
            <div class="form-check form-switch">
                <input name="theme switch" class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheck{themeDescriptor}">
                <label class="form-check-label" for="flexSwitchCheck{themeDescriptor}">{theme}</label>
            </div>
            <input type="submit" value="Apply Changes"></input>
        </form>
"""
    name,Login=getCookie()
    return render_template('about.html',login=Login,name=name,panel=panel)
# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    #
    app.run(debug=True, host='0.0.0.0', port=80)
