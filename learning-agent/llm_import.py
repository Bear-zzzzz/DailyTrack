from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:15731/v1",
    api_key="sk-synapse-proxy",
)

response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[
        {"role": "user", "content": "Hello!"}
    ],
)
print(response.choices[0].message.content)