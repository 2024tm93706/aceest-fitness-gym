import sqlite3

DB_NAME = "aceest_fitness.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # ---------- CLIENTS TABLE ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            age INTEGER,
            height REAL,
            weight REAL,
            program TEXT,
            calories INTEGER,
            target_weight REAL,
            target_adherence INTEGER
        )
    """)

    # ---------- PROGRESS TABLE ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            week TEXT,
            adherence INTEGER
        )
    """)

    # ---------- WORKOUTS TABLE ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            date TEXT,
            workout_type TEXT,
            duration_min INTEGER,
            notes TEXT
        )
    """)

    # ---------- EXERCISES TABLE ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_id INTEGER,
            name TEXT,
            sets INTEGER,
            reps INTEGER,
            weight REAL
        )
    """)

    # ---------- METRICS TABLE ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            date TEXT,
            weight REAL,
            waist REAL,
            bodyfat REAL
        )
    """)

    conn.commit()
    conn.close()

from flask import Flask, jsonify

app = Flask(__name__)

init_db()

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

@app.route("/progress/<name>")
def get_progress(name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT week, adherence
        FROM progress
        WHERE client_name=?
        ORDER BY id
    """, (name,))

    rows = cur.fetchall()
    conn.close()

    if not rows:
        return jsonify({"error": "No progress data"}), 404

    data = [
        {"week": r[0], "adherence": r[1]}
        for r in rows
    ]

    return jsonify({
        "client": name,
        "progress": data
    })

@app.route("/workouts", methods=["POST"])
def log_workout():
    from flask import request

    data = request.get_json()

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO workouts (client_name, date, workout_type, duration_min, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["date"],
        data["type"],
        data["duration"],
        data.get("notes", "")
    ))

    workout_id = cur.lastrowid

    if "exercise" in data:
        ex = data["exercise"]
        cur.execute("""
            INSERT INTO exercises (workout_id, name, sets, reps, weight)
            VALUES (?, ?, ?, ?, ?)
        """, (
            workout_id,
            ex["name"],
            ex["sets"],
            ex["reps"],
            ex["weight"]
        ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Workout logged"}), 201

@app.route("/metrics", methods=["POST"])
def log_metrics():
    from flask import request

    data = request.get_json()

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO metrics (client_name, date, weight, waist, bodyfat)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["date"],
        data.get("weight"),
        data.get("waist"),
        data.get("bodyfat")
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Metrics logged"}), 201

@app.route("/workouts/<name>")
def get_workouts(name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT date, workout_type, duration_min, notes
        FROM workouts
        WHERE client_name=?
        ORDER BY date DESC
    """, (name,))

    rows = cur.fetchall()
    conn.close()

    return jsonify([
        {
            "date": r[0],
            "type": r[1],
            "duration": r[2],
            "notes": r[3]
        }
        for r in rows
    ])

@app.route("/bmi/<name>")
def get_bmi(name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT height, weight FROM clients WHERE name=?", (name,))
    row = cur.fetchone()
    conn.close()

    if not row or not row[0] or not row[1]:
        return jsonify({"error": "Missing data"}), 400

    height_m = row[0] / 100
    bmi = round(row[1] / (height_m ** 2), 1)

    return jsonify({"bmi": bmi})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)