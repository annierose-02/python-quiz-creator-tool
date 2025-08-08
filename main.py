import json

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

def show_menu():
    print("=== Quiz Creator Tool ===")
    print("1. Create a new quiz")
    print("2. Take a quiz")
    print("3. Delete a quiz")
    print("4. Exit")

def create_quiz():
    print("\n--- Creating a New Quiz ---")
    quiz_name = input("Enter a name for your quiz: ")
    questions = []

    while True:
        question = input("\nEnter your question: ")
        answer = input("Enter the answer: ")
        questions.append((question, answer))

        more = input("Add another question? (yes/no): ").lower()
        if more != "yes":
            break

    quizzes[quiz_name] = questions
    save_quizzes_to_file()


    print(f"\nQuiz '{quiz_name}' created with {len(question)} questions:")
    for q, a in questions:
        print(f"Q: {q} | A: {a}")


def take_quiz():
    if not quizzes:
        print("\nNo quizzes available yet.")
        return
    
    print("\nAvailable quizzes:")
    for names in quizzes:
        print(f"-{names}")

    quiz_name = input("Enter the name of the quiz you would like to take: ")

    if quiz_name not in quizzes:
        print("\nQuiz not found")
        return
    
    score = 0
    for q, a in quizzes[quiz_name]:
        user_answer = input(q + ":")
        if user_answer.strip().lower() == a.lower():
            print("\nCorrect!")
            score = score + 1
        else:
            print(f"\nWrong! The answer is {a}.")


    print(f"\nYou scored {score} out of {len(quizzes[quiz_name])}")

def delete_quiz():
    global quizzes
    if not quizzes:
        print("\nNo quizzes available to delete")
        return
    
    print("\nAvailable quizzes :")
    for names in quizzes:
        print(f"-{names}")

    quiz_name = input("Enter the name of the quiz you would like to delete: ")

    if quiz_name in quizzes:
        confirm = input(f"Are you sure you want to delete {quiz_name}? (yes/no): ").lower()
        if confirm == "yes":
            del quizzes[quiz_name]
            save_quizzes_to_file()
            print(f"\n Quiz {quiz_name} deleted.")
        else:
            print("Deletion cancelled.")
    else:
        print("Quiz not found.")
        

def main():
    global quizzes 
    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == '1':
            create_quiz()
        elif choice == '2':
            take_quiz()
        elif choice == '3':
            delete_quiz()
        elif choice == '4':
            print("Goodbye!")
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()