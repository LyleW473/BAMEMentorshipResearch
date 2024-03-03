import openai
from os import getenv
from os import listdir
from create_prediction_mappings import create_prediction_mappings

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

    # Create prediction mappings for the problem number
    for problem_number in range(1, len(listdir("problems")) + 1):
        create_prediction_mappings(prob_number = problem_number)


if __name__ == "__main__":
    main()