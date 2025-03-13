from tools import agent
from tools import dataSaver
from tools import scriptToVideo

question = "What is a 1-sample z interval for proportions?"
result = agent.createScript(question)
dataSaver.saveVideoScript(result, "navTest2.py")
scriptToVideo.convert_to_mp4('navTest2.py', 'navTestVideo2.mp4')
# print(result)