# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, redirect, url_for, render_template, request, make_response,jsonify
import json
import random
import requests
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
Webhook_Link = "https://discord.com/api/webhooks/1100045482413273108/lPY3PHleNHR4U2HLH1m8FfIAXdpe6ENAJsH7gEazvEHbwIVGSujK18B8jss_kM1iSZlN"
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
def getCookie():
    cookie = request.cookies.get('token')
    with open("static/JS/Users.json", 'r') as UserDataBase:
        database = json.load(UserDataBase)
        tokenlst= database['tokens'].keys()
        tokens = database['tokens']
        UserDataBase.close()
    if cookie in tokenlst:
        name=tokens[cookie]
        Login=f"""
        <li><a href="about">{name}</a></li>
        """
    else: 
        name=""
        Login="""
        <li><a href="/login">Login</a></li>
        <li><a href="/signup">Sign Up</a></li>
        """
    return name,Login

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
            if users[user] == password:
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
        password = request.form['pwd']
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
        users.update({user: password})
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
    return render_template('welcome.html', name="",login=Login)
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
    if "logout" in request.args.keys():#logout
        resp = make_response("<meta http-equiv='refresh' content='0; url=/'>")
        resp.set_cookie('token', "")
        return resp
    if "usrprof" in request.args.keys():#user profile
        name,Login=getCookie()
        return render_template('about.html',login=Login,panel="""hi""")
    name,Login=getCookie()
    return render_template('about.html',login=Login)
# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    #
    app.run(debug=True, host='0.0.0.0', port=5000)
