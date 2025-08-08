import tkinter as tk
from tkinter import messagebox
import json

window = tk.Tk()
window.title("Quiz Creator Tool")
window.geometry("400x300")

quizzes = {}

# this saves quizzes to a json file
def save_quizzes_to_file(filename = "quizzes.json"):
    with open(filename,"w") as f:
        json.dump(quizzes,f)
    
def load_quizzes_from_file(filename = "quizzes.json"):
    try:
        with open(filename,"r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
quizzes = load_quizzes_from_file()

def create_quiz():
    create_window = tk.Toplevel(window)
    create_window.title("Create a New Quiz")
    create_window.geometry("400x400")

    tk.Label(create_window, text="Quiz name:").pack()
    quiz_name_entry = tk.Entry(create_window)
    quiz_name_entry.pack()

    tk.Label(create_window, text="Question:").pack()
    question_entry = tk.Entry(create_window)
    question_entry.pack()

    tk.Label(create_window, text="Answer:").pack()
    answer_entry = tk.Entry(create_window)
    answer_entry.pack()

    questions = []

    def add_question():
        q = question_entry.get()
        a = answer_entry.get()
        
        if q and a:
            questions.append((q,a))
            question_entry.delete(0,tk.END)
            answer_entry.delete(0,tk.END)
            messagebox.showinfo("Added","Question added.")
        else:
            messagebox.showwarning("Missing Info","Please enter both a question and an answer")

    def finish_quiz():
        quiz_name = quiz_name_entry.get()
        if not quiz_name:
            messagebox.showwarning("No name.","Please enter a quiz name.")
            return
        if not questions:
            messagebox.showwarning("No questions,","Please add atleast one question to continue")
            return
        
        quizzes[quiz_name] = questions
        save_quizzes_to_file()
        messagebox.showinfo("Saved", f"Quiz '{quiz_name}' saved succesfully!")
        create_window.destroy()

    tk.Button(create_window, text = "Add Question", command = add_question).pack(pady=5)
    tk.Button(create_window ,text="Finish quiz" , command = finish_quiz).pack(pady=10)


def take_quiz():
    messagebox.showinfo("Take a quiz", "This will open the take quiz window.")

def delete_quiz():
    messagebox.showinfo("Delete a quiz", "This will open the delete quiz window.")

def exit_app():
    window.destroy()

tk.Label(window, text="Welcome to the Quiz Creator!", font=("Times New Roman",16)).pack(pady=20)

tk.Button(window, text="Create a new quiz", width=25, command=create_quiz).pack(pady=5)
tk.Button(window, text="Take a quiz", width=25,command=take_quiz).pack(pady=5)
tk.Button(window, text="Delete a quiz", width=25, command=delete_quiz).pack(pady=5)
tk.Button(window, text="Exit", width=25, command=exit_app).pack(pady=20)

window.mainloop()
