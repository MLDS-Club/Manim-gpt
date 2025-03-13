from tools import agent
from tools import dataSaver
from tools import scriptToVideo

question = 'If I invest $100 and it increases by 5 percent each year, how much money will I have after 4 years?'
result = agent.createScript(question)
dataSaver.saveVideoScript(result, "navTest2.py")
scriptToVideo.convert_to_mp4('navTest2.py', 'navTestVideo2.mp4')
# print(result)