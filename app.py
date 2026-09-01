from flask import Flask, request, jsonify

app = Flask(__name__)


def predict_score(study_hours, quiz, assignment, attendance, gpa):
    score = (
        0.15 * study_hours * 10 +
        0.30 * quiz +
        0.25 * assignment +
        0.20 * attendance +
        0.10 * (gpa * 25)
    )
    return round(min(score, 100), 1)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    required = ["study_hours", "quiz", "assignment", "attendance", "gpa"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    try:
        study = float(data["study_hours"])
        quiz = float(data["quiz"])
        assignment = float(data["assignment"])
        attendance = float(data["attendance"])
        gpa = float(data["gpa"])
    except (TypeError, ValueError):
        return jsonify({"error": "All fields must be numeric"}), 400

    result = predict_score(study, quiz, assignment, attendance, gpa)
    cognitive = round((quiz + assignment + attendance) / 3 * 1.2)

    return jsonify({
        "predicted_score": result,
        "cognitive_index": cognitive
    })


if __name__ == "__main__":
    app.run(debug=True)
