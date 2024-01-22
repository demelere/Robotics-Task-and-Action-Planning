import time
import matplotlib.pyplot as plt

class Action:
    def __init__(self, name, preconditions, add_effects, del_effects):
        self.name = name
        self.preconditions = set(preconditions)
        self.add_effects = set(add_effects)
        self.del_effects = set(del_effects)

    def __repr__(self):
        return self.name


class PlanningGraph:
    def __init__(self, initial_state, actions):
        self.initial_state = set(initial_state)
        self.actions = actions
        self.layers = []

    def build_graph(self, goal_state, max_steps=10):
        current_state = self.initial_state
        for step in range(max_steps):
            print(f"Building layer {step}")
            action_layer = []
            new_state = current_state.copy()

            for action in self.actions:
                if action.preconditions.issubset(current_state):
                    action_layer.append(action)
                    new_state = new_state.union(action.add_effects) - action.del_effects

            self.layers.append((current_state, action_layer))
            if goal_state.issubset(new_state):
                print(f"Goal reached at step {step}")
                return self.layers

            current_state = new_state
        print("Goal not reached within max steps")
        return self.layers

    def display(self):
        for i, layer in enumerate(self.layers):
            print(f"Layer {i}:")
            print(f"  State: {layer[0]}")
            print(f"  Actions: {[action.name for action in layer[1]]}")
            print("")


def run_experiment(max_states):
    execution_times = []
    num_states = range(1, max_states + 1)

    for n in num_states:
        print(f"\nRunning experiment with {n} states")
        states = [f"State{i}" for i in range(n)]
        actions = [Action(f"Action{i}", [f"State{i}"], [f"State{i+1}"], []) for i in range(n-1)]

        planning_graph = PlanningGraph(states[:1], actions)
        goal_state = {states[-1]}

        print("Starting planning graph construction")
        start_time = time.time()
        planning_graph.build_graph(goal_state)
        end_time = time.time()

        execution_time = end_time - start_time
        print(f"Execution time for {n} states: {execution_time} seconds")
        execution_times.append(execution_time)

    return num_states, execution_times

# Run the experiment
max_states = 10  # Adjust based on your computational resources
num_states, execution_times = run_experiment(max_states)

# Plotting the results
plt.plot(num_states, execution_times, marker='o')
plt.xlabel('Number of States')
plt.ylabel('Execution Time (seconds)')
plt.title('Planning Graph Complexity')
plt.show()
