from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "smartvet-secret-key-change-this-later"

# -----------------------------
# Groq AI Setup
# -----------------------------

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

GROQ_SYSTEM_INSTRUCTION = (
    "তুমি SmartVet BD-এর একজন সহায়ক AI অ্যাসিস্ট্যান্ট। "
    "তুমি বাংলাদেশের কৃষকদের গরু, ছাগল, মুরগি, হাঁস, কুকুর, বিড়াল, কবুতর, মাছ ও খরগোশের "
    "স্বাস্থ্য সমস্যা বুঝতে সাহায্য করো। "
    "কৃষক তার প্রশ্ন বাংলা হরফে, বাংলিশ (যেমন 'amar gorur jor hoise'), অথবা ইংরেজিতে লিখতে পারে — "
    "তুমি সবক্ষেত্রেই ইনপুট বুঝবে। "
    "কিন্তু তোমার উত্তর সবসময় শুধুমাত্র বাংলা হরফে দেবে, ইংরেজি অক্ষরে (বাংলিশ) কখনো উত্তর দেবে না। "
    "সবসময় সহজ, সংক্ষিপ্ত বাংলা ভাষায় উত্তর দাও। "
    "কৃষক লক্ষণ বললে, সম্ভাব্য রোগ ও প্রাথমিক করণীয় বলো। "
    "কিন্তু প্রতিটি উত্তরের শেষে অবশ্যই স্পষ্টভাবে বলো যে এটি চূড়ান্ত ডায়াগনোসিস নয় এবং "
    "গুরুতর অবস্থায় দ্রুত পশুচিকিৎসকের পরামর্শ নেওয়া জরুরি। "
    "তুমি কখনো নির্দিষ্ট ওষুধের ডোজ বলবে না।"
)

# -----------------------------
# Flask-Login Setup
# -----------------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect("database/smartvet.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return User(row[0], row[1], row[2])
    return None


# -----------------------------
# Pages
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user_name=current_user.name)


@app.route("/animal/<animal_name>")
@login_required
def animal(animal_name):
    return render_template(
        "animal.html",
        animal=animal_name.capitalize()
    )


@app.route("/ai-chat")
@login_required
def ai_chat_page():
    return render_template("ai_chat.html")


@app.route("/emergency")
@login_required
def emergency_page():
    return render_template("emergency.html")


@app.route("/history")
@login_required
def history_page():

    conn = sqlite3.connect("database/smartvet.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT animal, symptoms, disease, search_date
        FROM history
        WHERE user_id = ?
        ORDER BY search_date DESC
    """, (current_user.id,))

    records = cursor.fetchall()
    conn.close()

    return render_template("history.html", records=records)


# -----------------------------
# Register
# -----------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not name or not email or not password:
        return render_template("register.html", error="সব ঘর পূরণ করুন।")

    hashed_password = generate_password_hash(password)

    conn = sqlite3.connect("database/smartvet.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed_password)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return render_template("register.html", error="এই ইমেইল দিয়ে আগেই অ্যাকাউন্ট আছে।")

    conn.close()

    return redirect(url_for("login"))


# -----------------------------
# Login
# -----------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    conn = sqlite3.connect("database/smartvet.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, password FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()

    if row and check_password_hash(row[3], password):
        user = User(row[0], row[1], row[2])
        login_user(user)
        return redirect(url_for("dashboard"))

    return render_template("login.html", error="ইমেইল বা পাসওয়ার্ড ভুল হয়েছে।")


# -----------------------------
# Logout
# -----------------------------

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


# -----------------------------
# Disease Search API
# -----------------------------

@app.route("/search_disease", methods=["POST"])
@login_required
def search_disease():

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "No data received."
        })

    animal = data.get("animal")
    selected_symptoms = data.get("symptoms", [])

    conn = sqlite3.connect("database/smartvet.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT disease_name, symptom, description, treatment
        FROM diseases
        WHERE animal = ?
    """, (animal,))

    diseases = cursor.fetchall()

    results = []

    for disease in diseases:

        disease_name = disease[0]
        db_symptoms = [x.strip() for x in disease[1].split(",")]
        description = disease[2]
        treatment = disease[3]

        matched = 0

        for symptom in selected_symptoms:
            if symptom in db_symptoms:
                matched += 1

        if matched > 0:

            percentage = round((matched / len(db_symptoms)) * 100)

            results.append({
                "disease": disease_name,
                "description": description,
                "treatment": treatment,
                "match": percentage
            })

    results.sort(key=lambda x: x["match"], reverse=True)

    top_results = results[:3]

    if len(top_results) > 0:
        top_disease_name = top_results[0]["disease"]
    else:
        top_disease_name = "কোনো মিল পাওয়া যায়নি"

    cursor.execute("""
        INSERT INTO history (user_id, animal, symptoms, disease)
        VALUES (?, ?, ?, ?)
    """, (current_user.id, animal, ", ".join(selected_symptoms), top_disease_name))

    conn.commit()
    conn.close()

    if len(top_results) == 0:
        return jsonify({
            "status": "not_found"
        })

    return jsonify({
        "status": "success",
        "results": top_results
    })


# -----------------------------
# AI Chat API
# -----------------------------

@app.route("/ai_chat_api", methods=["POST"])
@login_required
def ai_chat_api():

    data = request.get_json()

    if not data or not data.get("message"):
        return jsonify({
            "status": "error",
            "message": "No message received."
        })

    user_message = data.get("message")

    try:
        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": GROQ_SYSTEM_INSTRUCTION},
                {"role": "user", "content": user_message}
            ]
        )
        reply_text = response.choices[0].message.content
    except Exception as e:
        print("GROQ ERROR:", e)
        return jsonify({
            "status": "error",
            "message": "AI থেকে উত্তর পাওয়া যায়নি। একটু পরে আবার চেষ্টা করুন।"
        })

    return jsonify({
        "status": "success",
        "reply": reply_text
    })


# -----------------------------
# Run App
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)