from tools import agent
from tools import dataSaver
from tools import scriptToVideo

question = "What is the volume of a frustum with a top radius of 2 meters, a height of 5 meters, and a bottom radius of 4 meters?"
result = agent.createScript(question)
dataSaver.saveVideoScript(result, "test1.py")
scriptToVideo.convert_to_mp4('test1.py', 'test1.mp4')
# print(result)