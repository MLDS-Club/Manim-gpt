from tools import agent_doublehead as agentDH
from tools import dataSaver
from tools import scriptToVideo

question = "What do wind patterns around airplane wings look like during airplane takeoff and landing?"
name = "o4-lift_4"
result = agentDH.createScript(question)
dataSaver.saveVideoScript(result, name + ".py")
scriptToVideo.convert_to_mp4(name + ".py", name + ".mp4")
# print(result)

#New idea: use more creative model for inital code generation, then use more reasoning model for solving errors.
#Issue: manim docret is being queried with prompts relating to the question, not to specific documentation