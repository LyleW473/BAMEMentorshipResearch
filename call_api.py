import openai
from os import getenv

def main(query: str):
    API_TYPE = getenv("API_TYPE")
    ENDPOINT = getenv("ENDPOINT")
    API_VERSION = getenv("API_VERSION")
    API_KEY = getenv("API_KEY")

    openai.api_type = API_TYPE
    openai.azure_endpoint = ENDPOINT
    openai.api_version = API_VERSION
    openai.api_key = API_KEY

    # Read question
    with open("question1.txt") as q_file:
        contents = q_file.readlines()
        print(contents)

    # Construct permutations of question
    queries = []
    def recurse(current_i, current_query, subquestions_used):
        for i in range(current_i, len(contents)):
            if contents[i] not in subquestions_used:
                subquestions_used.add(contents[i])
                queries.append(current_query)
                recurse(
                        current_i = current_i + 1, 
                        current_query = current_query + contents[i],
                        subquestions_used = subquestions_used
                        )
                subquestions_used.remove(contents[i])

    recurse(
            current_i = 1, 
            current_query = contents[0],
            subquestions_used = set()
            )
    queries = queries[1:] # Remove the first question (as it contains no relevant information)
    for query in queries:
        print(query)

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
    print(completion.choices[0].message.content)

if __name__ == "__main__":
    main("What is 5 factorial (5!)?")