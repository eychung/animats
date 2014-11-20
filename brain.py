from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection

class Brain:
  def __init__(self):
    n = FeedForwardNetwork()
    n.addInputModule(LinearLayer(3, name='in'))
    n.addModule(SigmoidLayer(3, name='hidden'))
    n.addOutputModule(LinearLayer(1, name='out'))
    n.addConnection(FullConnection(n['in'], n['hidden'], name='c1'))
    n.addConnection(FullConnection(n['hidden'], n['out'], name='c2'))
    n.sortModules()

    self.n = n

  def getmaxadjidx(self, foodAdjVals, predAdjVals, marshAdjVals):
    if not foodAdjVals:
      foodAdjVals = [0] * 8
    if not predAdjVals:
      predAdjVals = [0] * 8
    if not marshAdjVals:
      marshAdjVals = [0] * 8

    maxIdx = 0
    maxVal = self.n.activate((foodAdjVals[0], predAdjVals[0], marshAdjVals[0]))
    for i in xrange(len(foodAdjVals)):
      val = self.n.activate((foodAdjVals[i], predAdjVals[i], marshAdjVals[i]))
      if val > maxVal:
        maxIdx = i
        maxVal = val
    return maxIdx
