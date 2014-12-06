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
    controller.initialize(0.)

    # Define Q-learning agent where alpha is 0.5 and gamma is 0.0
    learner = Q(0.5, 0.0)
    #learner._setExplorer(EpsilonGreedyExplorer(0.0))
    self.agent = LearningAgent(controller, learner)

    # Define the environment
    self.environment = BeaverEnv()

    # Define the task
    self.task = BeaverTask(self.environment)

    # Finally, define experiment
    self.experiment = Experiment(self.task, self.agent)

  def interact(self):
    #self.experiment.doInteractions(1)
    #self.agent.learn()
    #self.agent.reset()
    pass
