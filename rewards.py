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

rewards = {}
for beaver_state in state_type_weights[0].iteritems():
  for marsh_state in state_type_weights[1].iteritems():
    for lumber_state in state_type_weights[2].iteritems():
      for env_tree_state in state_type_weights[3].iteritems():
        for env_marsh_state in state_type_weights[4].iteritems():

          if env_tree_state[0] == "at tree" and env_marsh_state[0] == "at marsh":
            continue

          for env_wolf_state in state_type_weights[5].iteritems():
            for action in action_weights.iteritems():
              full_state = (
                beaver_state[0], marsh_state[0], lumber_state[0],
                env_tree_state[0], env_marsh_state[0], env_wolf_state[0],
                action[0])

              if ((action[0] == "eat" and env_tree_state[0] != "at tree") or
                 (action[0] == "pick up lumber" and env_tree_state[0] != "at tree") or
                 (action[0] == "pick up lumber" and lumber_state[0] != "has lumber") or
                 (action[0] == "drop lumber" and lumber_state[0] != "has lumber") or
                 (action[0] == "move towards tree" and env_tree_state[0] != "see tree") or
                 (action[0] == "move towards marsh" and env_marsh_state[0] != "see marsh")):
                 rewards[full_state] = 0
              else:
                rewards[full_state] = (
                  beaver_state[1] * marsh_state[1] * lumber_state[1] *
                  env_tree_state[1] * env_marsh_state[1] * env_wolf_state[1] *
                  action[1])

index_to_state = sorted(rewards.keys())
state_to_index = {state: index for index, state in enumerate(index_to_state)}

import pickle
pickle.dump(rewards, open('rewards.p', 'wb'))
pickle.dump(index_to_state, open('index_to_state.p', 'wb'))
pickle.dump(state_to_index, open('state_to_index.p', 'wb'))

# import csv
# writer = csv.writer(open('rewards.csv', 'wb'))
# for key, value in rewards.items():
#    writer.writerow([key, value])