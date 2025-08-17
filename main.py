import tkinter as tk
from tkinter import messagebox, simpledialog
import random
from backend import add, edit, check, exit, Empty, file  # use your existing backend

root = tk.Tk()
root.title("Flashcard Revision Tool")

current_question = None
answer_entry = None
question_label = None

def start_quiz():
    global current_question, answer_entry, question_label

    questions = file["Question"].tolist()
    if not questions:
        messagebox.showwarning("Warning", "No flashcards available")
        return

    current_question = random.choice(questions)

    for widget in frame.winfo_children():
        widget.destroy()

    question_label = tk.Label(frame, text=current_question, font=("Arial", 14))
    question_label.pack(pady=10)

    answer_entry = tk.Entry(frame, width=40)
    answer_entry.pack(pady=5)

    submit_btn = tk.Button(frame, text="Submit", command=submit_answer)
    submit_btn.pack(pady=5)

def submit_answer():
    global current_question, answer_entry

    ans = answer_entry.get()
    if not ans:
        messagebox.showwarning("Warning", "Please enter an answer")
        return

    correct, right_ans = check(current_question, ans)
    if correct:
        messagebox.showinfo("Result", "✅ Correct!")
    else:
        messagebox.showerror("Result", f"❌ Wrong! Correct: {right_ans}")

    # Immediately ask next question
    start_quiz()

def add_card():
    q = simpledialog.askstring("Add Flashcard", "Enter Question")
    a = simpledialog.askstring("Add Flashcard", "Enter Answer")
    if q and a:
        try:
            add(q, a)
            messagebox.showinfo("Success", "Flashcard added successfully")
        except Empty as e:
            messagebox.showerror("Error", str(e))

def edit_card():
    old_q = simpledialog.askstring("Edit Flashcard", "Enter the question to edit")
    new_q = simpledialog.askstring("Edit Flashcard", "Enter new question")
    new_a = simpledialog.askstring("Edit Flashcard", "Enter new answer")
    if old_q and new_q and new_a:
        try:
            edit(old_q, new_q, new_a)
            messagebox.showinfo("Success", "Flashcard edited successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def view_progress():
    overview = exit()
    messagebox.showinfo("Progress Overview", str(overview))

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

tk.Button(frame, text="Start Quiz", command=start_quiz).pack(pady=5)
tk.Button(frame, text="Add Flashcard", command=add_card).pack(pady=5)
tk.Button(frame, text="Edit Flashcard", command=edit_card).pack(pady=5)
tk.Button(frame, text="View Progress", command=view_progress).pack(pady=5)

root.mainloop()
