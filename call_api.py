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