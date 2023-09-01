# A little CLI quiz game
import requests # API requests
from random import shuffle # API returns 4 answers, first one is always right so they need to be shuffled
from util import LOGO, PREFIX, URL, CATEGORIES, MAX_QUESTIONS # Utilities like LOGO and PREFIX which would bloat this file too much
from colorama import Fore, Style # Color in the CLI

# Gets user input (amount of questions and category) and returnes these 2 values
def get_user_input():
    while True:
        try:
            question_amount = int(input(f"{PREFIX}How many questions do you want (max. {MAX_QUESTIONS}) --> "))
            if(question_amount > MAX_QUESTIONS) or question_amount < 1:
                print(f"{PREFIX}{Fore.RED}Enter a number between 1 and {MAX_QUESTIONS}.{Style.RESET_ALL}")
                continue
        except ValueError:
            print(f"{PREFIX}{Fore.RED}Enter a number between 1 and {MAX_QUESTIONS}.{Style.RESET_ALL}")
            continue

        print(f"{PREFIX}Categories:")
        print("---------------------------------")
        for key in CATEGORIES:
           print(key)
        print("---------------------------------")
        
        selected_category = str(input(f"{PREFIX}Please select your category --> "))
            
        if selected_category not in CATEGORIES:
            print(f"{PREFIX} {Fore.RED}Please enter a valid category.{Style.RESET_ALL}")
            continue
        break

    return question_amount, selected_category

# Sends a request to the API and returns the results
# Arguments: question_amount = number of questions to return; selected_category = question category
def send_api_request(question_amount, selected_category):
    url = f"{URL}?amount={question_amount}&category={CATEGORIES[selected_category]}"
    response = requests.get(url)

    if response.status_code == 200:
        request_data = response.json()
        if request_data["response_code"] == 0:
            results = request_data["results"]
            return results 
        
        else:
            print(f"{PREFIX}{Fore.RED}There was an error with the API response. Try again later.{Style.RESET_ALL}")
    else:
        print(f"{PREFIX}{Fore.RED}There was an error sending a GET request to the API. Try again later.{Style.RESET_ALL}")

# Creates and returns list out of the API response and shuffles the answers so it won't be the same answer over and over again
# Arguments: response = the API response 
def create_question_list(response):
    question_list = [] # list that contains all of the questions with corresponding answers
    for result in response:
        question = result["question"]
        correct_answer = result["correct_answer"]
        incorrect_answers = result["incorrect_answers"]

        question_data = {
            "question": question,
            "correct_answer": correct_answer,
            "incorrect_answers": incorrect_answers
        }
        question_list.append(question_data)

    # Create new key that contains the answers in a random order to avoid having the same answer over and over again
    for question_data in question_list:
        answers = [question_data["correct_answer"]] + question_data["incorrect_answers"]
        shuffle(answers)
        question_data["shuffled_answers"] = answers
    
    return question_list

# Actual quiz logic
# Arguments: question_list = The list of questions (and their corresponding answers) to ask the user
def start_quiz(question_list):
    correct_answers = 0
    wrong_answers = 0

    # Main game loop, questions are asked here
    for i, question_data in enumerate(question_list, start=1):
        print(f"Question {i}: {question_data['question']}")
        shuffled_answers = question_data["shuffled_answers"]
        for j, answer in enumerate(shuffled_answers, start=1):
            print(f"{j}. {answer}")
        user_answer = input(f"{PREFIX}")
        if(user_answer == question_data["correct_answer"]):
            print(f"{PREFIX}{Fore.GREEN}You are right.{Style.RESET_ALL}")
            correct_answers += 1
        else:
            print(f"{PREFIX}{Fore.RED}You are wrong.{Style.RESET_ALL}")
            wrong_answers += 1
        
    print(f"{PREFIX} You were right {correct_answers} times!")
    print(f"{PREFIX} You were wrong {wrong_answers} times!")

# Executes the whole program in right order
def main():
    print(LOGO)
    question_amount, selected_category = get_user_input()
    result = send_api_request(question_amount, selected_category)
    question_list = create_question_list(result)
    start_quiz(question_list)

# Main method
if __name__ == '__main__':
    main()
    
