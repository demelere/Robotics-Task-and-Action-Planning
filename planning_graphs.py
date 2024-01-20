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


# Define actions
actions = [
    Action("Pick up key", preconditions={"at door"}, add_effects={"has key"}, del_effects=set()),
    Action("Unlock door", preconditions={"has key"}, add_effects={"door unlocked"}, del_effects=set()),
    Action("Open door", preconditions={"door unlocked"}, add_effects={"door open"}, del_effects=set()),
    Action("Walk through door", preconditions={"door open"}, add_effects={"at garden"}, del_effects={"at door"})
]

# Initial state and goal state
initial_state = {"at door"}
goal_state = {"at garden"}

# Create and build the planning graph
planning_graph = PlanningGraph(initial_state, actions)
planning_graph.build_graph(goal_state)
planning_graph.display()
