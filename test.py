from tools import agent
from tools import dataSaver
from tools import scriptToVideo

question = "Randomly generate some values for the following problem: what is the upward force on an airplane wing in 500 mile an hour winds? Visualize wind flowing around airplane wings and pressure difference due to flow."
result = agent.createScript(question)
dataSaver.saveVideoScript(result, "4o-test1.py")
scriptToVideo.convert_to_mp4('4o-test1.py', '4o-test1.mp4')
# print(result)

#New idea: use more creative model for inital code generation, then use more reasoning model for solving errors.
#Issue: manim docret is being queried with prompts relating to the question, not to specific documentation