import tkinter as tk
from tkinter import simpledialog, messagebox
import random
# Added get_all_questions to the import list
from backend import add, edit, check, exit_overview, Empty, get_all_questions

root = tk.Tk()
root.title("Flashcard Revision Tool")
root.geometry("500x250")

current_question = None
remaining_questions = []

# --- UI Elements ---
question_label = tk.Label(root, text="Welcome to Flashcards!", font=("Arial", 14), wraplength=480)
question_label.pack(pady=(20, 10))

answer_entry = tk.Entry(root, width=40)
submit_btn = tk.Button(root, text="Submit")

menu_frame = tk.Frame(root)
menu_frame.pack(pady=10)

# --- Functions ---

def end_quiz():
    global remaining_questions
    remaining_questions = []
    question_label.config(text="Quiz Finished!")
    answer_entry.pack_forget()
    submit_btn.pack_forget()
    menu_frame.pack(pady=5)

def start_quiz():
    global current_question, remaining_questions
    menu_frame.pack_forget()

    if not remaining_questions:
        # Now calls the backend instead of running local SQL
        remaining_questions = get_all_questions()
        if not remaining_questions:
            messagebox.showwarning("No Flashcards", "Your database is empty!")
            menu_frame.pack(pady=5)
            return

    current_question = random.choice(remaining_questions)
    remaining_questions.remove(current_question)

    question_label.config(text=current_question)
    answer_entry.delete(0, tk.END)
    answer_entry.pack(pady=(0, 5))
    submit_btn.pack(pady=(0, 10))

def submit_answer():
    global current_question
    ans = answer_entry.get().strip()

    if not ans:
        messagebox.showwarning("Warning", "Please enter an answer")
        return

    # Secret code to view progress mid-quiz
    if ans == "1011":
        view_progress()
        return

    # Uses backend 'check' function
    correct, right_ans = check(current_question, ans)

    if correct:
        messagebox.showinfo("Result", "✅ Correct!")
    else:
        messagebox.showerror("Result", f"❌ Wrong!\nCorrect answer: {right_ans}")

    if remaining_questions:
        start_quiz()
    else:
        messagebox.showinfo("Quiz Complete", "You've gone through all the cards!")
        end_quiz()

def add_card():
    q = simpledialog.askstring("Add Flashcard", "Enter Question:")
    a = simpledialog.askstring("Add Flashcard", "Enter Answer:")
    if q and a:
        try:
            add(q, a) # Backend call
            messagebox.showinfo("Success", "Flashcard added!")
        except Empty as e:
            messagebox.showerror("Error", str(e))

def edit_card():
    old_q = simpledialog.askstring("Edit", "Question to edit:")
    new_q = simpledialog.askstring("Edit", "New Question:")
    new_a = simpledialog.askstring("Edit", "New Answer:")
    if old_q and new_q and new_a:
        edit(old_q, new_q, new_a) # Backend call
        messagebox.showinfo("Success", "Flashcard updated!")

def view_progress():
    overview = exit_overview() # Backend call
    # Format the list/tuple into a readable string
    report = "\n".join([f"Q: {r[0]} | Success: {r[2]} | Fails: {r[3]}" for r in overview])
    messagebox.showinfo("Progress Overview", report if report else "No data found.")

# --- Menu Buttons ---
tk.Button(menu_frame, text="Start Quiz", command=start_quiz).grid(row=0, column=0, padx=5)
tk.Button(menu_frame, text="Add Flashcard", command=add_card).grid(row=0, column=1, padx=5)
tk.Button(menu_frame, text="Edit Flashcard", command=edit_card).grid(row=0, column=2, padx=5)
tk.Button(menu_frame, text="View Progress", command=view_progress).grid(row=0, column=3, padx=5)

submit_btn.config(command=submit_answer)

root.mainloop()