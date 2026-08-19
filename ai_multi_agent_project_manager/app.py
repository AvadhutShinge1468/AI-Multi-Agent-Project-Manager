from flask import Flask, render_template, request, jsonify
from agents import ProjectManager

app = Flask(__name__)
manager = ProjectManager()

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/api/analyze")
def analyze():
    data = request.get_json(silent=True) or {}
    description = (data.get("description") or "").strip()
    if not description:
        return jsonify({"error": "Please enter a project description."}), 400

    result = manager.run(description)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
