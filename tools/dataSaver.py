import os

def saveVideoScript(content = "No content provided.", filename = "default.py"):

    print(f"Saving video script to {filename}...")
    
    # Strip any "`", "python", or whitespace characters from the beginning and end of the string
    content = content.strip().strip('`').strip('python').strip()
    
    # Define the path to the videoScript folder
    video_script_folder = os.path.join(os.path.dirname(__file__), '..', 'output', 'videoScript')
    
    # Ensure the directory exists
    os.makedirs(video_script_folder, exist_ok=True)
    
    # Define the full path to the file
    file_path = os.path.join(video_script_folder, filename)
    
    # Write the content to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Example usage
if __name__ == "__main__":
    saveVideoScript('example.txt', 'This is a test string.')