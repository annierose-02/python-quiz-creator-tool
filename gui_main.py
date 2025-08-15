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

#this loads quizzes from file
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

    questions_Listbox = tk.Listbox(create_window, width=50,height=8)
    questions_Listbox.pack(pady=5)

    def add_question():
        q = question_entry.get()
        a = answer_entry.get()
        
        if q and a:
            questions.append((q,a))
            questions_Listbox.insert(tk.END,f"Q: {q} | A: {a}")
            question_entry.delete(0,tk.END)
            answer_entry.delete(0,tk.END)
            messagebox.showinfo("Added","Question added.")
        else:
            messagebox.showwarning("Missing Info","Please enter both a question and an answer")

    def delete_question():
        selected_index = questions_Listbox.curselection()
        if selected_index:
            index = selected_index[0]
            questions_Listbox.delete(index)
            del questions[index]
            messagebox.showinfo("Deleted","Question deleted")
        else:
            messagebox.showwarning("Missing Info","Please select a question to delete")

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
    tk.Button(create_window , text="Delete Question",command=delete_question).pack(pady=5)
    tk.Button(create_window ,text="Finish quiz" , command = finish_quiz).pack(pady=10)


def take_quiz():
    take_window = tk.Toplevel(window)
    take_window.title("Take a quiz")
    take_window.geometry("400x400")

    tk.Label(take_window, text="Select a quiz:").pack()

    quiz_Listbox = tk.Listbox(take_window)
    for quiz_name in quizzes.keys():
        quiz_Listbox.insert(tk.END,quiz_name)
    quiz_Listbox.pack(pady=10)

    def start_selected_quiz():
        selected = quiz_Listbox.curselection()
        if not selected:
            messagebox.showwarning("No quiz selected","Please select a quiz to take")
            return
        quiz_name = quiz_Listbox.get(selected[0])
        play_quiz(quiz_name) #playquiz function not defined yet
        take_window.destroy()

    tk.Button(take_window, text = "Start Quiz", command = start_selected_quiz).pack(pady=5)
    tk.Button(take_window, text = "Cancel", command = take_window.destroy).pack(pady=5)
        
from tkinter import simpledialog

def play_quiz(selected_quiz):
    import tkinter as tk
    from tkinter import messagebox

    questions = quizzes[selected_quiz]
    score = 0
    current_index = 0
    user_answers = []

    play_window = tk.Toplevel(window)
    play_window.title(f"Play Quiz: {selected_quiz}")
    play_window.geometry("400x300")

    question_label = tk.Label(play_window, text="")
    question_label.pack(pady =10)

    answer_entry = tk.Entry(play_window)
    answer_entry.pack(pady =5)

    def load_question():
        q, _ = questions[current_index]
        question_label.config(text = f"Q {current_index + 1}: {q}")
        answer_entry.delete(0,tk.END)

    def show_review():
        review_window = tk.Toplevel(window)
        review_window.title("Quiz review")
        review_window.geometry("400x300")

        tk.Label(review_window , text = f"Score: {score}/{len(questions)}", font = ("Helvetica",14,"bold")).pack(pady=10)

        frame = tk.Frame(review_window)
        frame.pack(fill = "both", expand = True)
         
        text = tk.Text(frame, wrap = "word", font=("Helvetica",12))
        text.pack(fill = "both" , expand = True)

        for i, (q,user_answer,correct_a) in enumerate (user_answers, start=1):
            text.insert("end",f"Q{i}: {q}\n")
            text.insert("end",f"Your answer: {user_answer}\n")
            text.insert("end", f"Correct answer: {correct_a}\n\n")

        scrollbar = tk.Scrollbar(frame , command = text.yview)
        text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side = "right", fill = "y")

        text.config(state="disabled")
        tk.Button(review_window, text="Back to Menu",command = review_window.destroy).pack(pady=10)
        
    def next_question():
        nonlocal score, current_index
        user_answer = answer_entry.get()

        if not user_answer:
            messagebox.showwarning("No answer","Please enter an answer before continuing")
            return
        
        q, a = questions[current_index]
        user_answers.append((q , user_answer , a))
        
        if user_answer.strip().lower() == questions[current_index][1].strip().lower():
            score = score + 1
        
       
        current_index += 1
        if current_index < len(questions):
            load_question()
        else:
            messagebox.showinfo("Score",f"You scored {score} out of {len(questions)} on this quiz")
            play_window.destroy()
            show_review()

    def quit_quiz():
        confirm = messagebox.askyesno("Quit quiz","Are you sure you want to quit?")
        if confirm:
            play_window.destroy()
            show_review()

    
    next_button = tk.Button(play_window , text = "Next" , command = next_question)
    next_button.pack(pady=5)
    quit_button = tk.Button(play_window , text = "Quit" , command = quit_quiz)
    quit_button.pack(pady=5)

    load_question()

        
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
