from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)
API_KEY = os.environ.get('API_KEY')
API_URL = 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=['POST'])
def get_bot_response_route():
    user_data = request.get_json()
    user_text = user_data.get('msg')
    
    if not user_text:
        return jsonify({"error": "No message provided"}), 400
    
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "inputs": user_text
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status() 
        
        bot_response_data = response.json()
        
        if bot_response_data and isinstance(bot_response_data, list) and 'generated_text' in bot_response_data[0]:
            bot_text = bot_response_data[0]['generated_text']
            return jsonify({"response": bot_text})
        else:
            return jsonify({"error": "Invalid API response"}), 500
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)