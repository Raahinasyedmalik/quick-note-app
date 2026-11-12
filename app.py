from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Database Setup
def init_db():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/notes', methods=['GET'])
def get_notes():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM notes')
    notes = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(notes)

@app.route('/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    note_content = data.get('content')
    if note_content:
        conn = sqlite3.connect('notes.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes (content) VALUES (?)', (note_content,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Note added successfully!'}), 201
    return jsonify({'error': 'Content is empty'}), 400

if __name__ == '__main__':
    app.run(debug=True)