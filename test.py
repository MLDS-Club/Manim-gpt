from tools import agent
from tools import dataSaver
from tools import scriptToVideo

question = "Randomly generate some values for the following problem: what is the upward force on an airplane wing in 500 mile an hour winds? Visualize wind flowing around airplane wings and pressure difference due to flow."
result = agent.createScript(question)
dataSaver.saveVideoScript(result, "piAprox2.py")
scriptToVideo.convert_to_mp4('piAprox2.py', 'piAprox2a.mp4')
# print(result)