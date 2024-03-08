import itertools

def create_queries(idxs, contents):

    # Find permutations of the indexes
    all_permutations = [list(itertools.permutations(idxs, length)) for length in range(1, len(idxs) + 1)] # Contains sublists of permutations at a specific length

    # Flatten to 1D list containg all permutations of indexes
    flattened_permutations = [comb for sublist in all_permutations for comb in sublist]
    print(flattened_permutations)
    print(f"Num permutations: {len(flattened_permutations)}")

    # Create queries
    answer_guidance_text = "\n\nPlease leave your response in the following format (json format), where the keys are the sub-question number and corresponding value is your answer. An example for a question with subquestions 1, 2, and 3 is as follows: {1: 16, 2: 6, 3: 25}, where '16', '6' and '25' represent your answers to each sub-question. Do not explain your answers. Your answers should be in numerical format, with no text. Responses that do not adhere to these rules will be marked as incorrect.\n"
    print(answer_guidance_text)
    queries = [contents[0] + ("".join(contents[idx] for idx in flattened_permutations[i])) + answer_guidance_text for i in range(len(flattened_permutations))]

    # Return queries and indexes used
    return queries, flattened_permutations