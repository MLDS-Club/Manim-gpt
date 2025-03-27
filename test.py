from tools import agent
from tools import dataSaver
from tools import scriptToVideo

question = ''
result = agent.createScript(question)
dataSaver.saveVideoScript(result, "piAproxxx.py")
scriptToVideo.convert_to_mp4('piAproxxx.py', 'piAproxxx.mp4')
# print(result)