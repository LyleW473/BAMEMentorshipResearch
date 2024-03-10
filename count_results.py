import json
import re

def contains_letters(string):
    return any(char.isalpha() for char in string)

def clean_string(string):   

    # Remove any irrelevant characters from the string
    # Adapted to also remove any commas that appear inside the answers to subquestions,
    # E.g., {1: 16,938, 2:32,392} would cause issues with parsing
    corrected_string_chars = []
    for i in range(0, len(string)):
        if string[i] == ",":
            if not (string[i-1].isdigit() and string[i+1].isdigit()):
                corrected_string_chars.append(string[i])
        elif string[i].isdigit() or string[i] == ":" or string[i] == ",":
            corrected_string_chars.append(string[i])

    string = "".join(char for char in corrected_string_chars)
    print("corrected", string)
    return "".join(char for char in corrected_string_chars)

def format_answers(string):
    qs_map_answers = clean_string(string).split(",")
    return [sub_q_answer.split(":") for sub_q_answer in qs_map_answers]

def count_results(prob_number):

    with open(f"problems/answers/prob{prob_number}_answers.txt", "r") as answers_file:
        answers = answers_file.readlines()

    answers = [answer.replace("\n", "") for answer in answers] # Clean answers
    answers_indexes = {str(i): str(answers[i]) for i in range(1, len(answers))} # Indexes for each subquestion, skip the '#' operator
    print(answers_indexes)
    print(len(answers))

    with open(f"results/prob{prob_number}_predictions.json", "r") as predictions_file:
        predictions = json.load(predictions_file)
    
    # Filter and calculate the number of incorrect responses
    print(len(predictions))
    num_responses = len(predictions)
    predictions = {sub_qs:pred for sub_qs, pred in predictions.items() if not contains_letters(pred)}
    num_incorrect_responses = num_responses - len(predictions)
    print(num_incorrect_responses)

    # Remove any irrelevant characters from the predictions and format it into a list of tuples, where the first element is the subquestion and the second is the answer
    predictions = {sub_qs: format_answers(pred) for sub_qs, pred in predictions.items()}    
    
    
    grades = {}
    for permutation_string, answers in predictions.items(): 
        print(permutation_string)
        print(answers)
        total_correct = 0
        total_subquestions = len(answers)
        for i, (sub_q_idx, sub_q_answer) in enumerate(answers):
            print(f"i: {i} | sub_q_idx: {sub_q_idx} | sub_q_answer: {sub_q_answer} | ground truth: {answers_indexes[sub_q_idx]}")
            if sub_q_answer != answers_indexes[sub_q_idx]:
                print(f"Subquestion {sub_q_idx} is incorrect")
            else:
                print(f"Subquestion {sub_q_idx} is correct")
                total_correct += 1
        
        # Save the "grade"
        grades[permutation_string] = total_correct / total_subquestions
        print(total_correct / total_subquestions)

if __name__ == "__main__":
    count_results(prob_number = 1)