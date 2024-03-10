import json

def contains_letters(string):
    return any(char.isalpha() for char in string)

def clean_string(string):
    # Only keeps relevant characters
    return "".join(char for char in string if char.isdigit() or char == ":" or char == ",")

def format_answers(string):
    qs_map_answers = clean_string(string).split(",")
    return [sub_q_answer.split(":") for sub_q_answer in qs_map_answers]

def count_results(prob_number):

    with open(f"problems/answers/prob{prob_number}_answers.txt", "r") as answers_file:
        answers = answers_file.readlines()

    answers = [answer.replace("\n", "") for answer in answers] # Clean answers
    answers_indexes = {i: answers[i] for i in range(1, len(answers))} # Indexes for each subquestion, skip the '#' operator
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

    for permutation_string, answer in predictions.items():
        print(permutation_string)
        print(answer)
        
if __name__ == "__main__":
    count_results(prob_number = 1)