import mysql.connector as m
import random

class Empty(Exception):
    pass


con = m.connect(
    host="localhost",
    user="root",
    password="----------",
    database="flashcard"
)
cur = con.cursor()


def exit_overview():
    cur.execute("select question, answer, success, fails from flashcards")
    data = cur.fetchall()
    print("Exiting the program...")
    print(data)
    return data


def add(question, answer):
    if question == "" or answer == "":
        raise Empty("The fields were left empty!")

    q = question.lower().strip()
    cur.execute(
        "insert into flashcards values (%s,%s,%s,%s)",
        (q, answer, 0, 0)
    )
    con.commit()


def check(question, answer):
    cur.execute(
        "select answer from flashcards where question=%s",
        (question,)
    )
    row = cur.fetchone()

    if row is None:
        return False, None

    correct = row[0]

    if answer.lower().strip() == correct:
        print("Correct!")
        cur.execute(
            "update flashcards set success=success+1 where question=%s",
            (question,)
        )
        con.commit()
        return True, correct
    else:
        print("Incorrect! The correct answer is:", correct)
        cur.execute(
            "update flashcards set fails=fails+1 where question=%s",
            (question,)
        )
        con.commit()
        return False, correct


def show():
    cur.execute("select question from flashcards")
    qs = cur.fetchall()

    if qs == []:
        raise Empty("No questions available")

    questions = [i[0] for i in qs]

    while questions:
        q = random.choice(questions)
        print(q)
        ans = input("Enter the answer: ")

        if ans == "1011":
            exit_overview()
            break

        questions.remove(q)
        check(q, ans)


def edit(question, new_question, new_answer):
    q = question.lower().strip()
    nq = new_question.lower().strip()

    cur.execute("select question from flashcards where question=%s", (q,))
    if cur.fetchone() is None:
        print("Question not found!")
        return

    cur.execute(
        """update flashcards
           set question=%s, answer=%s, success=0, fails=0
           where question=%s""",
        (nq, new_answer, q)
    )
    con.commit()
