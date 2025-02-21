from tools import agent
from tools import dataSaver

question = "What is the area of a circle with a radius of 3 meters?"
result = agent.createScript(question)
dataSaver.saveVideoScript(result, "testScript.py")
print(result)
