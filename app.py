
from flask import Flask, request, jsonify

app = Flask(__name__)

expenses = []
next_id = 1


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Expense Tracker API",
        "status": "success"
    }), 200


@app.route("/expenses", methods=["GET"])
def get_expenses():
    total = sum(expense["amount"] for expense in expenses)

    return jsonify({
        "expenses": expenses,
        "total": round(total, 2)
    }), 200


@app.route("/expenses", methods=["POST"])
def add_expense():
    global next_id

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    title = data.get("title")
    amount = data.get("amount")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "A valid title is required"}), 400

    if isinstance(amount, bool):
        return jsonify({"error": "Amount must be a positive number"}), 400

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({"error": "Amount must be a positive number"}), 400

    if amount <= 0 or not amount < float("inf"):
        return jsonify({"error": "Amount must be a positive number"}), 400

    expense = {
        "id": next_id,
        "title": title.strip(),
        "amount": round(amount, 2)
    }

    expenses.append(expense)
    next_id += 1

    return jsonify(expense), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
