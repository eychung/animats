from pybrain.rl.environments.task import Task
from constants import Constants

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
    pass

  @property
  def indim(self):
    return Constants.NUM_ACTIONS

  @property
  def outdim(self):
    return Constants.NUM_STATES
