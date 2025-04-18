# app.py
from flask import Flask, request, send_file
from tools import agent, dataSaver, scriptToVideo
import os

app = Flask(__name__, static_folder="frontend/static")

# 1. Serve your frontend at “/”
@app.route("/")
def index():
    # this will look for static/index.html
    return app.send_static_file("index.html")

# 2. Handle the “Generate Video” call
@app.route("/generate", methods=["POST"])
def generate():
    payload = request.get_json()
    question = payload.get("question", "").strip()
    if not question:
        return {"error": "No question provided."}, 400

    # 2a. Create the script
    script_text = agent.createScript(question)
    script_path = "phasechange.py"
    dataSaver.saveVideoScript(script_text, script_path)

    # 2b. Convert to MP4
    video_path = "phasechange.mp4"
    scriptToVideo.convert_to_mp4(script_path, video_path)

    # 2c. Stream the MP4 back
    return send_file(video_path, mimetype="video/mp4")

if __name__ == "__main__":
    # Flask will look in ./static for index.html automatically
    app.run(debug=True)
