from pybrain.rl.environments.task import Task
from derived_constants import DerivedConstants

class BeaverTask(Task):
  def __init__(self, environment):
    # All tasks are coupled to an environment
    self.env = environment

  def performAction(self, action):
    self.env.performAction(action)

  def getObservation(self):
    # A filtered mapping to getSensors of the underlying environment
    sensors = self.env.getSensors()
    return sensors

  def getReward(self):
    return DerivedConstants.REWARDS[tuple(self.env.beaver.states + [self.env.beaver.action])]

  @property
  def indim(self):
    return DerivedConstants.NUM_ACTIONS

  @property
  def outdim(self):
    return DerivedConstants.NUM_STATES
