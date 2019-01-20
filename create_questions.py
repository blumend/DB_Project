import random

familiarity = 0.999
familiarity2 = 0.930
session = {}
mysql = None

def create(session_, mysql_):
    global session, mysql
    session = session_
    mysql = mysql_
    if(session['counter'] % 7) == 0:
        typeOfQ = random.randint(1, 4)
        try:
            if(typeOfQ == 1):
                sevenBoom1()
            elif(typeOfQ == 2): 
                sevenBoom2()
            elif(typeOfQ == 3): 
                sevenBoom3()
            elif(typeOfQ == 4): 
                sevenBoom4()
            session['rank'] += 1
            changeFamiliraity()
        except:
            create(session, mysql)
    else:
        typeOfQ = random.randint(1, 8)
        try:
            if(typeOfQ == 1):
                q1()
            elif(typeOfQ == 2): 
                q2()
            elif(typeOfQ == 3): 
                q3()
            elif(typeOfQ == 4): 
                q4()
            elif(typeOfQ == 5): 
                q5()
            elif(typeOfQ == 6): 
                q6()
            elif(typeOfQ == 7): 
                q7()
            elif(typeOfQ == 8): 
                q8()
            elif(typeOfQ == 9): 
                q9()
            else: 
                q10()
        except:
            changeFamiliraity(True)
            create(session, mysql)
        
    return [session['question'], session['answers'], session['real_answer']]

def changeFamiliraity(increase = False):
    global familiarity, familiarity2
    if(increase == False):
        familiarity = 1 / ((1 / familiarity) * 1.05)
        familiarity2 = familiarity - 0.099
    else:
        familiarity += 0.01
        familiarity2 -= 0.01

def q1():
    global session, mysql
    cur = mysql.connection.cursor()
    query = "SELECT artists.artist_id, artists.artist_name, artist_location.location FROM artists INNER JOIN artist_location ON artists.artist_id = artist_location.artist_id WHERE artist_familiarity BETWEEN " + str(familiarity2) + " AND " + str(familiarity) + " ORDER BY RAND() LIMIT 1;"
    cur.execute(query)
    row = cur.fetchall()
    session['question'] = "Where does " + str(row[0][1]) + " come from?"
    session['real_answer'] = str(row[0][2])
    answers = []
    answers.append(session['real_answer'])
    query = "SELECT DISTINCT location FROM artist_location WHERE location != '" + str(row[0][2]) + "' ORDER BY RAND() LIMIT 3;"
    cur.execute(query)
    row = cur.fetchall()
    for i in range(3):
        answers.append(str(row[i][0]))
    session['answers'] = answers
    mysql.connection.commit()
    cur.close()

def q2():
    global session, mysql
    cur = mysql.connection.cursor()
    query = "SELECT artists.artist_id, artists.artist_name, songs.song_name, songs.year FROM artists INNER JOIN songs ON artists.artist_id = songs.artist_id WHERE artist_familiarity BETWEEN " + str(familiarity2) + " AND " + str(familiarity) + " ORDER BY RAND() LIMIT 1;"
    cur.execute(query)
    row = cur.fetchall()
    session['question'] = "In which year was the song '" + str(row[0][2]) + "' by " + str(row[0][1]) + " published?"
    session['real_answer'] = str(row[0][3])
    answers = []
    answers.append(session['real_answer'])
    query = "SELECT DISTINCT year FROM songs WHERE year != " + str(row[0][3]) + " ORDER BY RAND() LIMIT 3;"
    cur.execute(query)
    row = cur.fetchall()
    for i in range(3):
        answers.append(str(row[i][0]))
    session['answers'] = answers
    mysql.connection.commit()
    cur.close()

