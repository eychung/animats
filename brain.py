from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection

class Brain:
  def __init__(self):
    n = FeedForwardNetwork()
    n.addInputModule(LinearLayer(2, name='in')
    n.addModule(SigmoidLayer(3, name='hidden')
    n.addOutputModule(LinearLayer(1, name='out')
    n.addConnection(FullConnection(n['in'], n['hidden'], name='c1'))
    n.addConnection(FullConnection(n['hidden'], n['out'], name='c2'))
    n.sortModules()

  
