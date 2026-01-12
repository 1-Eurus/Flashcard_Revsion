import tkinter as tk
from tkinter import simpledialog, messagebox
import random
from backend import add, edit, check, exit_overview, Empty, show

root = tk.Tk()
root.title("TEST Revision Tool")
root.geometry("500x250")

current_question = None
remaining_questions = []

# --- UI Elements ---
question_label = tk.Label(root, text="Welcome to TESTER!", font=("Arial", 14), wraplength=480)
question_label.pack(pady=(20, 10))



answer_entry = tk.Entry(root, width=40)
submit_btn = tk.Button(root, text="Submit")

menu_frame = tk.Frame(root)
menu_frame.pack(pady=10)

# --- Functions ---

def end_test(): #ends test when called
    global remaining_questions
    
    remaining_questions = [] 
    question_label.config(text="Test Finished!") #displays exit message

    answer_entry.pack_forget()
    submit_btn.pack_forget()
    menu_frame.pack(pady=5)

def start_test(): #to start the test 
    global current_question, remaining_questions
    menu_frame.pack_forget()

    if not remaining_questions:
        remaining_questions = show()
        if not remaining_questions: #if there are no questions to put in test
            
            messagebox.showwarning("No Questions!", "Your database is empty!")
            menu_frame.pack(pady=5)
            return

    current_question = random.choice(remaining_questions) #randomly choses a question from the list of remaining questions
    remaining_questions.remove(current_question) #removes the question after use from list

    question_label.config(text=current_question) #displays question
    answer_entry.delete(0, tk.END)
    answer_entry.pack(pady=(0, 5))
    submit_btn.pack(pady=(0, 10))

def submit_answer(): #checks answer 
    global current_question
    ans = answer_entry.get().strip()

    if not ans:
        messagebox.showwarning("Warning", "Please enter an answer") #gives warning if empty
        return


    # Uses backend 'check' function
    correct, right_ans = check(current_question, ans) 

    if correct:
        messagebox.showinfo("Result", "✅ Correct!")
    else:
        messagebox.showerror("Result", f"❌ Wrong!\nCorrect answer: {right_ans}")

    if remaining_questions: #if questions are left it goes to next question
        start_test() 
    else:
        messagebox.showinfo("Test Complete", "You've gone through all the questions!") #message to show test is over
        end_test()

def add_card():#adds questions to the database
    
    q = simpledialog.askstring("Add Question", "Enter Question:") #user input for qeustions and answers
    a = simpledialog.askstring("Add Answer", "Enter Answer:")
    
    if q and a:
        try:
            add(q, a) # Backend call to fucntion 'add'
            messagebox.showinfo("Success", "Question added!")
        except Empty as e: #shows error if empty
            messagebox.showerror("Error", str(e))

def edit_card():#to modify existing question and answer
    
    old_q = simpledialog.askstring("Edit", "Question to edit:") #user input for which question to edit
    new_q = simpledialog.askstring("Edit", "New Question:")#user input for changing it to the required question and answer
    new_a = simpledialog.askstring("Edit", "New Answer:")
    
    if old_q and new_q and new_a:
        edit(old_q, new_q, new_a) # Backend call to function 'edit'
        messagebox.showinfo("Success", "Question updated!")

def view_progress():#shows success and failures
    overview = exit_overview() # Backend call
   
    report = "\n".join([f"Q: {r[0]} | Success: {r[2]} | Fails: {r[3]}" for r in overview])
    messagebox.showinfo("Progress Overview", report if report else "No data found.")

# --- Menu Buttons ---
tk.Button(menu_frame, text="Start Test", command=start_quiz).grid(row=0, column=0, padx=5)
tk.Button(menu_frame, text="Add Question", command=add_card).grid(row=0, column=1, padx=5)
tk.Button(menu_frame, text="Edit Question", command=edit_card).grid(row=0, column=2, padx=5)
tk.Button(menu_frame, text="View Progress", command=view_progress).grid(row=0, column=3, padx=5)

submit_btn.config(command=submit_answer)

root.mainloop()
