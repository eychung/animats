from constants import Constants

weights = {}
state_type_weights = [weights]
action_weights = {}
with open("state_weights.txt", 'r') as wfile:
  for line in wfile:
    if line == "break\n":
      weights = {}
      state_type_weights.append(weights)
    elif line == "action\n":
      weights = {}
      action_weights = weights
    else:
      state, weight = line.split(',')
      weight = float(weight)
      weights[state] = weight

only_states = []
rewards = {}
for beaver_state in state_type_weights[0].iteritems():
  for marsh_state in state_type_weights[1].iteritems():
    for lumber_state in state_type_weights[2].iteritems():
      for env_tree_state in state_type_weights[3].iteritems():
        for env_marsh_state in state_type_weights[4].iteritems():
          for env_wolf_state in state_type_weights[5].iteritems():
            only_state = (
              beaver_state[0], marsh_state[0], lumber_state[0],
              env_tree_state[0], env_marsh_state[0], env_wolf_state[0])
            only_states.append(only_state)

            for action in action_weights.iteritems():
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

import pickle
pickle.dump(rewards, open('rewards.p', 'wb'))
pickle.dump(index_to_state, open('index_to_state.p', 'wb'))
pickle.dump(state_to_index, open('state_to_index.p', 'wb'))

# import csv
# writer = csv.writer(open('rewards.csv', 'wb'))
# for key, value in rewards.items():
#    writer.writerow([key, value])