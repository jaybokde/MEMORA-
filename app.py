from flask import Flask, render_template, request, jsonify

from ai import analyze_input, generate_response
from tools import process_ai_result


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/capture")
def capture():
    return render_template("capture.html")


@app.route("/memory")
def memory():
    return render_template("memory.html")

@app.route("/ask")
def ask():
    return render_template("ask.html")


@app.route("/api/capture", methods=["POST"])
def api_capture():

    data = request.get_json()

    user_text = data.get("text", "").strip()

    if not user_text:
        return jsonify({
            "success": False,
            "error": "Please enter something."
        }), 400

    try:

        # Ask NVIDIA to understand the user's message
        result = analyze_input(user_text)

        # Save extracted information
        saved = process_ai_result(result)

        # Generate MEMORA's friendly response
        message = generate_response(result)

        return jsonify({
            "success": True,
            "message": message,
            "result": result,
            "saved": saved
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


@app.route("/api/memory")
def api_memory():

    try:

        from database import (
            get_memories,
            get_tasks,
            get_events
        )

        user_id = "jay"

        return jsonify({
            "success": True,
            "tasks": get_tasks(user_id),
            "events": get_events(user_id),
            "memories": get_memories(user_id)
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)