import requests
import json
from random import shuffle
from colorama import init, Fore, Style


LOGO = f""" {Fore.BLUE}
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
██████████████░░░░░░░░░░░░░░░░░░░░░░░░░░
█░░░░░░░░░░░░░██░░░░░░░░░░░░░░░░░░░░░░░░
█░░░░░░░░░░░░░░░█░░░░░░░█░░████░░░░░░░░░
█░░░░░░░░░░░░░░░░█░░░░░░░░░░░░████░░░░░░
█░░░░░░░██░░░░░░░██░░░░░░░░░░░░░░██░░░░░
█░░░░░░░░██░░░░░░█░░░░░░░░░░░░░░░░░█░░░░
█░░░░░░░░░██░░░░██░░░░█░░█░░░░██████████
█░░░░░░░░░░█░░███░█░░░█░░██░░░░░░██░░░░░
█░░░░░░░░░░███░░░░█░░██░░░█░░░░░░███████
████████████░██░░░████░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░█░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░█░░░░░░░░████████░░░░░░█░░░░░░░░░
░░░░░░██░░░░░░░░██░░░░██░░░░░░█░░░░░░░░░
░░░░░█░░█░░░░░░░███████░░░░░░░█░░░░░░░░░
░░░░█░░░██░░░░░░░█░░░░░░░░░░░░█░░░░░░░░░
░░░█████████░░░░░█░░░░░░░░░░░░█░░░░░░░░░
░░██░░░░░░░██░░░░█░░░░░░░░░░░░█░░░░░░░░░
░█░░░░░░░░░░█░░░░█░░░░░░░░░░░░█░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
{Style.RESET_ALL}
"""

PREFIX = f"{Fore.BLUE}[QuizAPI]{Style.RESET_ALL}"

# Base URL
URL = 'https://opentdb.com/api.php'

# Categories and their numbers 
CATEGORIES = {
    "General Knowledge": 9,
    "Cartoon": 32,
    "Anime": 31,
    "Gadgets": 30,
    "Comics": 29,
    "Politics" : 24
}

def prepare_quiz():
    print(LOGO)
    while True:
        try:
            question_amount = int(input(PREFIX + "How many questions do you want (max. 50) --> ")) # sets amount of questions with a max of 50
            print(PREFIX + "Categories: ")
            for key in CATEGORIES:
                print(key)
            selected_category = str(input(PREFIX + "Please select your category --> "))
            if selected_category not in CATEGORIES:
                print(PREFIX + "Please enter a valid category.")
                continue
            url = f"{URL}?amount={question_amount}&category={CATEGORIES[selected_category]}" # Final request URL
            break
        except ValueError:
            print(PREFIX + "Please enter a number between 1-50.")
    return url

def get_response(url):
    response = requests.get(url) # get response from API
    if response.status_code == 200: # if response successful
        request_data = response.json()
        if request_data["response_code"] == 0:
            results = request_data["results"]
            return results  # returns only the results of the response, results contains the questions and the right and wrong answers
        
        else:
            print(PREFIX + "There was an error sending a GET request to the API. Try again later.")
    else:
        print(PREFIX + "There was an error sending a GET request to the API. Try again later.")

def start_quiz(results):
    correct_answers = 0
    wrong_answers = 0
    question_list = []
    for result in results:
        question = result["question"]
        correct_answer = result["correct_answer"]
        incorrect_answers = result["incorrect_answers"]

        question_data = {
            "question": question,
            "correct_answer": correct_answer,
            "incorrect_answers": incorrect_answers
        }
        question_list.append(question_data)

    for question_data in question_list:
        answers = [question_data["correct_answer"]] + question_data["incorrect_answers"]
        shuffle(answers)
        question_data["shuffled_answers"] = answers

    # Main game loop, questions are asked here
    for i, question_data in enumerate(question_list, start=1):
        print(f"Question {i}: {question_data['question']}")
        shuffled_answers = question_data["shuffled_answers"]
        for j, answer in enumerate(shuffled_answers, start=1):
            print(f"{j}. {answer}")
        user_answer = input(PREFIX + "")
        if(user_answer == question_data["correct_answer"]):
            print(PREFIX + "You are right!")
            correct_answers += 1
        else:
            print(PREFIX + "You are wrong.")
            wrong_answers += 1
    print(f"{PREFIX} You were right {correct_answers} times!")
    print(f"{PREFIX} You were wrong {wrong_answers} times!")

if __name__ == '__main__':
    start_quiz(get_response(prepare_quiz())) # this is just for fun, i would not write actual production code like that :)
