# manimToMp4.py
import os
import subprocess
import glob
import shutil

def convert_to_mp4(input_file: str, output_file: str):
    """
    Given an input_file (e.g. 'inputFile.py') located in ../output/videoScript,
    render it with Manim and move the resulting .mp4 into ../output/compiledVideo
    under the name provided by output_file (e.g. 'outputVideo.mp4').
    
    Paths are built relative to this file's directory (i.e. the 'tools/' folder).
    """
    # 1. Identify relevant paths
    script_dir = os.path.dirname(os.path.abspath(__file__))   # Directory of manimToMp4.py
    video_script_dir = os.path.join(script_dir, "..", "output", "videoScript")
    compiled_video_dir = os.path.join(script_dir, "..", "output", "compiledVideo")
    media_videos_dir = os.path.join(script_dir, "..", "media", "videos")

    input_path = os.path.join(video_script_dir, input_file)
    final_output_path = os.path.join(compiled_video_dir, output_file)

    # 2. Ensure the compiled video directory exists
    os.makedirs(compiled_video_dir, exist_ok=True)

    # 3. Render the Manim script
    #    -pqh = preview in high quality (you can adjust to your preference)
    subprocess.run(["manim", "-pqh", input_path], check=True)

    # 4. Find the newest mp4 file produced in the media/videos directory
    mp4_files = glob.glob(os.path.join(media_videos_dir, "**", "*.mp4"), recursive=True)
    if not mp4_files:
        raise FileNotFoundError("No MP4 files were found after rendering with Manim.")

    newest_mp4 = max(mp4_files, key=os.path.getmtime)

    # 5. Move/rename the rendered file to the 'compiledVideo' directory
    shutil.move(newest_mp4, final_output_path)
    print(f"Video compiled and saved at: {final_output_path}")