def q3():
    global session, mysql
    cur = mysql.connection.cursor()
    query = "SELECT artists.artist_id, artists.artist_name, songs.song_name, songs.album_name FROM artists INNER JOIN songs ON artists.artist_id = songs.artist_id WHERE artist_familiarity BETWEEN " + str(familiarity2) + " AND " + str(familiarity) + " ORDER BY RAND() LIMIT 1;"
    cur.execute(query)
    row = cur.fetchall()
    session['question'] = "What is the name of the album which '" + str(row[0][2]) + "' by " + str(row[0][1]) + ", belongs to?"
    session['real_answer'] = str(row[0][3])
    answers = []
    answers.append(session['real_answer'])
    query = "SELECT DISTINCT album_name FROM songs WHERE album_name != '" + session['real_answer'] + "' ORDER BY RAND() LIMIT 3;"
    cur.execute(query)
    row = cur.fetchall()
    for i in range(3):
        answers.append(str(row[i][0]))
    session['answers'] = answers
    mysql.connection.commit()
    cur.close()

def q4():
    global session, mysql
    cur = mysql.connection.cursor()
    query = "SELECT DISTINCT artist_name, song_name, album_name FROM (SELECT * FROM artists WHERE artist_familiarity BETWEEN " + str(familiarity2) + " AND " + str(familiarity) + ") AS one INNER JOIN songs ON one.artist_id = songs.artist_id ORDER BY RAND() LIMIT 1;"
    cur.execute(query)
    row = cur.fetchall()
    session['question'] = "To whom does the song '" + str(row[0][1]) + "' from the album '" + str(row[0][2]) + "' belong?"
    session['real_answer'] = str(row[0][0])
    answers = []
    answers.append(session['real_answer'])
    query = "SELECT DISTINCT artist_name FROM artists WHERE artist_name != '" + session['real_answer'] + "' ORDER BY RAND() LIMIT 3;"
    cur.execute(query)
    row = cur.fetchall()
    for i in range(3):
        answers.append(str(row[i][0]))
    session['answers'] = answers
    mysql.connection.commit()
    cur.close()


def q5():
    global session, mysql
    cur = mysql.connection.cursor()
    query = "SELECT artist_name, song_name, year FROM (SELECT * FROM artists WHERE artist_familiarity BETWEEN " + str(familiarity2) + " AND " + str(familiarity) + ") AS one INNER JOIN songs ON one.artist_id = songs.artist_id ORDER BY RAND() LIMIT 1;"
    cur.execute(query)
    row = cur.fetchall()
    session['question'] = "Which song published by " + str(row[0][0]) + " in the year " + str(row[0][2]) + "?"
    session['real_answer'] = str(row[0][1])
    answers = []
    answers.append(session['real_answer'])
    query = "SELECT DISTINCT song_name FROM songs WHERE song_name != '" + str(row[0][1]) + "' ORDER BY RAND() LIMIT 3;"
    cur.execute(query)
    row = cur.fetchall()
    for i in range(3):
        answers.append(str(row[i][0]))
    session['answers'] = answers
    mysql.connection.commit()
    cur.close()

def q6():
    global session, mysql
    cur = mysql.connection.cursor()
    query = "SELECT artist_name, album_name, year FROM (SELECT artist_id, artist_name FROM artists WHERE artist_familiarity BETWEEN " + str(familiarity2) + " AND " + str(familiarity) + ") AS one INNER JOIN songs ON one.artist_id = songs.artist_id ORDER BY RAND() LIMIT 1;"
    cur.execute(query)
    row = cur.fetchall()
    session['question'] = "When did " + str(row[0][0]) + " published the album '" + str(row[0][1]) + "'?"
    session['real_answer'] = str(row[0][2])
    answers = []
    answers.append(session['real_answer'])
    query = "SELECT DISTINCT year FROM songs WHERE year != " + str(row[0][2]) + " ORDER BY RAND() LIMIT 3;"
    cur.execute(query)
    row = cur.fetchall()
    for i in range(3):
        answers.append(str(row[i][0]))
    session['answers'] = answers
    mysql.connection.commit()
    cur.close()

