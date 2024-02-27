import openai
from os import getenv

def main():
    # Initialise API
    API_TYPE = getenv("API_TYPE")
    ENDPOINT = getenv("ENDPOINT")
    API_VERSION = getenv("API_VERSION")
    API_KEY = getenv("API_KEY")

    openai.api_type = API_TYPE
    openai.azure_endpoint = ENDPOINT
    openai.api_version = API_VERSION
    openai.api_key = API_KEY

    # Read question
    with open("prob1.txt") as p_file:
        contents = p_file.readlines()
        print(contents)

    # Construct permutations of question
    queries = []
    all_answers_idxs = []
    def recurse(current_i, current_query, subquestions_used_idxs):
        for i in range(current_i, len(contents)):
            if i not in subquestions_used_idxs:
                subquestions_used_idxs.add(i)
                all_answers_idxs.append([idx for idx in subquestions_used_idxs])
                queries.append(current_query)
                recurse(
                        current_i = current_i + 1, 
                        current_query = current_query + contents[i],
                        subquestions_used_idxs = subquestions_used_idxs
                        )
                subquestions_used_idxs.remove(i)
    recurse(
            current_i = 1, 
            current_query = contents[0],
            subquestions_used_idxs = set()
            )
    queries = queries[1:] # Remove the first question (as it contains no relevant information)
    # for query in queries:
    #     print(query)

    # Generate answers to queries
    answers = []
    print("start")
    for i, (query, idxs_used) in enumerate(zip(queries, all_answers_idxs)):
        print(i, query, idxs_used)
        message_text = [{
                        "role": "system",
                        "content": "You are an AI assistant that helps people find information."
                        },
                        {
                        "role": "user",
                        "content": query
                        }]
        
        completion = openai.chat.completions.create(
                                                    model = "gpt-4",
                                                    messages = message_text,
                                                    temperature = 0.7,
                                                    max_tokens = 800,
                                                    top_p = 0.95,
                                                    frequency_penalty = 0,
                                                    presence_penalty = 0,
                                                    stop = None,
                                                    )
        answers.append(completion.choices[0].message.content)
        print(answers[i])
    
    print("end")

    for answer in answers:
        print(answer)

if __name__ == "__main__":
    main()