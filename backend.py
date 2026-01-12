import mysql.connector as m
import random

class Empty(Exception):
    pass


con = m.connect(
    host="localhost",
    user="root",
    password="Lotus300902@",
    database="flashcard"
)
cur = con.cursor()


def exit_overview():#function to give overview before ending program

    
    cur.execute("select question, answer, success, fails from test") #using python sql connectivity to get data
    data = cur.fetchall()
    print("Exiting the program...")
    print(data)
    return data


def add(question, answer): #function to add questions and answers to sql database

    
    if question == "" or answer == "":
        raise Empty("The fields were left empty!") #raises exception if fields were left empty

    q = question.title().strip()
    
    cur.execute(
        "insert into flashcards values (%s,%s,%s,%s)",
        (q, answer, 0, 0)
    )
    con.commit()


def check(question, answer): #checks answer given for a question
    
    cur.execute(
        "select answer from flashcards where question=%s",
        (question,)
    )
    
    row = cur.fetchone()

    if row is None: #if row received is empty i.e the question is not in database 
        return False, None

    correct = row[0]

    if answer.lower().strip() == correct.lower().strip(): #to update successes and fails
        
        print("Correct!")

        #updates database
        cur.execute(
            "update flashcards set success=success+1 where question=%s",
            (question,)
        )
        
        con.commit()
        
        return True, correct
    
    else:
        
        print("Incorrect! The correct answer is:", correct)

        #updates database
        cur.execute(
            "update flashcards set fails=fails+1 where question=%s",
            (question,)
        )
        
        con.commit()
        
        return False, correct


def show(): #shows all questions saved in database
    
    cur.execute("select question from flashcards")
    qs = cur.fetchall()

    if qs == []: #when database is empty
        raise Empty("No questions available")

    questions = [i[0] for i in qs]

    while questions:
        
        q = random.choice(questions) #randomly choses a question
        
        questions.remove(q) 
       
def get_all_questions():
    cur.execute("SELECT question FROM flashcards")
    
    rows = cur.fetchall()
    
    question_list = []
    
    for row in rows:
        question_list.append(row[0])
        
    return question_list

def edit(question, new_question, new_answer): #edits questions in database
    
    q = question.title().strip()
    nq = new_question.title().strip()

    cur.execute("select question from flashcards where question=%s", (q,))
    
    if cur.fetchone() is None:#when question entered did not match any questions in database
        
        print("Question not found!")
        return

    
    cur.execute(
        """update flashcards
           set question=%s, answer=%s, success=0, fails=0
           where question=%s""",
        (nq, new_answer, q)
    )
    con.commit()
