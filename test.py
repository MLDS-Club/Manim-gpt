from tools import agent
from tools import dataSaver
from tools import scriptToVideo

question = "Demonstrate with visual detail the way a speaker works in terms of interacting with the air"
result = agent.createScript(question)
dataSaver.saveVideoScript(result, "speaker.py")
scriptToVideo.convert_to_mp4('speaker.py', 'speaker.mp4')
# print(result)