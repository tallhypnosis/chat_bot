from flask import Flask, render_template, request, jsonify
from openai import OpenAI, RateLimitError
import os
from dotenv import load_dotenv
import time

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Set up OpenAI API credentials
client = OpenAI(api_key=os.environ.get('OPEN_AI_KEY'))

# Define the default route to return the index
@app.route("/")
def index():
    return render_template("index.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    # Get the message from POST request
    message = request.json.get("message")

    # Define initial values for backoff and retry
    wait_time = 0.1
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            # Send the message to OpenAI's API and receive the response
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": message}],
                model="gpt-3.5-turbo"
            )

            # Return JSON response containing the completion
            if completion.choices and completion.choices[0].message:
                return jsonify(completion.choices[0].message)
            else:
                return jsonify({'error': 'Failed to generate response!'})

        except RateLimitError as e:
            # Rate limit error, retry after exponential backoff
            wait_time *= 2
            retries += 1
            time.sleep(wait_time)
            continue

    return jsonify({'error': 'Exceeded maximum number of retries!'})

if __name__ == '__main__':
    app.run()
