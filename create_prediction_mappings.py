import json
from os.path import exists as os_path_exists
from os import mkdir
from create_queries import create_queries
import openai

def create_prediction_mappings(prob_number, make_uniform):

    # Set the path for the results
    results_path = "results/uniform" if make_uniform else "results"
    
    # Create folder for holding the json for results
    if not os_path_exists(results_path):
        mkdir(results_path)
    else:
        # Already generated predictions for this problem
        if os_path_exists(f"{results_path}/prob{prob_number}_predictions.json"):
            print(f"Already generated answers for problem {prob_number}")
            return

    # Read question
    with open(f"problems/problems/prob{prob_number}.txt") as p_file:
        contents = p_file.readlines()
        # print(contents)

    # Get queries based on the indexes and contents of the question
    idxs = [i for i in range(1, len(contents))]
    print(idxs)
    queries, indexes_used = create_queries(idxs = idxs, contents = contents, make_uniform = make_uniform)
    print(len(queries))
    for query in queries:
        print(query)
        print("----------------")

    # ----------------------------------------------
    # Generate answers to queries
    mappings = [] if make_uniform else {} # Maps the subquestions used (List of indexes) to the predictions generated by the LLM., uses list if making uniform, else uses hashmap

    for i, (query, idxs_used) in enumerate(zip(queries, indexes_used)):
        print(f"i: {i}\nQuery:\n{query}\nIndexes used:\n{idxs_used}\n")

        message_text = [{
                        "role": "system",
                        "content": "You are an AI assistant that helps people find information."
                        },
                        {
                        "role": "user",
                        "content": query
                        }]
        
        answer = (openai.chat.completions.create(
                                                model = "gpt-4",
                                                messages = message_text,
                                                temperature = 0.7,
                                                max_tokens = 800,
                                                top_p = 0.95,
                                                frequency_penalty = 0,
                                                presence_penalty = 0,
                                                stop = None,
                                                )).choices[0].message.content # Extract Python String
        
        # Create hashmap mapping
        indexes_string = "".join(str(idx) + "#" for idx in idxs_used) # Used because cannot have keys as tuple or list when using json.dump

        if make_uniform:
            mappings.append({indexes_string: answer})
        else:
            mappings[indexes_string] = answer
        
        # Save results
        with open(f"{results_path}/prob{prob_number}_predictions.json", "w") as file:
            json.dump(mappings, file)