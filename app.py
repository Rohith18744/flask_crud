from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL)''')
    conn.commit()
    conn.close()

def run_query(query, params=(), fetch=False):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(query, params)
    data = None
    if fetch:
        data = c.fetchall()
    conn.commit()
    conn.close()
    return data

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    run_query("INSERT INTO users (name, email) VALUES (?, ?)", (data['name'], data['email']))
    return jsonify({"message": "User created successfully"}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = run_query("SELECT * FROM users", fetch=True)
    return jsonify([{"id": u[0], "name": u[1], "email": u[2]} for u in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = run_query("SELECT * FROM users WHERE id = ?", (user_id,), fetch=True)
    if not user:
        return jsonify({"error": "User not found"}), 404
    u = user[0]
    return jsonify({"id": u[0], "name": u[1], "email": u[2]})

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    run_query("UPDATE users SET name = ?, email = ? WHERE id = ?", (data['name'], data['email'], user_id))
    return jsonify({"message": "User updated successfully"})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    run_query("DELETE FROM users WHERE id = ?", (user_id,))
    return jsonify({"message": "User deleted successfully"})


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
