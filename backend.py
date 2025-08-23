
import random

import csv


 


class Empty(Exception):
    def __init__(self, message="The fields were left empty!"):
        super().__init__(message) #custom exception for empty fields

def exit():
    file= open("info.xlsx",'r', newline='')
    ro = csv.DictReader(file)
    overview=[]
    for i in ro:
        overview.append(i["Question"], i['Answer'], i['Success'],i['Fails'])
    print("Exiting the program...")

    

    print(overview)

    
    file.close()
    return overview #returns the overview of the questions, success and fails



def add(question,answer):#to add a new question and answer

    file= open("info.xlsx",'a', newline='')
    
    wo= csv.writer(file)

    
    if question =="" or answer =="": #checks incase question and answer fields are empty
        raise(Empty)

    else:
        new= [question.lower().strip(),answer,0,0] #answer can only be a single word
        wo.writerow(new)

    file.close()


def check(question, answer):
    file= open("info.xlsx",'r', newline='')

    ro = csv.DictReader(file)

    for i in ro:
        if question== i["Question"]:
            if answer.lower().strip() == i["Answer"]:
                print("Correct!")
                return True, i["Answer"]
            else:
                print(f"Incorrect! The correct answer is: {i['Answer']}")
                return False, i["Answer"]

    file.close()


def show(): #shows a random question from the file and asks the answer
    
    file= open("info.xlsx",'r', newline='')
    ro = csv.DictReader(file)

    questions=[]
    for i in ro:
        questions.append(ro["Question"]) #gets all the questions from the file
    
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
    file= open("info.xlsx",'r', newline='')
    questions=[]
    ro = csv.DictReader(file)
    rows=list(ro)
    for i in rows:
        questions.append(rows["Question"]) #gets all the questions from the file#gets all the questions from the file
    file.close()
    if question.lower().strip() not in questions: #checks if the question is in the file
        print(f"Question '{question}' not found!") 
        return
    
    
    else: #replaces old question and answers with new ones and resets the success and fails count
        file= open("info.xlsx",'w', newline='')
        fieldnames = ['Question','Answer' 'Success', 'Fails']
        for i in rows:
            if i["Question"]== question.lower().strip():
                i["Question"]=new_question
                i["Answer"]=new_answer
                i["Success"]=0
                i["Fails"]=0
        wo = csv.DictWriter(file, fieldnames=fieldnames)
        wo.writeheader()
        wo.write(rows)
        file.close()
    
