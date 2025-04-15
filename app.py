from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

# ✅ Set your Gemini API key
GOOGLE_API_KEY = "AIzaSyCMQm7XTKg5f-4N2M6fvFcoQ3E9NJSgenU"  # Replace with your actual API key

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing. Please provide a valid key.")

genai.configure(api_key=GOOGLE_API_KEY)

# ✅ Initialize generative model and chat history
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[
    {"role": "user", "parts": ["You're an AI car insurance advisor. Use the info below to answer."]},
    {"role": "user", "parts": ["Third-party insurance covers damage to others but not your car. Comprehensive covers both."]}
])


# ✅ Fixed __name__ typo here
app = Flask(__name__, template_folder="templates")

@app.route('/')
def index():
    print("Rendering index.html...")  # Debugging
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_response():
    data = request.json
    user_input = data.get('message')
    print(f"User input received: {user_input}")  # Debugging

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = chat.send_message(user_input).text
        print(f"Bot response: {response}")  # Debugging
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

# ✅ Fixed __name__ check here
if __name__ == '__main__':
    print("Starting Flask app on http://127.0.0.1:5000")
    app.run(debug=True)
