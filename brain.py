from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q
from pybrain.rl.experiments import Experiment
from pybrain.rl.environments import Task
from pybrain.rl.explorers import EpsilonGreedyExplorer
from beaver_env import BeaverEnv
from beaver_task import BeaverTask
from constants import Constants

class Brain:
  def __init__(self):
    self.interactionscount = 0

    # Define action-value table
    controller = ActionValueTable(Constants.NUM_STATES, Constants.NUM_ACTIONS)
    controller.initialize(1.)

    # Define Q-learning agent where alpha is 0.5 and gamma is 0.0
    learner = Q(0.5, 0.0)
    #learner._setExplorer(EpsilonGreedyExplorer(0.0))
    agent = LearningAgent(controller, learner)

    # Define the environment
    #environment = BeaverEnv()

    # Define the task
    #task = BeaverTask(environment)

    # Finally, define experiment
   # experiment = Experiment(task, agent)

