import os
from dotenv import find_dotenv, load_dotenv
from openai import AzureOpenAI

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

client = AzureOpenAI(azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
api_key=os.getenv("AZURE_OPENAI_API_KEY"),
api_version="2023-12-01-preview")

def messages_ai(system_message, user_message):

    response = client.chat.completions.create(model="story-gen",
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ])
    return response.choices[0].message.content