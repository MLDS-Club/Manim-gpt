import importlib.util
import subprocess
import shutil
from pathlib import Path
from manim import Scene
import os

def render_manim(filename_input: str, filename_output: str) -> None:
    """Renders a Manim video from a Python script and saves it to the specified output location."""
    
    # Define the base paths for video script and compiled videos
    base_dir = Path(__file__).resolve().parent.parent
    video_script_folder = base_dir / 'output' / 'videoScript'
    compiled_video_folder = base_dir / 'output' / 'compiledVideo'
    
    # Ensure directories exist
    video_script_folder.mkdir(parents=True, exist_ok=True)
    compiled_video_folder.mkdir(parents=True, exist_ok=True)
    
    # Construct input file path
    input_file_path = video_script_folder / filename_input

    # Validate the input file
    if not input_file_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file_path}")
    if input_file_path.suffix != '.py':
        raise ValueError("The input file must be a Python (.py) script.")
    
    print(f"Processing Manim script: {input_file_path}")

    # Load the module dynamically
    module_name = input_file_path.stem
    spec = importlib.util.spec_from_file_location(module_name, str(input_file_path))
    
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not import module from {input_file_path}")
    
    module = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        raise ImportError(f"Error loading module {module_name}: {e}")
    
    # Find all Manim Scene subclasses
    scenes = [obj.__name__ for obj in module.__dict__.values()
              if isinstance(obj, type) and issubclass(obj, Scene) and obj is not Scene]
    
    if not scenes:
        raise ValueError(f"No Manim Scene classes found in {filename_input}")
    
    scene_name = scenes[0]  # Use the first scene found
    print(f"Detected Manim Scene: {scene_name}")

    # Build the Manim command
    command = [
        'manim',
        str(input_file_path),
        '-pql',  # Low quality for faster rendering; use '-qm' for medium
        scene_name
    ]
    
    print(f"Running Manim command: {' '.join(command)}")

    # Execute the Manim render command
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Manim output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Manim error:\n{e.stderr}")
        raise RuntimeError(f"Manim rendering failed: {e.stderr}") from e

    # Determine the expected output video path
    quality_dir = '480p15'  # Matches '-pql' setting
    generated_video = Path('./media/videos') / module_name / quality_dir / f"{scene_name}.mp4"

    if not generated_video.exists():
        raise FileNotFoundError(f"Rendered video not found: {generated_video}")

    print(f"Rendered video located at: {generated_video}")

    # Define the final output path
    output_path = compiled_video_folder / filename_output

    # Ensure the output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Move the generated video to the output location
    shutil.move(str(generated_video), str(output_path))
    print(f"Video successfully saved to: {output_path}")

    # Clean up generated media folder
    media_folder = Path('./media/videos') / module_name
    if media_folder.exists():
        shutil.rmtree(media_folder)
        print(f"Cleaned up media folder: {media_folder}")

