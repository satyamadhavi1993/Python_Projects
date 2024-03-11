import json
import random
from pyfiglet import Figlet
import requests


def main():
    print_message('Welcome')
    gameon = True

    while gameon:
        category = get_category()
        difficulty = get_difficulty()
        questions_list = api_request(category, difficulty)
        display_questions(questions_list)
        gameon = continue_playing()
        
    print_message('Goodbye')


def print_message(message):
    figlet = Figlet()
    figlet.setFont(font='slant')
    print(figlet.renderText(message))


def continue_playing():
    while True:
        choice = input("Do you want to continue playing (Y or N): ").strip().upper()
        print()
        if choice in ['Y', 'YES']:
            return True
        elif choice in ['N', 'NO']:
            return False
        else:
            print('Please enter valid choice (Y or N)')


def get_difficulty():
    while True:
        difficulty_levels = {'E': 'easy', 'M': 'medium', 'H': 'hard', 'EASY': 'easy', 'MEDIUM': 'medium', 'HARD': 'hard', 'A': 'any', 'ANY': 'any'}
        try:
            difficulty = input("Select difficulty level. ('E' for Easy, 'M' for Medium, 'H' for Hard and 'A' for Any'): ").strip().upper()
            print()
        except ValueError:
            print('Please select valid difficulty level')
        if difficulty in difficulty_levels.keys():
            return difficulty_levels[difficulty]
        else:
            print('Please select a valid difficulty level (E, M, H or A).')


def get_category():
    print('Select a category from the below list\n')
    categories = {'Any Category': 1, 'General Knowledge': 2, 'Books': 3, 'Film': 4,  'Music': 5, 'Musicals & Theatres': 6, 'Television': 7, 
                  'Video Games': 8, 'Board Games': 9, 'Science & Nature': 10, 'Computers': 11, 'Mathematics': 12, 'Mythology': 13, 'Sports': 14,
                  'Geography': 15, 'History': 16, 'Politics': 17, 'Art': 18, 'Celebrities': 19, 'Animals': 20, 'Vehicles': 21, 'Comics': 22,
                  'Gadgets': 23, 'Japanese Anime & Manga': 24, 'Cartoon & Animations': 25
                 }
    
    category = None
    for category, index in categories.items():
        print(f'{index} - {category}')
    print()

    while True:
        try:
            category = int(input('Please enter you choice: ').strip())
        except ValueError:
            print('Please select valid input\n')
        if category in categories.values():
            print()
            break
        else:
            print('Please select valid category (1 to 25)\n')


    if category == 1:
        return 'any'
    else:
        return category + 7


def api_request(category, difficulty):
    questions_list = []

    url = f'https://opentdb.com/api.php?amount=50&type=multiple'
    if not category == 'any':
        url += f'&category={category}'
    if not difficulty == 'any':
        url += f'&difficulty={difficulty}'

    response = requests.get(url).json()
    for question in response['results']:
        questions_list.append({'question': question['question'], 'correct_answer': question['correct_answer'], 
                               'incorrect_answers': question['incorrect_answers'], 'difficulty': question['difficulty'], 
                               'category': question['category']})
    random.shuffle(questions_list)
    return questions_list[:10]


def display_questions(questions_list):
    score = 0
    for question_number, question in enumerate(questions_list):
        correct_answer = question['correct_answer']
        options = [correct_answer] + question['incorrect_answers']
        random.shuffle(options)
        correct_option_index = None
        print(f'{question_number + 1}. {question["question"]}\n')
        for index, option in enumerate(options):
            options_index = chr(97 + index)
            print(f'    {options_index}. {option}')
            if option == correct_answer:
                correct_option_index = options_index
        print()
        while True:
            answer = input('Enter your answer: ').lower()
            if answer in ['a', 'b', 'c', 'd']:
                if answer == correct_option_index:
                    print('Correct answer !!\n')
                    score += 1
                else:
                    print(f'Correct answer is: {correct_option_index}. {correct_answer}')    
                break    
            else:
                print('Please select an option from (a, b, c or d): ')
        print()
    print(f'Your total score is: {score}\n')

        
if __name__ == "__main__":
    main()
