from flask import Flask

app = Flask(__name__)

@app.route("/generatevideo")
def generate_video():
    """Code to do generating video probably"""
    return "<p>Hello, World!</p>"