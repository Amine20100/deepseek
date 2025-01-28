from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    expiry_date = data['expiry_date']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, expiry_date) VALUES (?, ?, ?)', 
                   (username, password, expiry_date))
    conn.commit()
    conn.close()
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                   (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        expiry_date = datetime.strptime(user[3], '%Y-%m-%d')
        if expiry_date > datetime.now():
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"message": "Account expired!"}), 403
    else:
        return jsonify({"message": "Invalid credentials!"}), 401

if __name__ == '__main__':
    app.run(debug=True)
