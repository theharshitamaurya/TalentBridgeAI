import os
from dotenv import load_dotenv

load_dotenv()

class Settings():

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    GROQ_API_URL= "https://api.groq.com/openai/v1/chat/completions"

    MODEL_NAME = "llama-3.1-8b-instant"
    
    TEMPERATURE = 0.9

    MAX_RETRIES = 3


settings = Settings()  


# from dotenv import load_dotenv
# import os

# load_dotenv()  # This loads the .env file into environment

# # Now ArtisanAssistant() will find the env variables
# assistant = ArtisanAssistant()
