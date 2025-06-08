import os
import openai
import json

# Set your API Key and Organization ID
# Key redacted for privacy
openai.api_key = 'example3'
openai.organization = 'example4'

def ask_gpt3(query):
    # Create a series of messages
    messages = [
        {"role": "system", "content": "You first respond to a user by categorizing their input into the bracket of journalling, therapy, essay writing, or planning for the future. You then summarize their input back to them, followed by pointing out something interesting within their response which you want to explore further."},
        {"role": "user", "content": query}
    ]

    # Request the model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000  # control the length of the result
    )

    # Extract the assistant's reply from the response
    assistant_reply = response['choices'][0]['message']['content']

    # Print out the reply
    print(f"Assistant: {assistant_reply}")


def main():
    while True:
        user_input = input("What would you like to talk about?")
        if user_input.lower() == "quit":
            break
        ask_gpt3(user_input)


if __name__ == "__main__":
    main()
