import json
def count_results(prob_number):

        with open(f"problems/answers/prob{prob_number}_answers.txt", "r") as answers_file:
            answers = answers_file.readlines()
            

        print(len(answers))
        print(answers)
        answers = [answer.replace("\n", "") for answer in answers]
        print(answers)

        with open(f"results/prob{prob_number}_predictions.json", "r") as predictions_file:
            predictions = json.load(predictions_file)
        
        print(predictions)



if __name__ == "__main__":
    count_results(prob_number = 1)