def q7():
    global session, mysql
    cur = mysql.connection.cursor()
    query = "SELECT artist_name, location FROM artist_location WHERE location IN (SELECT counter.location FROM (SELECT COUNT(artist_location.artist_id) AS num, location FROM artist_location INNER JOIN artists ON artists.artist_id = artist_location.artist_id WHERE artist_familiarity BETWEEN " + str(familiarity2) + " AND " + str(familiarity) + " GROUP BY location) AS counter WHERE counter.num > 1) ORDER BY RAND() LIMIT 2;"
    cur.execute(query)
    row = cur.fetchall()
    session['question'] = "Which artist comes from the same place as " + str(row[0][0]) + "?"
    session['real_answer'] = str(row[1][0])
    answers = []
    answers.append(session['real_answer'])
    query = "SELECT DISTINCT artist_name FROM artist_location WHERE location != '" + str(row[0][1]) + "' ORDER BY RAND() LIMIT 3;"
    cur.execute(query)
    row = cur.fetchall()
    for i in range(3):
        answers.append(str(row[i][0]))
    session['answers'] = answers
    mysql.connection.commit()
    cur.close()


def q8():
    global session, mysql
    cur = mysql.connection.cursor()
    query = "SELECT song_name, year FROM songs WHERE year IN (SELECT counter.year FROM (SELECT COUNT(songs.song_id) AS num, songs.year FROM artists INNER JOIN songs ON artists.artist_id = songs.artist_id WHERE artist_familiarity BETWEEN " + str(familiarity2) + " AND " + str(familiarity) + " GROUP BY year) AS counter WHERE counter.num > 1) ORDER BY RAND() LIMIT 2;"
    cur.execute(query)
    row = cur.fetchall()
    session['question'] = "Which two songs were published in the year " + str(row[0][1]) + "?"
    session['real_answer'] = str(row[0][0]) + ", " + str(row[1][0])
    answers = []
    answers.append(session['real_answer'])
    query = "SELECT DISTINCT song_name FROM songs WHERE year != " + str(row[0][1]) + " ORDER BY RAND() LIMIT 6;"
    cur.execute(query)
    row = cur.fetchall()
    for i in range(0, 6, 2):
        answers.append(str(row[i][0]) + ", " + str(row[i + 1][0]))
    session['answers'] = answers
    mysql.connection.commit()
    cur.close()


def q9():
    global session, mysql
    cur = mysql.connection.cursor()
    query = "SELECT artist_name FROM artists INNER JOIN songs ON artists.artist_id = songs.artist_id WHERE album_name = song_name AND artist_familiarity BETWEEN " + str(familiarity2) + " AND " + str(familiarity) + " ORDER BY RAND() LIMIT 1;"
    cur.execute(query)
    row = cur.fetchall()
    session['question'] = "Which artist has a song that has the same title as its album?"
    session['real_answer'] = str(row[0][0])
    answers = []
    answers.append(session['real_answer'])
    query = "SELECT DISTINCT artist_name FROM artists INNER JOIN songs ON artists.artist_id = songs.artist_id WHERE album_name != song_name ORDER BY RAND() LIMIT 3;"
    cur.execute(query)
    row = cur.fetchall()
    for i in range(3):
        answers.append(str(row[i][0]))
    session['answers'] = answers
    mysql.connection.commit()
    cur.close()

def q10():
    global session, mysql
    cur = mysql.connection.cursor()
    query = "SELECT artists.artist_name, artist_location.location FROM artists INNER JOIN artist_location ON artists.artist_id = artist_location.artist_id WHERE artist_familiarity BETWEEN " + str(familiarity2) + " AND " + str(familiarity) + " ORDER BY RAND() LIMIT 1;"
    cur.execute(query)
    row = cur.fetchall()
    session['question'] = "Which artist comes from '" + str(row[0][1]) + "'?"
    session['real_answer'] = str(row[0][0])
    answers = []
    answers.append(session['real_answer'])
    query = "SELECT DISTINCT artist_name FROM artist_location WHERE location != '" + str(row[0][1]) + "' ORDER BY RAND() LIMIT 3;"
    cur.execute(query)
    row = cur.fetchall()
    for i in range(3):
        answers.append(str(row[i][0]))
    session['answers'] = answers
    mysql.connection.commit()
    cur.close()


