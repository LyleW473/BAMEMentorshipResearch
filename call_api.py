import openai
from os import getenv
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
    create_prediction_mappings(prob_number = 1)


if __name__ == "__main__":
    main()