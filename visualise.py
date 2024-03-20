import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os
from count_results import count_results, count_uniform_results


def draw_bar_chart(data, title, xlabel, ylabel, labels_per_bar):
    keys = data.keys()
    values = data.values()

    # Define a colour map
    colours = cm.rainbow(np.linspace(0, 1, len(keys)))
    
    # Create bar chart
    bars = plt.bar(keys, values, color=colours)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Add text to each bar (representing the value)
    for i, bar in enumerate(bars):
        y_val = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, y_val, round(y_val, 2), va='bottom', ha='center') # The total grade for the each bar
        plt.text(bar.get_x() + bar.get_width()/2, y_val/2, labels_per_bar[i], va='center', ha='center') # Number of queries for each bar


    plt.show()
    

if __name__ == "__main__":
    for problem_number in range(1, len(os.listdir("problems/problems")) + 1):
        info_A = count_results(prob_number = problem_number)
        info_B = count_uniform_results(prob_number = problem_number)
        # Grades per length (non-uniform)
        total_per_length_A, total_sqs_per_length_A, grades_per_length_A, correct_per_length_A, num_incorrect_responses_A = info_A
        # draw_bar_chart(
        #                 data=grades_per_length_A, 
        #                 title=f"Grades per length for Problem {problem_number}", 
        #                 xlabel="No.of subquestions used", 
        #                 ylabel="Grade(%)", 
        #                 labels_per_bar=list(total_per_length_A.values())
        #                 )

        # # Grades per length (uniform)
        total_per_length_B, total_sqs_per_length_B, grades_per_length_B, correct_per_length_B, num_incorrect_responses_B = info_B
        # draw_bar_chart(
        #                 data=grades_per_length_B, 
        #                 title=f"Grades per length for Problem {problem_number} [Uniform]", 
        #                 xlabel="No.of subquestions used", 
        #                 ylabel="Grade(%)", 
        #                 labels_per_bar=list(total_per_length_B.values())
        #                 )
        # print(grades_per_length_A)
        # print(total_per_length_A)
        # print(num_incorrect_responses_A)
        
        # print(grades_per_length_B)
        # print(total_per_length_B)
        # print(num_incorrect_responses_B)
        
        # Total number of incorrectly answered queries
        total_subquestions = sum(total_sqs_per_length_A.values())
        total_correctly_answered_subqs = sum(correct_per_length_A.values())
        print(total_subquestions, total_correctly_answered_subqs)
        draw_bar_chart(
                    data={1: total_correctly_answered_subqs, 2: sum(total_sqs_per_length_A.values())},
                    title=f"Number of subquestions correct for Problem {problem_number}", 
                    xlabel="Correct/Incorrect", 
                    ylabel="Num of subquestions", 
                    labels_per_bar=["Correct", "Incorrect"]
                    )
        
        # Total number of incorrectly answered queries
        total_subquestions = sum(total_sqs_per_length_B.values())
        total_correctly_answered_subqs = sum(correct_per_length_B.values())
        print(total_subquestions, total_correctly_answered_subqs)
        draw_bar_chart(
                    data={1: total_correctly_answered_subqs, 2: sum(total_sqs_per_length_B.values())},
                    title=f"Number of subquestions correct for Problem {problem_number}", 
                    xlabel="Correct/Incorrect", 
                    ylabel="Num of subquestions", 
                    labels_per_bar=["Correct", "Incorrect"]
                    )
