from tools import agent
from tools import dataSaver
from tools import scriptToVideo

question = 'If I invest $100 and it increases by 5 percent each year, how much money will I have after 4 years?'
result = agent.createScript(question)
dataSaver.saveVideoScript(result, "test1.py")
scriptToVideo.convert_to_mp4('test1.py', 'test1.mp4')
# print(result)