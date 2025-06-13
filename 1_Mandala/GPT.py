from flask import Flask, request, jsonify
import openai
import json

app = Flask(__name__)

@app.route('/api/ask', methods=['POST'])
def ask_gpt3():
    # Get the text from the request's JSON
    text = request.get_json().get('text')

    # Set your API Key and Organization ID
    #Real key redacted for privacy
    openai.api_key = 'example1'
    openai.organization = 'example2'

    # Create a series of messages
    messages = [
        {"role": "system", "content": "You categorize user input and base your response on that category. If the user inputs something like a journal entry or problem, you analyze it, summarize it, and then inquire about one interesting thing in it. If the user is talking about their future, you help them generate plans for the future. If the user is talking about personality, you talk about the big five model of personality and connect their input with that model."},
        {"role": "user", "content": text}
    ]

    # Request the model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000  # control the length of the result
    )

    # Extract the assistant's reply from the response
    assistant_reply = response['choices'][0]['message']['content']

    # Return the reply
    return jsonify({"assistant": assistant_reply})

@app.route('/api/askForTitle', methods=['POST'])
def ask_gpt3_for_title():
    # Get the text from the request's JSON
    text2 = request.get_json().get('text2')

    # Set your API Key and Organization ID
    openai.api_key = 'example1'
    openai.organization = 'example2'

    # Create a series of messages
    messages = [
        {"role": "system", "content": "you take user input and return a 3 word output summarizing it, or you just say error"},
        {"role": "user", "content": text2}
    ]

    # Request the model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100  # control the length of the result
    )

    # Extract the assistant's reply from the response
    assistant_reply = response['choices'][0]['message']['content']

    # Return the reply
    return jsonify({"assistant": assistant_reply})

if __name__ == "__main__":
    app.run(port=5001)  # run the Flask app on port 5001
