from flask import Flask, render_template, request, jsonify
import sqlite3
import random

app = Flask(__name__)

# Function to create the database table (only runs once)
def create_table():
    conn = sqlite3.connect("spins.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS spin_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prize TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Call the function to ensure the table exists
create_table()

# Prize options
prizes = ["$1000", "$2000", "$5000", "$10000", "$50000"]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/spin', methods=['POST'])
def spin_wheel():
    prize = random.choice(prizes)  # Select a random prize

    # Store the prize in the database
    conn = sqlite3.connect("spins.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO spin_results (prize) VALUES (?)", (prize,))
    conn.commit()
    conn.close()

    # Retrieve last 5 spin results
    conn = sqlite3.connect("spins.db")
    cursor = conn.cursor()
    cursor.execute("SELECT prize, timestamp FROM spin_results ORDER BY id DESC LIMIT 5")
    last_spins = cursor.fetchall()
    conn.close()

    return jsonify({"prize": prize, "last_spins": last_spins})

if __name__ == '__main__':
    app.run(debug=True)
