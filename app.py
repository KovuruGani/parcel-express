from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)


def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS parcels(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        receiver TEXT,
        pickup TEXT,
        delivery TEXT,
        weight REAL,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return "Online Parcel Booking Backend Running Successfully!"

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (data["name"], data["email"], data["password"])
        )
        conn.commit()
        return jsonify({"message": "Registration Successful"})
    except sqlite3.IntegrityError:
        return jsonify({"message": "Email already exists"})
    finally:
        conn.close()
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (data["email"], data["password"])
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login Successful"})
    else:
        return jsonify({"message": "Invalid Email or Password"})
@app.route("/book", methods=["POST"])
def book():

    data = request.get_json()

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO parcels
        (sender,receiver,pickup,delivery,weight,status)
        VALUES(?,?,?,?,?,?)
        """,
        (
            data["sender"],
            data["receiver"],
            data["pickup"],
            data["delivery"],
            data["weight"],
            "Booked"
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"message":"Parcel Booked Successfully"})
@app.route("/track/<int:id>", methods=["GET"])
def track(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT status FROM parcels WHERE id=?",
        (id,)
    )

    parcel = cursor.fetchone()

    conn.close()

    if parcel:
        return jsonify({"status": parcel[0]})
    else:
        return jsonify({"message": "Parcel Not Found"})
@app.route("/parcels", methods=["GET"])
def get_parcels():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM parcels")
    parcels = cursor.fetchall()

    conn.close()

    return jsonify([dict(row) for row in parcels])
conn=sqlite3.connect("database.db")
cursor=conn.cursor()
cursor.execute("UPDATE parcels SET status='In Transit' WHERE id=2")
cursor.execute("UPDATE parcels SET status='Delivered' WHERE id=3")
conn.commit()
conn.close()
    
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
