from tools import agent
from tools import dataSaver
from tools import scriptToVideo

question = 'What is the volume of a cone with radius of 3 and height of 6?'
result = agent.createScript(question)
dataSaver.saveVideoScript(result, "boog.py")
scriptToVideo.convert_to_mp4('boog.py', 'boogyboog.mp4')
# print(result)