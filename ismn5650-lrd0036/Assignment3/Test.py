import requests
import random

API_KEY = "c0b2eacf05076f13b78dfdda91307cbe2168515f0b42a244105052532b31ceac"
API_BASE_URL = "https://ismn5650-questionsapi.azurewebsites.net/"

HEADERS = {
    "x-api-key": API_KEY
}

def get_categories():
    url = f"{API_BASE_URL}metadata"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get('categories', [])
    else:
        print(f"Failed to retrieve categories. Status code: {response.status_code}")
        print(f"Response text: {response.text}")
        return []

def get_category_statistics(category_id):
    url = f"{API_BASE_URL}stats"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        stats_list = response.json()
        for stat in stats_list:
            if stat['category']['id'] == category_id:
                return {
                    "easy": stat.get("easy", {}),
                    "medium": stat.get("medium", {}),
                    "hard": stat.get("hard", {})
                }
        return {}
    else:
        print(f"Failed to retrieve category statistics. Status code: {response.status_code}")
        print(f"Response text: {response.text}")
        return {}

def fetch_trivia_questions(category_id, difficulty):
    url = f"{API_BASE_URL}questions"
    params = {
        "categoryId": category_id,
        "difficulty": difficulty.lower(),
        "max": 10
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        questions = response.json()
        # Filter questions to only keep those with matching category id
        filtered_questions = [q for q in questions if q['category']['id'] == category_id]
        return filtered_questions
    else:
        print(f"Failed to retrieve trivia questions. Status code: {response.status_code}")
        print(f"Response text: {response.text}")
        return []


def play_trivia_game(category, difficulty):
    questions = fetch_trivia_questions(category['id'], difficulty)
    if not questions:
        print("No questions available for this category and difficulty.")
        return

    questions = questions[:10]  # Limit to max 10 questions here

    score = 0
    question_number = 1

    # Continue processing questions...


    for q in questions:
        print(f"\nQuestion {question_number}: {q['question']}")

        if q['type'] == "multiple":
            answers = q['incorrect_answers'] + [q['correct_answer']]
            random.shuffle(answers)
            options_map = {}
            for idx, ans in enumerate(answers):
                letter = chr(ord('A') + idx)
                options_map[letter] = ans
                print(f"{letter}.) {ans}")
            while True:
                user_choice = input("What's your choice: ").upper()
                if user_choice in options_map:
                    selected_answer = options_map[user_choice]
                    break
                else:
                    print("Invalid choice. Enter valid letter.")
        else:
            options_map = {"A": "True", "B": "False"}
            print("A) True")
            print("B) False")
            while True:
                user_choice = input("What's your choice: ").upper()
                if user_choice in options_map:
                    selected_answer = options_map[user_choice]
                    break
                else:
                    print("Invalid choice. Enter A or B.")

        if selected_answer == q['correct_answer']:
            score += 1

        question_number += 1

    print(f"\nFinal Score: {score}/{len(questions)} = {score / len(questions) * 100:.1f}%")

def display_main_menu():
    print("\n1) Lookup Category Statistics")
    print("2) Play Trivia Game")
    print("3) Exit")

def display_categories(categories):
    print("\nPlease choose one of the following categories:")
    for idx, cat in enumerate(categories, start=1):
        print(f"{idx}. {cat['name']} (ID: {cat['id']})")

def display_category_statistics(category_name, stats):
    print(f"\nYour selection: {category_name}\n")
    print(f"{category_name}:")
    for difficulty, types in stats.items():
        print(f"  {difficulty.capitalize()}:")
        for question_type, count in types.items():
            print(f"    {question_type}: {count}")

def select_category(categories):
    while True:
        try:
            choice = int(input("Your selection: "))
            if 1 <= choice <= len(categories):
                return categories[choice - 1]
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a number.")

def select_difficulty():
    difficulties = ["Easy", "Medium", "Hard"]
    print("\nPlease choose a difficulty:")
    for diff in difficulties:
        print(diff)
    while True:
        choice = input("Your selection: ").capitalize()
        if choice in difficulties:
            return choice
        else:
            print("Invalid difficulty. Try again.")

def main():
    categories = get_categories()
    if not categories:
        print("No categories available. Exiting.")
        return

    while True:
        display_main_menu()
        choice = input("Choose an option: ")
        if choice == "1":
            display_categories(categories)
            category = select_category(categories)
            stats = get_category_statistics(category['id'])
            display_category_statistics(category['name'], stats)
        elif choice == "2":
            display_categories(categories)
            category = select_category(categories)
            difficulty = select_difficulty()
            print(f"\nStarting trivia game for category: {category['name']} at {difficulty} difficulty")
            play_trivia_game(category, difficulty)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
