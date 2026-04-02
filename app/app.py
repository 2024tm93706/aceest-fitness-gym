import sqlite3

DB_NAME = "aceest_fitness.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            age INTEGER,
            weight REAL,
            program TEXT,
            calories INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            week TEXT,
            adherence INTEGER
        )
    """)

    conn.commit()
    conn.close()

init_db()

from flask import Flask, jsonify

app = Flask(__name__)

programs = {
    "fat-loss": {
        "name": "Fat Loss (FL)",
        "workout": """Mon: 5x5 Back Squat + AMRAP
Tue: EMOM 20min Assault Bike
Wed: Bench Press + 21-15-9
Thu: 10RFT Deadlifts/Box Jumps
Fri: 30min Active Recovery""",
        "diet": """B: 3 Egg Whites + Oats Idli
L: Grilled Chicken + Brown Rice
D: Fish Curry + Millet Roti
Target: 2,000 kcal""",
        "color": "#e74c3c",
        "calorie_factor": 22,
        "factor": 22
    },
    "muscle-gain": {
        "name": "Muscle Gain (MG)",
        "workout": """Mon: Squat 5x5
Tue: Bench 5x5
Wed: Deadlift 4x6
Thu: Front Squat 4x8
Fri: Incline Press 4x10
Sat: Barbell Rows 4x10""",
        "diet": """B: 4 Eggs + PB Oats
L: Chicken Biryani (250g Chicken)
D: Mutton Curry + Jeera Rice
Target: 3,200 kcal""",
        "color": "#2ecc71",
        "calorie_factor": 35,
        "factor": 35
    },
    "beginner": {
        "name": "Beginner (BG)",
        "workout": """Circuit Training: Air Squats, Ring Rows, Push-ups
Focus: Technique Mastery & Form (90% Threshold)""",
        "diet": """Balanced Tamil Meals: Idli-Sambar, Rice-Dal, Chapati
Protein: 120g/day""",
        "color": "#3498db",
        "calorie_factor": 26,
        "factor": 26
    }
}

@app.route("/")
def home():
    return jsonify({"message": "ACEest Gym API running"})

@app.route("/programs")
def get_programs():
    return jsonify(programs)

@app.route("/programs/<program_id>")
def get_program(program_id):
    program = programs.get(program_id)
    if program:
        return jsonify(program)
    return jsonify({"error": "Program not found"}), 404

@app.route("/calculate-calories/<program_id>/<weight>")
def calculate_calories(program_id, weight):
    program = programs.get(program_id)

    if not program:
        return jsonify({"error": "Program not found"}), 404

    try:
        weight = float(weight)
    except:
        return jsonify({"error": "Invalid weight"}), 400

    calorie_factor = program.get("calorie_factor")

    if not calorie_factor:
        return jsonify({"error": "Calorie data not available"}), 400

    calories = int(weight * calorie_factor)

    return jsonify({
        "program": program["name"],
        "weight": weight,
        "estimated_calories": calories
    })

@app.route("/clients", methods=["POST"])
def save_client():
    from flask import request

    data = request.get_json()

    required = ["name", "age", "weight", "program"]

    for f in required:
        if f not in data:
            return jsonify({"error": f"{f} required"}), 400

    if data["program"] not in programs:
        return jsonify({"error": "Invalid program"}), 400

    calorie_factor = programs[data["program"]]["calorie_factor"]
    calories = int(data["weight"] * calorie_factor)

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO clients
        (name, age, weight, program, calories)
        VALUES (?, ?, ?, ?, ?)
    """, (data["name"], data["age"], data["weight"], data["program"], calories))

    conn.commit()
    conn.close()

    return jsonify({"message": "Client saved"}), 201

@app.route("/clients/<name>")
def load_client(name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT name, age, weight, program, calories FROM clients WHERE name=?", (name,))
    row = cur.fetchone()

    conn.close()

    if not row:
        return jsonify({"error": "Client not found"}), 404

    return jsonify({
        "name": row[0],
        "age": row[1],
        "weight": row[2],
        "program": row[3],
        "calories": row[4]
    })

@app.route("/progress", methods=["POST"])
def save_progress():
    from flask import request
    from datetime import datetime

    data = request.get_json()

    if "name" not in data or "adherence" not in data:
        return jsonify({"error": "Missing fields"}), 400

    week = datetime.now().strftime("Week %U - %Y")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO progress (client_name, week, adherence)
        VALUES (?, ?, ?)
    """, (data["name"], week, data["adherence"]))

    conn.commit()
    conn.close()

    return jsonify({"message": "Progress saved"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)