import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os
from count_results import count_results, count_uniform_results


def draw_bar_chart(data, title, xlabel, ylabel):
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
    for bar in bars:
        y_val = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, y_val, round(y_val, 2), va='bottom', ha='center') # Center text
    
    plt.show()
    

if __name__ == "__main__":
    for problem_number in range(1, len(os.listdir("problems/problems")) + 1):
        info_a = count_results(prob_number = problem_number)
        info_b = count_uniform_results(prob_number = problem_number)
        print("A", info_a)
        print()
        print("B", info_b)

        # Grades per length (non-uniform)
        total_per_length, total_sqs_per_length, grades_per_length, num_incorrect_responses = info_a
        draw_bar_chart(grades_per_length, title=f"Grades per length for Problem {problem_number}", xlabel="No.of subquestions used", ylabel="Grade(%)")

        # Grades per length (uniform)
        total_per_length, total_sqs_per_length, grades_per_length, num_incorrect_responses = info_b
        draw_bar_chart(grades_per_length, title=f"Grades per length for Problem {problem_number} [Uniform]", xlabel="No.of subquestions used", ylabel="Grade(%)")

