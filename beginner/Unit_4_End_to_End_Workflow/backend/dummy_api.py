from flask import Flask, jsonify

app = Flask(__name__)

students_db = [
    {"id": 1, "name": "John Doe", "course": "BCA", "status": "Active"},
    {"id": 2, "name": "Jane Smith", "course": "BBA", "status": "Graduated"},
    {"id": 3, "name": "Sam Wilson", "course": "BSc IT", "status": "Active"}
]

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the College System Backend API"})

@app.route("/api/students", methods=["GET"])
def get_students():
    return jsonify(students_db)

if __name__ == "__main__":
    app.run(port=8000, debug=True)
