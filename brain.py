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

  def getmaxadjidx(self, adjvalsfood, adjvalspred, adjvalsmarsh):
    if not adjvalsfood:
      adjvalsfood = [0] * 8
    if not adjvalspred:
      adjvalspred = [0] * 8
    #if not adjvalsmarsh:
      adjvalsmarsh = [0] * 8

    print adjvalsfood
    maxIdx = 0
    maxVal = self.n.activate((adjvalsfood[0], adjvalspred[0], adjvalsmarsh[0]))
    for i in xrange(len(adjvalsfood)):
      val = self.n.activate((adjvalsfood[i], adjvalspred[i], adjvalsmarsh[i]))
      if val < maxVal:
        maxIdx = i
        maxVal = val
      print str(val) + " for " + str(adjvalsfood[i]) + ", " + str(adjvalspred[i]) + ", " + str(adjvalsmarsh[i])
    return maxIdx
