import random
import csv

class Empty(Exception):
    def __init__(self, message="The fields were left empty!"):
        super().__init__(message) #custom exception for empty fields

def exit():
    file = open("info.csv",'r', newline='')
    ro = csv.DictReader(file)
    overview = []
    for i in ro:
        overview.append((i["Question"], i['Answer'], i['Success'], i['Fails']))
    print("Exiting the program...")
    print(overview)
    file.close()
    return overview #returns the overview of the questions, success and fails

def add(question,answer):#to add a new question and answer
    file = open("info.csv",'a', newline='')
    wo = csv.DictWriter(file, fieldnames=["Question","Answer","Success","Fails"])

    if question =="" or answer =="": #checks incase question and answer fields are empty
        raise(Empty)
    else:
        new= {"Question": question.lower().strip(), "Answer": answer, "Success": "0", "Fails": "0"} #answer can only be a single word
        wo.writerow(new)

    file.close()

def check(question, answer):
    file = open("info.csv",'r', newline='')
    ro = csv.DictReader(file)
    rows = list(ro)
    file.close()
    is_correct = False
    correct_answer = None
    
    for i in rows:
        if question == i["Question"]:
            correct_answer = i["Answer"]
            if answer.lower().strip() == i["Answer"]:
                print("Correct!")
                i["Success"] = str(int(i["Success"]) + 1)  # ← NEW: Increment success
                is_correct = True
            else:
                print(f"Incorrect! The correct answer is: {i['Answer']}")
                i["Fails"] = str(int(i["Fails"]) + 1)  # ← NEW: Increment fails
                is_correct = False
            break
    
    if correct_answer is not None:  # ← NEW: Write updated data back to CSV
        file = open("info.csv",'w', newline='')
        fieldnames = ['Question','Answer','Success','Fails']
        wo = csv.DictWriter(file, fieldnames=fieldnames)
        wo.writeheader()
        for row in rows:
            wo.writerow(row)
        file.close()
    return is_correct, correct_answer
    
def show(): #shows a random question from the file and asks the answer
    file = open("info.csv",'r', newline='')
    ro = csv.DictReader(file)

    questions = []
    for i in ro:
        questions.append(i["Question"]) #gets all the questions from the file

    if questions==[]: #checks if the file is empty
        raise(Empty) #if empty the empty exception is raised 

    while True:
        if questions==[]: #once all questions are done the loop breaks
            break

        question = random.choice(questions) #chooses a random question from the list
        print(question)
        answer = input("Enter the answer: ") #replace with input from user interface

        if answer == "1011": #if the answer is this specific input it will stop everything, show results 
            exit()
            break

        questions.remove(question) #removes question from list after asking it once
        check(question,answer)

    file.close()

def edit(question, new_question, new_answer): #to edit a question and answer
    file = open("info.csv",'r', newline='')
    ro = csv.DictReader(file)
    rows = list(ro)
    questions = [i["Question"] for i in rows] #gets all the questions from the file
    file.close()

    if question.lower().strip() not in questions: #checks if the question is in the file
        print(f"Question '{question}' not found!") 
        return

    else: #replaces old question and answers with new ones and resets the success and fails count
        file = open("info.csv",'w', newline='')
        fieldnames = ['Question','Answer','Success','Fails']
        wo = csv.DictWriter(file, fieldnames=fieldnames)
        wo.writeheader()
        for i in rows:
            if i["Question"] == question.lower().strip():
                i["Question"] = new_question
                i["Answer"] = new_answer
                i["Success"] = "0"
                i["Fails"] = "0"
            wo.writerow(i)
        file.close()

