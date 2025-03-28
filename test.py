from tools import agent
from tools import dataSaver
from tools import scriptToVideo

question = "How do I approximate pi using the Monte Carlo method?"
result = agent.createScript(question)
dataSaver.saveVideoScript(result, "piAprox2.py")
scriptToVideo.convert_to_mp4('piAprox2.py', 'piAprox2a.mp4')
# print(result)