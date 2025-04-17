from tools import agent
from tools import dataSaver
from tools import scriptToVideo

question = "How do airplane wings generate lift?"
name = "o4-mini-lift"
result = agent.createScript(question)
dataSaver.saveVideoScript(result, name + ".py")
scriptToVideo.convert_to_mp4(name + ".py", name + ".mp4")
# print(result)

#New idea: use more creative model for inital code generation, then use more reasoning model for solving errors.
#Issue: manim docret is being queried with prompts relating to the question, not to specific documentation