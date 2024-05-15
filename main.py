from dotenv import load_dotenv
from openai import OpenAI
import os

# Load the API key from the .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

# Define placeholder values
topic = "sports"
mood = "concise"

# Multi-line comment with placeholders
system_role = f"""
You are an expert on {topic}.
You write in a {mood} way.
Only write about your expert topic.
Three bullet points, short full sentence for each
"""

# print(system_role)
# exit()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_role},
        {"role": "user", "content": "What were the most important events in Germany in 1989 in your topic?"}
    ]
)

print(response.choices[0].message.content)
