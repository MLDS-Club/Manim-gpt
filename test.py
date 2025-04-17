from agent_base import ManimAgent
from tools import dataSaver
from tools import scriptToVideo

agent = PrefetchManimAgent()
question = 'Calculate and visualize the centripetal force of a hampster running on a wheel'
result = agent.create_script(question)
dataSaver.saveVideoScript(result, "hampster.py")
scriptToVideo.convert_to_mp4('hampster.py', 'hampster.mp4')
# print(result)


#TODO: make this work with the new agent_base agent_prefetch system. (work in progress)
#This version DOES in fact work if you call just agent2 in this test.py. replace this test.py with the old one and replace agent with agent2 to get a working demo.