def sevenBoom1():
    global session, mysql
    cur = mysql.connection.cursor()
    query = "SELECT artist_name FROM artist_location WHERE location IN (SELECT len.location FROM (SELECT location, LENGTH(location) AS lenOfLoc FROM artist_location) AS len WHERE len.lenOfLoc = 7) ORDER BY RAND() LIMIT 1;"
    cur.execute(query)
    row = cur.fetchall()
    session['question'] = "Which artist comes from a place that its name's length is 7?"
    session['real_answer'] = str(row[0][0])
    answers = []
    answers.append(session['real_answer'])
    query = "SELECT DISTINCT artist_name FROM artist_location WHERE location NOT IN (SELECT len.location FROM (SELECT location, LENGTH(location) AS lenOfLoc FROM artist_location) AS len WHERE len.lenOfLoc != 7) ORDER BY RAND() LIMIT 3;"
    cur.execute(query)
    row = cur.fetchall()
    for i in range(3):
        answers.append(str(row[i][0]))
    session['answers'] = answers
    mysql.connection.commit()
    cur.close()

def sevenBoom2():
    global session, mysql
    cur = mysql.connection.cursor()
    query = "SELECT song_name FROM songs WHERE duration BETWEEN 400 AND 440  ORDER BY RAND() LIMIT 1;"
    cur.execute(query)
    row = cur.fetchall()
    session['question'] = "Which song is playing for about seven minutes?"
    session['real_answer'] = str(row[0][0])
    answers = []
    answers.append(session['real_answer'])
    query = "SELECT DISTINCT song_name FROM songs WHERE duration < 350 OR duration > 480 ORDER BY RAND() LIMIT 3;"
    cur.execute(query)
    row = cur.fetchall()
    for i in range(3):
        answers.append(str(row[i][0]))
    session['answers'] = answers
    mysql.connection.commit()
    cur.close()


def sevenBoom3():
    global session, mysql
    cur = mysql.connection.cursor()
    query = "SELECT song_name FROM songs WHERE year LIKE '%7%' ORDER BY RAND() LIMIT 1;"
    cur.execute(query)
    row = cur.fetchall()
    session['question'] = "Which song was published in the year containing the number seven?"
    session['real_answer'] = str(row[0][0])
    answers = []
    answers.append(session['real_answer'])
    query = "SELECT DISTINCT song_name FROM songs WHERE year NOT LIKE '%7%' ORDER BY RAND() LIMIT 3;"
    cur.execute(query)
    row = cur.fetchall()
    for i in range(3):
        answers.append(str(row[i][0]))
    session['answers'] = answers
    mysql.connection.commit()
    cur.close()


def sevenBoom4():
    global session, mysql
    cur = mysql.connection.cursor()
    query = "SELECT artist_name FROM artists INNER JOIN (SELECT DISTINCT artist_id FROM songs WHERE song_name LIKE '%seven%' OR album_name LIKE '%seven%') AS seven ON artists.artist_id = seven.artist_id  ORDER BY RAND() LIMIT 1;"
    cur.execute(query)
    row = cur.fetchall()
    session['question'] = "Which artist has a Song or Album containing the word 'seven'?"
    session['real_answer'] = str(row[0][0])
    answers = []
    answers.append(session['real_answer'])
    query = "SELECT DISTINCT artist_name FROM artists INNER JOIN (SELECT DISTINCT artist_id FROM songs WHERE song_name NOT LIKE '%seven%' AND album_name NOT LIKE '%seven%') AS seven ON artists.artist_id = seven.artist_id  ORDER BY RAND() LIMIT 3;"
    cur.execute(query)
    row = cur.fetchall()
    for i in range(3):
        answers.append(str(row[i][0]))
    session['answers'] = answers
    mysql.connection.commit()
    cur.close()