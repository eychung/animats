from constants import Constants
from parameters import StateWeightParameters

def get_num_states():
  return (len(StateWeightParameters.BEAVER_ENERGY.keys()) *
          len(StateWeightParameters.MARSH_ENERGY.keys()) *
          len(StateWeightParameters.LUMBER.keys()) *
          len(StateWeightParameters.TREE.keys()) *
          len(StateWeightParameters.MARSH.keys()) *
          len(StateWeightParameters.WOLF.keys()))

def get_num_actions():
  return len(StateWeightParameters.ACTION.keys())

def get_state_to_index_and_rewards():
  only_states = []
  rewards = {}
  for beaver_state in StateWeightParameters.BEAVER_ENERGY.iteritems():
    for marsh_state in StateWeightParameters.MARSH_ENERGY.iteritems():
      for lumber_state in StateWeightParameters.LUMBER.iteritems():
        for env_tree_state in StateWeightParameters.TREE.iteritems():
          for env_marsh_state in StateWeightParameters.MARSH.iteritems():
            for env_wolf_state in StateWeightParameters.WOLF.iteritems():
              only_state = (
                beaver_state[0], marsh_state[0], lumber_state[0],
                env_tree_state[0], env_marsh_state[0], env_wolf_state[0])
              only_states.append(only_state)

              for action in StateWeightParameters.ACTION.iteritems():
                full_state = (
                  beaver_state[0], marsh_state[0], lumber_state[0],
                  env_tree_state[0], env_marsh_state[0], env_wolf_state[0],
                  action[0])

                if ((action[0] == Constants.BEAVER_ACTION_EAT and env_tree_state[0] != Constants.BEAVER_STATE_AT_TREE) or
                   (action[0] == Constants.BEAVER_ACTION_PICK_UP_LUMBER and env_tree_state[0] != Constants.BEAVER_STATE_AT_TREE) or
                   (action[0] == Constants.BEAVER_ACTION_PICK_UP_LUMBER and lumber_state[0] != Constants.BEAVER_STATE_NO_LUMBER) or
                   (action[0] == Constants.BEAVER_ACTION_DROP_LUMBER and lumber_state[0] != Constants.BEAVER_STATE_HAS_LUMBER) or
                   (action[0] == Constants.BEAVER_ACTION_MOVE_TREE and env_tree_state[0] != Constants.BEAVER_STATE_SEE_TREE) or
                   (action[0] == Constants.BEAVER_ACTION_MOVE_MARSH and env_marsh_state[0] != Constants.BEAVER_STATE_SEE_MARSH)):
                   rewards[full_state] = 0
                else:
                  rewards[full_state] = (
                    beaver_state[1] * marsh_state[1] * lumber_state[1] *
                    env_tree_state[1] * env_marsh_state[1] * env_wolf_state[1] *
                    action[1])

  index_to_state = sorted(only_states)
  state_to_index = {state: index for index, state in enumerate(index_to_state)}
  return (state_to_index, rewards)

class DerivedConstants:
  NUM_STATES = get_num_states()
  NUM_ACTIONS = get_num_actions()
  STATE_TO_INDEX, REWARDS = get_state_to_index_and_rewards()