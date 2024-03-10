import itertools
import math

def create_queries(idxs, contents, make_uniform):

    # Find permutations of the indexes
    all_permutations = [list(itertools.permutations(idxs, length)) for length in range(1, len(idxs) + 1)] # Contains sublists of permutations at a specific length

    # Make distribution of queries with n, n+1, n+2 and so on subquestions uniform
    if make_uniform == True:
        total_per_length = [len(sublist) for sublist in all_permutations]
        print(total_per_length)
        lcm = math.lcm(*total_per_length)
        print(lcm)
        all_permutations = [sublist * (lcm // len(sublist)) for sublist in all_permutations] # Repeat the list multiple times until there are lcm permutations of length n
        print(all_permutations[1][25:35])
        print([len(a) for a in all_permutations])

        # print(math.lcm(*[length for length in total_per_length.values()]))
        # lcm = math.lcm(*[length for length in total_per_length.values()])
        # num_repeats = [sublist * (lcm) for sublist in all_permutations]
        # print(total_per_length)
        # print()

    # Flatten to 1D list containg all permutations of indexes
    flattened_permutations = [comb for sublist in all_permutations for comb in sorted(sublist)]
    print(len([perm for perm in flattened_permutations if len(perm) == 6]))
    print(flattened_permutations)
    print(f"Num permutations: {len(flattened_permutations)}")

    # Create queries
    answer_guidance_text = "\n\nPlease leave your response in the following format (json format), where the keys are the sub-question number and corresponding value is your answer. An example for a question with subquestions 1, 2, and 3 is as follows: {1: 16, 2: 6, 3: 25}, where '16', '6' and '25' represent your answers to each sub-question. Do not explain your answers. Your answers should be in numerical format, with no text. Responses that do not adhere to these rules will be marked as incorrect.\n"
    print(answer_guidance_text)
    queries = [contents[0] + ("".join(contents[idx] for idx in flattened_permutations[i])) + answer_guidance_text for i in range(len(flattened_permutations))]

    # Return queries and indexes used
    return queries, flattened_permutations