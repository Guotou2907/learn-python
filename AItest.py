import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("API_BASE_URL"),
)

resp = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[
        {"role": "user", "content": "你好，请用一句话介绍你自己"}
    ],
)

print(resp.choices[0].message.content)
