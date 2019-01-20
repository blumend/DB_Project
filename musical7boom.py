from create_questions import create
from flask import Flask, render_template, request, escape, url_for, logging, redirect, make_response, session, flash
import random
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from datetime import datetime

# Config app
app = Flask(__name__)
app.config['SECRET_KEY'] = "123"
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# Config MySQL
try:
    with open ("DB_config.txt", 'r') as db_config: 
        app.config['MYSQL_HOST'] = db_config.readline().split('=')[1].strip()
        app.config['MYSQL_USER'] = db_config.readline().split('=')[1].strip()
        app.config['MYSQL_PASSWORD'] = db_config.readline().split('=')[1].strip()
        app.config['MYSQL_DB'] = db_config.readline().split('=')[1].strip()

    mysql = MySQL(app)
except:
    render_template("error.html")

countUsersFlag = 0

        

@app.route('/', methods=['GET', 'POST'])
def index():
    global countUsersFlag
    countUsersFlag = 0
    session['rank'] = 1
    session['score'] = 0
    session['counter']  = 0
    session['lives'] = 5
    if('type' in request.form and request.form['type'] == "1 Player"):
        session['players'] = 1
        return redirect(url_for('login'))
    elif('type' in request.form and request.form['type'] == "2 Players"):
        countUsersFlag += 1
        session['players'] = 2
        session['score2'] = 0
        session['lives2'] = 5
        return redirect(url_for('login'))
    elif(countUsersFlag >= 1):
        return index()
    else:
        return render_template('entry.html')


@app.route('/startgame', methods = ['Get', 'POST'])
def startgame():
    if((session['players'] == 1 and countUsersFlag == 1) or (session['players'] == 2 and countUsersFlag > 2)):
        return render_template("startgame.html", title = "Click to Start!")
    else:
        return redirect(url_for('login'))


class Registraion(Form):
    username = StringField('Username:', [validators.length(min=1, max=10)])
    password = PasswordField('Password:', [validators.length(min=4, max=30)])


@app.route('/register', methods=['GET', 'POST'])
def register():
    error=""
    form = Registraion(request.form)
    cur = mysql.connection.cursor()
    if request.method == 'POST' and form.validate():
        userName = form.username.data
        query = cur.execute("SELECT * FROM users WHERE user_name = %s", [userName])
        if query == 0:
            password = sha256_crypt.hash((form.password.data))
            cur.execute("INSERT INTO users(user_name, user_pass) VALUES(%s, %s)",
            (userName, password))
            mysql.connection.commit()
            cur.close()
            flash("Registration Completed!", 'success')
            return redirect(url_for('login'))
        else:
            error = "Username already taken, Please try again"
            cur.close()
    return render_template('register.html', form = form, error = error)


@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        userName = request.form['username']
        unvalidated_password = request.form['password']
        cur = mysql.connection.cursor()
        query = cur.execute("SELECT * FROM users WHERE user_name = %s", [userName])
        if query > 0:
            password = cur.fetchone()[2]
            if sha256_crypt.verify(unvalidated_password, password):
                global countUsersFlag
                if countUsersFlag != 2:
                    session['username'] = userName
                    if countUsersFlag == 0:
                        return render_template("startgame.html", name=userName, title="Click to Start!")
                    else:
                        countUsersFlag += 1
                        return redirect(url_for('login'))
                else:
                    if(userName == session['username']):
                        return render_template('login.html', title="Second Player ", error = "This user is already signed in")
                    session['username2'] = userName
                    #return render_template('quiz.html')
                    countUsersFlag += 1
                    return render_template("startgame.html", name=session['username'], name2=userName, title="Click to Start!")  
            else:
                login_err = 'Wrong Password'
                return render_template('login.html', error = login_err)
        else:
            login_err = 'Username not found'
            return render_template('login.html', error = login_err)
    if(countUsersFlag > 1):
        return render_template('login.html', title="Second Player ")    
    return render_template('login.html')


@app.route('/quiz', methods =['GET','POST'])
def quiz():
    session['counter'] += 1
    question, answers, real_answer = create(session, mysql)
    session['question'] = question
    session['answers'] = answers
    session['real_answer'] = real_answer
    random.shuffle(session['answers'])
    print("real_answer is: ", session['real_answer'])
    if(session['players'] == 1):
        return render_template('quiz.html',
            the_question = session['question'],
            the_title = "Question " + str(session['counter']), score1 = session['username'] + ': ' + 
            str(session['score']), lives = session['lives'],
            a = session['answers'][0],
            b = session['answers'][1],
            c = session['answers'][2],
            d = session['answers'][3])
    else:
        return render_template('quiz.html',
            the_question = session['question'],
            the_title = "Question " + str(session['counter']), score1 = session['username'] + ': ' +
            str(session['score']), lives = session['lives'], score2 = session['username2'] + ': ' +
            str(session['score2']), lives2 = session['lives2'],
            a = session['answers'][0],
            b = session['answers'][1],
            c = session['answers'][2],
            d = session['answers'][3])

    
@app.route('/quiz', methods =['GET','POST'])
def get_score():
    user_answer = None
    if request.method == 'POST':
        for k,v in request.form.items():
            user_answer = v
        if  user_answer != None and user_answer[3:] == session['real_answer']:
            if session['counter'] % 7 == 0:
                if session['players'] == 2 and session['counter'] % 2 == 0:
                        session['score2'] += 7
                else:
                    session['score'] += 7
            else:
                if session['players'] == 2 and session['counter'] % 2 == 0:
                        session['score2'] += 1
                else:
                    session['score'] += 1
            session['is_correct'] = "Correct"
        else:
            if session['players'] == 2 and session['counter'] % 2 == 0:
                    session['lives2'] -= 1
            else:
                session['lives'] -= 1
            session['is_correct'] = "Wrong"


@app.route('/highscores')
def showHighscores():
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_name, highscore FROM users ORDER BY highscore DESC LIMIT 10;")
    scores = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template("highscores.html", highscores = scores) 


@app.route('/answer', methods =['GET','POST'])
def answer():
    get_score()
    if ((session['players'] == 1) and (session['lives'] <= 0)):
        updateHighscores()
        return render_template('gameover.html', score1 = session['username'] + ': ' + str(session['score']))
    elif ((session['players'] == 2) and (session['lives'] <= 0 or session['lives2'] <= 0)):
        updateHighscores()
        return render_template('gameover.html', score1 = session['username'] + ': ' + str(session['score']), score2 = session['username2'] + ': ' + str(session['score2']))
    total = session['counter']
    return render_template('answer.html',total =  total)

def updateHighscores():
    cur = mysql.connection.cursor()
    query = "SELECT highscore FROM users WHERE user_name = '" + session['username'] + "';"
    cur.execute(query)
    score = cur.fetchone()[0]
    if session['score'] > score:
        query = "UPDATE users SET highscore = " + str(session['score']) + " WHERE user_name = '" + session['username'] + "';"
        cur.execute(query)
    if(countUsersFlag > 1):
        query = "SELECT highscore FROM users WHERE user_name = '" + session['username2'] + "';"
        cur.execute(query)
        score = cur.fetchone()[0]
        if session['score2'] > score:
            query = "UPDATE users SET highscore = " + str(session['score2']) + " WHERE user_name = '" + session['username2'] + "';"
            cur.execute(query)
    mysql.connection.commit()
    cur.close()


@app.route('/instructions')
def instructions():
    return render_template("instructions.html")

app.run(debug = True, port = 5200, host = '0.0.0.0')