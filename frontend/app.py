# # frontend/app.py
#
# import os, sys
# from flask import Flask, request, send_file
#
# # ─────────────────────────────────────────────────────────────────────────────
# # 1) Make sure we can do `from tools import …`
# BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
# PROJECT_ROOT  = os.path.abspath(os.path.join(BASE_DIR, ".."))
# sys.path.append(PROJECT_ROOT)
#
# # ─────────────────────────────────────────────────────────────────────────────
# # 2) Flask static setup
# STATIC_DIR = os.path.join(BASE_DIR, "static")
# app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="")
#
# @app.route("/")
# def index():
#     return app.send_static_file("index.html")
#
# # ─────────────────────────────────────────────────────────────────────────────
# # 3) Where Manim writes its final videos
# VIDEO_DIR = os.path.join(PROJECT_ROOT, "frontend", "media", "videos", "_temp_script", "1080p60")
# os.makedirs(VIDEO_DIR, exist_ok=True)
#
# # ─────────────────────────────────────────────────────────────────────────────
# from tools import agent, dataSaver, scriptToVideo
#
# @app.route("/generate", methods=["POST"])
# def generate():
#     data     = request.get_json() or {}
#     question = data.get("question", "").strip()
#     if not question:
#         return {"error": "No question provided."}, 400
#
#     # A) Let the agent emit its own Python script text & name
#     script_text = agent.createScript(question)
#     # assume dataSaver will pick a filename internally or you can extract it;
#     # but to be safe, we'll write to a temp file:
#     tmp_script = os.path.join(BASE_DIR, "_temp_script.py")
#     dataSaver.saveVideoScript(script_text, tmp_script)
#
#     # B) Run Manim conversion – Manim writes to output/compiledVideo/<YourName>.mp4
#     scriptToVideo.convert_to_mp4(tmp_script, VIDEO_DIR)
#
#     # C) Now grab the very latest .mp4 in that directory
#     mp4_files = [
#         os.path.join(VIDEO_DIR, f)
#         for f in os.listdir(VIDEO_DIR)
#         if f.lower().endswith(".mp4")
#     ]
#     if not mp4_files:
#         return {"error": "Video conversion failed."}, 500
#
#     # sort by modification time, newest first
#     mp4_files.sort(key=os.path.getmtime, reverse=True)
#     latest_video = mp4_files[0]
#
#     # stream it back
#     return send_file(latest_video, mimetype="video/mp4")
#
#
# if __name__ == "__main__":
#     app.run(debug=True)


# frontend/app.py

import os, sys
from flask import Flask, request, send_file

# ─────────────────────────────────────────────────────────────────────────────
# 1) Make sure we can import tools
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT  = os.path.abspath(os.path.join(BASE_DIR, ".."))
sys.path.append(PROJECT_ROOT)

# ─────────────────────────────────────────────────────────────────────────────
# 2) Set up Flask app to serve static frontend
STATIC_DIR = os.path.join(BASE_DIR, "static")
app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="")

@app.route("/")
def index():
    return app.send_static_file("index.html")

# ─────────────────────────────────────────────────────────────────────────────
# 3) Final video directory (Manim output path)
VIDEO_DIR = os.path.join(BASE_DIR, "media", "videos", "_temp_script", "1080p60")
os.makedirs(VIDEO_DIR, exist_ok=True)

from tools import agent, dataSaver, scriptToVideo

@app.route("/generate", methods=["POST"])
def generate():
    data     = request.get_json() or {}
    question = data.get("question", "").strip()
    if not question:
        return {"error": "No question provided."}, 400

    # A) Save script to a known temp file
    temp_script_path = os.path.join(BASE_DIR, "_temp_script.py")
    script_text = agent.createScript(question)
    dataSaver.saveVideoScript(script_text, temp_script_path)

    # B) Convert it using Manim (outputs to media/videos/_temp_script/1080p60/)
    scriptToVideo.convert_to_mp4(temp_script_path, VIDEO_DIR)

    # C) Find latest generated video in VIDEO_DIR
    mp4_files = [
        os.path.join(VIDEO_DIR, f)
        for f in os.listdir(VIDEO_DIR)
        if f.lower().endswith(".mp4")
    ]
    if not mp4_files:
        return {"error": "No video file found."}, 500

    mp4_files.sort(key=os.path.getmtime, reverse=True)
    latest_video = mp4_files[0]

    return send_file(latest_video, mimetype="video/mp4")
    print(f"[DEBUG] Returning video: {latest_video}")

if __name__ == "__main__":
    app.run(debug=True)

