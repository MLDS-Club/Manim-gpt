from tools import agent
from tools import dataSaver
from tools import manimToMp4

question = "What is the square root of 64?"
result = agent.createScript(question)
dataSaver.saveVideoScript(result, "testScript.py")
manimToMp4.render_manim('./output/videoScript/testScript.py', './output/compiledVideo/sqrt64.mp4')
print(result)
