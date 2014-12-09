from constants import Constants

class GameParameters:
  BG_COLOR = (0, 92, 9)
  HEALTHBAR_COLOR = (0, 255, 0)
  HEALTHBAR_HEIGHT = 5

  SCREEN_WIDTH = 640
  SCREEN_HEIGHT = 400

  FRAMERATE = 60

  NUM_GENERATIONS = 30

class AgentParameters:
  ALPHA = 0.5
  GAMMA = 0.0
  EPSILON = 0.5
  INITIAL_ACTION_VALUE_TABLE_VALUE = 0.0

class BeaverParameters:
  CONST_VIEW_DIST = 300
  CONST_SCENT_DIST = 200
  CONST_STEP_SIZE_LAND = 1 # pixels
  CONST_STEP_SIZE_WATER = 4

  CONST_LUMBER_WEIGHT = 2

  CONST_INITIAL_ENERGY = 100
  CONST_MAX_ENERGY = 100

  CONST_DEAD_ENERGY_THRESHOLD = 0
  CONST_LOW_ENERGY_THRESHOLD = 30
  CONST_MED_ENERGY_THRESHOLD = 70

  CONST_ENERGY_IDLE_COST = .15
  CONST_ENERGY_WALK_LAND_COST = 0.5
  CONST_ENERGY_WALK_WATER_COST = 0.25
  CONST_ENERGY_EAT_GAIN = 0.5
  CONST_ENERGY_PICK_UP_LUMBER_COST = 0.25

class MarshParameters:
  INITIAL_HEALTH = 50
  MAX_HEALTH = 150
  MIN_HEALTH = 20

  LOW_HEALTH_THRESHOLD = 30
  MED_HEALTH_THRESHOLD = 70

  HEALTH_LUMBER_GAIN = 10
  HEALTH_IDLE_COST = 0.025

class TerrainParameters:
  MAX_NUM_TREES = 50

class TreeParameters:
  INITIAL_HEALTH = 100
  HEALTH_EATEN_COST = 1
  HEALTH_FORAGED_COST = 50

class WolfParameters:
  CONST_VIEW_DIST = 100
  # randomly selected every time
  CONST_SCENT_DISTS = ([100] * 5) + ([200] * 10) + ([225] * 5)
  CONST_STEP_SIZE = 2

class StateWeightParameters:
  BEAVER_ENERGY = {
    Constants.BEAVER_STATE_BEAVER_ENERGY_ZERO:  0,
    Constants.BEAVER_STATE_BEAVER_ENERGY_LOW:   0.3,
    Constants.BEAVER_STATE_BEAVER_ENERGY_MED:   0.6,
    Constants.BEAVER_STATE_BEAVER_ENERGY_HIGH:  1
  }

  MARSH_ENERGY = {
    Constants.BEAVER_STATE_MARSH_HEALTH_LOW:    0.1,
    Constants.BEAVER_STATE_MARSH_HEALTH_MED:    0.5,
    Constants.BEAVER_STATE_MARSH_HEALTH_HIGH:   1
  }

  LUMBER = {
    Constants.BEAVER_STATE_HAS_LUMBER:          0.5,
    Constants.BEAVER_STATE_NO_LUMBER:           0.5
  }

  TREE = {
    Constants.BEAVER_STATE_SEE_TREE:            0.7,
    Constants.BEAVER_STATE_AT_TREE:             1,
    Constants.BEAVER_STATE_NONE_TREE:           0.3
  }

  MARSH = {
    Constants.BEAVER_STATE_SEE_MARSH:           0.3,
    Constants.BEAVER_STATE_AT_MARSH:            0.3,
    Constants.BEAVER_STATE_NONE_MARSH:          0.1
  }

  WOLF = {
    Constants.BEAVER_STATE_SEE_WOLF:            0.05,
    Constants.BEAVER_STATE_NONE_WOLF:           0.7
  }

  ACTION = {
    Constants.BEAVER_ACTION_MOVE_TREE:          0.9,
    Constants.BEAVER_ACTION_MOVE_MARSH:         0.5,
    Constants.BEAVER_ACTION_EAT:                1.0,
    Constants.BEAVER_ACTION_PICK_UP_LUMBER:     0.5,
    Constants.BEAVER_ACTION_DROP_LUMBER:        0.5
  }