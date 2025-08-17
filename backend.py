import pandas as pd 
import random


file= pd.read_excel("info.xlsx") 


class Empty(Exception):
    def __init__(self, message="The fields were left empty!"):
        super().__init__(message) #custom exception for empty fields

def exit():
    global file 

    print("Exiting the program...")

    overview = file[["Question","Success","Fails"]]

    print(overview)

    #break

    return overview #returns the overview of the questions, success and fails



def add(question,answer):#to add a new question and answer

    global file
    
    if question =="" or answer =="": #checks incase question and answer fields are empty
        raise(Empty)

    else:
        new= {"Question":question,"Answer":answer,"Success":0,"Fails":0} #answer can only be a single word
        new_df = pd.DataFrame([new])
        file = pd.concat([file, new_df], ignore_index=True) #adds the new question and answer to the file
        file.to_excel("info.xlsx", index=False)


def check(question, answer):
    correct_answer = file[file["Question"] == question]["Answer"].iloc[0]

    if answer.lower().strip() == correct_answer.lower().strip():
        print("Correct!")
        file.loc[file["Question"] == question, "Success"] = file[file["Question"] == question]["Success"].iloc[0] + 1  
        return True, correct_answer  
    else:
        print(f"Incorrect! The correct answer is: {correct_answer}")
        file.loc[file["Question"] == question, "Fails"] = file[file["Question"] == question]["Fails"].iloc[0] + 1
        return False, correct_answer  


def show(): #shows a random question from the file and asks the answer
    
    global file

    questions = file["Question"].tolist() #gets all the questions from the file
    
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
    
    
def edit(question, new_question, new_answer): #to edit a question and answer
    global file

    questions = file["Question"].tolist() #gets all the questions from the file

    if question not in questions: #checks if the question is in the file
        print(f"Question '{question}' not found!") 
        return
    
    else: #replaces old question and answers with new ones and resets the success and fails count
        file.loc[file["Question"] == question, "Answer"] = new_answer 
        file.loc[file["Question"] == question, "Question"] = new_question
        file.loc[file["Question"] == question, "Success"] = 0
        file.loc[file["Question"] == question, "Fails"] = 0


        file.to_excel("info.xlsx", index=False)
