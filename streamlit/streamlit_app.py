import os, sys

import streamlit as st
import glob
import time
import uuid



#Setup directories to import tools
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

#import the tools
from tools import agent, dataSaver, scriptToVideo


######
#Config streamlit page
st.set_page_config(page_title="Manim Video Generator", layout = "centered")
st.title("Manim Math Video Generator")

st.markdown("Genorate AI Math help videos by entering prompts")


#---Paths for the actual scripts---
#Paths for video genoration
#Paths for manim genoration


TEMP_SCRIPT_DIR = os.path.join(BASE_DIR, "temp_scripts")
#the videos folder where the finished videos goes gets assigned to video search root so we can loop through the directory and search for the most recent genorated mp4s
VIDEO_SEARCH_ROOT = os.path.join(BASE_DIR, "media", "videos")

os.makedirs(TEMP_SCRIPT_DIR, exist_ok=True)

#--- GENERATE PROMPT BOX UI IN STREAMLIT ---
prompt = st.text_area(
    "Prompt",
    placeholder="e.g. Demonstrate how an XOR logic gate works with two input lines A and B ...",
    height=150
)
generate_btn = st.button("Generate", type="primary")

if generate_btn:
    if not prompt.strip():
        st.warning("Please enter a prompt first.")
        st.stop()

    #Genorate a random hex name for each video so that the ai genorated names dont cause a discrepency in the

    uid = uuid.uuid4().hex
    script_path = os.path.join(TEMP_SCRIPT_DIR, f"script_{uid}.py")

    with st.spinner("Generating Manim script …"):
        script_text = agent.createScript(prompt)
        dataSaver.saveVideoScript(script_text, script_path)

    #Run manim create video:
    with st.spinner("Rendering video — this may take a minute …"):
        # Note: adjust this call if your `scriptToVideo.convert_to_mp4` signature differs.
        scriptToVideo.convert_to_mp4(script_path, VIDEO_SEARCH_ROOT)

    #Loop through the mp4 directroy and find newly made videos
    mp4_candidates = glob.glob(os.path.join(VIDEO_SEARCH_ROOT, "**", "*.mp4"), recursive=True)
    if not mp4_candidates:
        st.error("No MP4 files were produced. Check Manim logs.")
        st.stop()

    latest_mp4 = max(mp4_candidates, key=os.path.getmtime)

    time.sleep(0.5)

    st.success("VIDEO IS GENORATED!!")

    #Display the final vidoe
    st.video(latest_mp4)










