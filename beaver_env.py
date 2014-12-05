from pybrain.rl.environments.environment import Environment

class BeaverEnv(Environment):
  def getSensors(self):
    pass

  def performAction(self, action):
    pass

  def reset(self):
    # Most environments will implement this optional method that allows for
    # reinitialization
    pass
