# scriptToVideo.py

import os
import subprocess
import glob
import shutil
import tempfile

def convert_to_mp4(input_file: str, output_file: str):
    """
    Given an input_file (e.g. 'my_scene.py') located in ../output/videoScript,
    this function:
      1) Strips off any prose or non‑Python lines before the first import
      2) Renders it with Manim (low‑quality for speed)
      3) Finds the newest .mp4 in media/videos
      4) Moves/renames it into ../output/compiledVideo/output_file
    """
    # 1) Identify relevant paths
    script_dir        = os.path.dirname(os.path.abspath(__file__))
    video_script_dir  = os.path.join(script_dir, "..", "output", "videoScript")
    compiled_video_dir= os.path.join(script_dir, "..", "output", "compiledVideo")
    media_videos_dir  = os.path.join(script_dir, "..", "media", "videos")

    input_path        = os.path.join(video_script_dir, input_file)
    final_output_path = os.path.join(compiled_video_dir, output_file)

    # 2) Ensure the compiled‑video directory exists
    os.makedirs(compiled_video_dir, exist_ok=True)

    # 3a) Read & strip out anything before the first 'import' or 'from'
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    start = 0
    for i, line in enumerate(lines):
        if line.lstrip().startswith(("import ", "from ")):
            start = i
            break
    cleaned_lines = lines[start:]

    # 3b) Write cleaned code to a temp file
    fd, clean_path = tempfile.mkstemp(suffix=".py", text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as wf:
            wf.writelines(cleaned_lines)

        # 4) Render the clean file with Manim (preview high‑quality = pqh)
        subprocess.run(
            ["manim", "-pqh", clean_path],
            check=True,
        )
    finally:
        # 5) Always remove the temp file
        if os.path.exists(clean_path):
            os.remove(clean_path)

    # 6) Locate the newest .mp4 in media/videos
    mp4_files = glob.glob(os.path.join(media_videos_dir, "**", "*.mp4"), recursive=True)
    if not mp4_files:
        raise FileNotFoundError("No MP4 files were found after rendering with Manim.")

    newest_mp4 = max(mp4_files, key=os.path.getmtime)

    # 7) Move/rename into compiledVideo
    shutil.move(newest_mp4, final_output_path)
    print(f"✅ Video compiled and saved at: {final_output_path}")


if __name__ == "__main__":
    # Example usage:
    # Assumes you have generated 'MyScene.py' into ../output/videoScript
    convert_to_mp4("MyScene.py", "MyScene.mp4")
