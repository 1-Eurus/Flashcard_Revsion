import tkinter as tk
from tkinter import simpledialog, messagebox
import random
from backend import add, edit, check, exit, Empty
import csv

CSV_PATH = "info.csv"

root = tk.Tk()
root.title("Flashcard Revision Tool")
root.geometry("500x250")

current_question = None
remaining_questions = []

# --- Question display ---
question_label = tk.Label(root, text="", font=("Arial", 14), wraplength=480, justify="left")
question_label.pack(pady=(10,5))

answer_entry = tk.Entry(root, width=40)  # pack dynamically
submit_btn = tk.Button(root, text="Submit")  # pack dynamically

# --- Menu buttons frame ---
menu_frame = tk.Frame(root)
menu_frame.pack(pady=5)

tk.Button(menu_frame, text="Start Quiz", command=lambda: start_quiz()).grid(row=0, column=0, padx=5)
tk.Button(menu_frame, text="Add Flashcard", command=lambda: add_card()).grid(row=0, column=1, padx=5)
tk.Button(menu_frame, text="Edit Flashcard", command=lambda: edit_card()).grid(row=0, column=2, padx=5)
tk.Button(menu_frame, text="View Progress", command=lambda: view_progress()).grid(row=0, column=3, padx=5)

submit_btn.config(command=lambda: submit_answer())

# --- Helper to read questions ---
def read_questions():
    try:
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            return [row["Question"].strip() for row in csv.DictReader(f) if row.get("Question")]
    except Exception:
        return []

# --- End quiz helper ---
def end_quiz():
    global remaining_questions
    remaining_questions = []  # reset
    question_label.config(text="")
    answer_entry.pack_forget()
    submit_btn.pack_forget()
    menu_frame.pack(pady=5)

# --- Quiz functions ---
def start_quiz():
    global current_question, remaining_questions
    menu_frame.pack_forget()  # hide menu buttons during quiz

    # Initialize remaining_questions if empty
    if not remaining_questions:
        remaining_questions = read_questions()
        if not remaining_questions:
            messagebox.showwarning("No Flashcards", "No flashcards available")
            menu_frame.pack(pady=5)
            return

    current_question = random.choice(remaining_questions)
    remaining_questions.remove(current_question)

    question_label.config(text=current_question)
    answer_entry.delete(0, tk.END)
    answer_entry.pack(pady=(0,5))
    submit_btn.pack(pady=(0,10))

def submit_answer():
    global current_question, remaining_questions
    ans = answer_entry.get().strip()
    if not ans:
        messagebox.showwarning("Warning", "Please enter an answer")
        return

    # Special exit code
    if ans == "1011":
        overview = exit()
        messagebox.showinfo("Progress Overview", str(overview))
        end_quiz()
        return

    correct, right_ans = check(current_question, ans)
    if correct:
        messagebox.showinfo("Result", "✅ Correct!")
    else:
        messagebox.showerror("Result", f"❌ Wrong! Correct: {right_ans}")

    # Check if questions remain
    if remaining_questions:
        start_quiz()
    else:
        messagebox.showinfo("Quiz Complete", "You have answered all questions!")
        end_quiz()

# --- Utility buttons ---
def add_card():
    q = simpledialog.askstring("Add Flashcard", "Enter Question")
    a = simpledialog.askstring("Add Flashcard", "Enter Answer")
    if q and a:
        try: add(q, a)
        except Empty as e: messagebox.showerror("Error", str(e))

def edit_card():
    old_q = simpledialog.askstring("Edit Flashcard", "Enter the question to edit")
    new_q = simpledialog.askstring("Edit Flashcard", "Enter new question")
    new_a = simpledialog.askstring("Edit Flashcard", "Enter new answer")
    if old_q and new_q and new_a:
        try: edit(old_q, new_q, new_a)
        except Exception as e: messagebox.showerror("Error", str(e))

def view_progress():
    try: overview = exit()
    except Exception as e: messagebox.showerror("Error", str(e))
    else: messagebox.showinfo("Progress Overview", str(overview))

root.mainloop()
