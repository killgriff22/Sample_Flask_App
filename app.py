# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, redirect, url_for, render_template, request, make_response
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


@app.route('/')
def hello_world():
    cookie = request.cookies.get('token')
    with open("static/JS/Users.json", 'r') as UserDataBase:
        database = json.load(UserDataBase)
        tokenlst= database['tokens'].keys()
        tokens = database['tokens']
        UserDataBase.close()
    if cookie in tokenlst:
        name=tokens[cookie]
    else:
        name=""
    return render_template('hello.html',name=name)
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
    cookie = request.cookies.get('token')
    with open("static/JS/Users.json", 'r') as UserDataBase:
        database = json.load(UserDataBase)
        tokenlst= database['tokens'].keys()
        tokens = database['tokens']
        UserDataBase.close()
    if cookie in tokenlst:
        return render_template('welcome.html', user=tokens[cookie],name=tokens[cookie])
    return render_template('welcome.html', name="")
@app.route('/chat')
def imgchat():
    return render_template('imgchat.html')
# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    #
    app.run(debug=True, host='0.0.0.0', port=5000)
