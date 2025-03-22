# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
from routes import submit_form, get_card_data

app = Flask(__name__)
CORS(app)

app.register_blueprint(submit_form.api_submit_form)
app.register_blueprint(get_card_data.api_card_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5001)
