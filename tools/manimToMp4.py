# function that takes the pathname of a python file, the pathname of an output location, and returns a manim video using the code inside the python file.
import importlib.util
import subprocess
import shutil
from pathlib import Path
from manim import Scene

def render_manim(filename: str, output_path: str) -> None:
    # Validate the input file exists
    input_path = Path(filename)
    if not input_path.exists():
        raise FileNotFoundError(f"The file {filename} does not exist.")
    if input_path.suffix != '.py':
        raise ValueError("The input file must be a Python (.py) file.")
    
    # Load the module from the file
    module_name = input_path.stem
    spec = importlib.util.spec_from_file_location(module_name, filename)
    if spec is None:
        raise ImportError(f"Could not import module from {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Find all Scene subclasses in the module
    scenes = []
    for attr in dir(module):
        obj = getattr(module, attr)
        if (isinstance(obj, type) and
            issubclass(obj, Scene) and
            obj.__name__ != 'Scene'):
            scenes.append(obj.__name__)
    
    if not scenes:
        raise ValueError(f"No Manim Scene classes found in {filename}.")
    scene_name = scenes[0]  # Use the first scene found

    # Build the Manim command
    command = [
        'manim',
        input_path,
        '-pql',  # Low quality for faster rendering; consider '-qm' for medium
        scene_name
    ]
    
    # Execute the Manim render command
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Manim rendering failed: {e.stderr}") from e
    
    # Determine the path of the generated video
    quality_dir = '480p15'  # Corresponds to -ql flag
    # check the specific media folder that manim should upload its videos to
    generated_video = Path('./media/videos/') / module_name / quality_dir / f"{scene_name}.mp4"
    
    if not generated_video.exists():
        raise FileNotFoundError(f"Rendered video not found at {generated_video}.")
    
    # Prepare the destination path
    output_path = Path(output_path)
    if output_path.is_dir():
        dest_path = output_path / f"{scene_name}.mp4"
    else:
        dest_path = output_path
    
    # Ensure the destination directory exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Move the video to the desired output path
    shutil.move(str(generated_video), str(dest_path))

    shutil.rmtree(Path('./media/videos/') / module_name)

render_manim('./output/videoScript/manimOutput.py', './output/compiledVideo/1+4output.mp4')