from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q
from pybrain.rl.experiments import Experiment
from pybrain.rl.environments import Task
from pybrain.rl.explorers import EpsilonGreedyExplorer
from beaver_env import BeaverEnv
from beaver_task import BeaverTask
from derived_constants import DerivedConstants
from parameters import AgentParameters

INITIAL_ACTION_VALUE_TABLE_VALUE = AgentParameters.INITIAL_ACTION_VALUE_TABLE_VALUE
ALPHA = AgentParameters.ALPHA
GAMMA = AgentParameters.GAMMA

class Brain:
  def __init__(self):
    self.interactionscount = 0

    # Define action-value table
    controller = ActionValueTable(DerivedConstants.NUM_STATES,
                                  DerivedConstants.NUM_ACTIONS)
    controller.initialize(INITIAL_ACTION_VALUE_TABLE_VALUE)

    # Define Q-learning agent
    learner = Q(ALPHA, GAMMA)
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
