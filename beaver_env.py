from pybrain.rl.environments.environment import Environment
from derived_constants import DerivedConstants

class BeaverEnv(Environment):
  def __init__(self):
    self.beaver = None

  def setbeaver(self, beaver):
    self.beaver = beaver

  """ Map state to action; returns a numpy array of doubles (states)
  e.g. Say in a new array, x, that maps indices with a string that's a list
  of states, and x[1] represents "beaver energy high, marsh energy high, ..."
  return [float(index[1]), ]
  """
  def getSensors(self):
    return [float(DerivedConstants.STATE_TO_INDEX[tuple(self.beaver.states)])]

  def performAction(self, action):
    self.beaver.performaction(action)

  def reset(self):
    # Most environments will implement this optional method that allows for
    # reinitialization
    pass
