import json
def count_results(prob_number):

    with open(f"problems/answers/prob{prob_number}_answers.txt", "r") as answers_file:
        answers = answers_file.readlines()

    answers = [answer.replace("\n", "") for answer in answers] # Clean answers
    answers_indexes = {i: answers[i] for i in range(1, len(answers))} # Indexes for each subquestion, skip the '#' operator
    print(answers_indexes)

    print(len(answers))
    print(answers)
    print(answers)

    with open(f"results/prob{prob_number}_predictions.json", "r") as predictions_file:
        predictions = json.load(predictions_file)

    print(predictions)
    for permutation_string, answer in predictions.items():
        pass
        



if __name__ == "__main__":
    count_results(prob_number = 1)