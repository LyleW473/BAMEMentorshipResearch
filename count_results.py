import json
import re

def contains_letters(string):
    return any(char.isalpha() or char == "+" or char == "-" for char in string)

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

    # Count the results
    correct_per_length = {} # Number of correctly answered subquestions at where the questions contains 1, 2, 3 and so on subquestions
    total_per_length = {} # Number of questions with 1, 2, 3, and so on subquestions
    for permutation_string, ans in predictions.items(): 
        print(permutation_string)
        print(ans)

        total_subquestions = len(ans)
        total_per_length[total_subquestions] = total_per_length.get(total_subquestions, 0) + 1 # Increment the number of total questions that have n subquestions

        num_sqs_correct = 0
        for i, (sub_q_idx, sub_q_answer) in enumerate(ans):
            print(f"i: {i} | sub_q_idx: {sub_q_idx} | sub_q_answer: {sub_q_answer} | ground truth: {answers_indexes[sub_q_idx]}")
            if sub_q_answer != answers_indexes[sub_q_idx]:
                print(f"Subquestion {sub_q_idx} is incorrect")
            else:
                print(f"Subquestion {sub_q_idx} is correct")
                num_sqs_correct += 1

        correct_per_length[total_subquestions] =  correct_per_length.get(total_subquestions, 0) + num_sqs_correct # Increment the number of total correctly answered subquestions at this length n
         
    
    print(total_per_length)
    print(sum(total_per_length.values()) == num_responses - num_incorrect_responses)
    total_sqs_per_length = {length: total_per_length[length] * length for length in total_per_length.keys()} # The total number of subquestions in a query with n subquestions
    print(total_sqs_per_length)
    print(correct_per_length)
    grades_per_length = {total_questions_with_n_sqs: (num_correct / total_sqs) * 100 for num_correct, (total_questions_with_n_sqs, total_sqs) in zip(correct_per_length.values(), total_sqs_per_length.items())}
    print(grades_per_length)
    
    total_correct_subqs = sum(correct_per_length.values())
    total_subquestions = sum(total_per_length.values())
    avg_grade = total_correct_subqs / total_subquestions
    print(avg_grade)

def count_uniform_results(prob_number):
    with open(f"problems/answers/prob{prob_number}_answers.txt", "r") as answers_file:
        answers = answers_file.readlines()

    answers = [answer.replace("\n", "") for answer in answers] # Clean answers
    answers_indexes = {str(i): str(answers[i]) for i in range(1, len(answers))} # Indexes for each subquestion, skip the '#' operator
    print(answers_indexes)
    print(len(answers))

    with open(f"results/uniform/prob{prob_number}_predictions.json", "r") as predictions_file:
        predictions = json.load(predictions_file)
    

    # Filter and calculate the number of incorrect responses
    num_responses = len(predictions)
    preds = []
    for pred_dict in predictions:
        for sub_qs, pred in pred_dict.items():
            if not contains_letters(pred):
                preds.append({sub_qs: pred})
    num_incorrect_responses = num_responses - len(preds)
    predictions = preds
    print(num_incorrect_responses, len(predictions))

    # Format answers so that they can be counted
    predictions = [{sub_qs: format_answers(pred) for sub_qs, pred in pred_dict.items()} for pred_dict in predictions]
    print(len(predictions), predictions[1]["1#"])
    
    # Count results
    correct_per_length = {}
    total_per_length = {}
    num_sub_correct = 0
    num_sub_qs = 0
    for pred_dict in predictions:
        for permutation_string, ans in pred_dict.items(): 
            print(pred_dict, permutation_string, ans)

            total_subquestions = len(ans)
            total_per_length[total_subquestions] = total_per_length.get(total_subquestions, 0) + 1 # Increment the number of total questions that have n subquestions

            num_sqs_correct = 0
            for i, (sub_q_idx, sub_q_answer) in enumerate(ans):
                num_sub_qs += 1
                print(f"i: {i} | sub_q_idx: {sub_q_idx} | sub_q_answer: {sub_q_answer} | ground truth: {answers_indexes[sub_q_idx]}")
                if sub_q_answer != answers_indexes[sub_q_idx]:
                    print(f"Subquestion {sub_q_idx} is incorrect")
                else:
                    print(f"Subquestion {sub_q_idx} is correct")
                    num_sqs_correct += 1
                    num_sub_correct += 1

            correct_per_length[total_subquestions] =  correct_per_length.get(total_subquestions, 0) + num_sqs_correct # Increment the number of total correctly answered subquestions at this length n

    print("total correct:", num_sub_correct, num_sub_qs)
    print("total per length", total_per_length)
    print(sum(total_per_length.values()) == num_responses - num_incorrect_responses)
    total_sqs_per_length = {length: total_per_length[length] * length for length in total_per_length.keys()} # The total number of subquestions in a query with n subquestions
    print(total_sqs_per_length)
    print(correct_per_length)
    grades_per_length = {total_questions_with_n_sqs: (num_correct / total_sqs) * 100 for num_correct, (total_questions_with_n_sqs, total_sqs) in zip(correct_per_length.values(), total_sqs_per_length.items())}
    print(grades_per_length)
    
    total_correct_subqs = sum(correct_per_length.values())
    total_subquestions = sum(total_per_length.values())
    avg_grade = total_correct_subqs / total_subquestions
    print(avg_grade)

if __name__ == "__main__":
    # count_results(prob_number = 1)
    count_uniform_results(prob_number = 1)