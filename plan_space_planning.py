class Action:
    def __init__(self, name, preconditions, effects):
        self.name = name
        self.preconditions = set(preconditions)
        self.effects = set(effects)

    def __repr__(self):
        return self.name


class Plan:
    def __init__(self, initial_state, goal_state):
        self.initial_state = set(initial_state)
        self.goal_state = set(goal_state)
        self.actions = []
        self.ordering_constraints = []
        self.causal_links = []

    def is_goal_reached(self):
        """ Check if the goal state is reached """
        current_state = set(self.initial_state)
        for action in self.actions:
            current_state.update(action.effects)
        return self.goal_state.issubset(current_state)

    def add_action(self, action):
        """ Add an action to the plan """
        self.actions.append(action)
        print(f"Added action: {action}")

    def __repr__(self):
        return f"Plan: {self.actions}"


class POPPlanner:
    def __init__(self, actions):
        self.actions = actions

    def plan(self, initial_state, goal_state):
        plan = Plan(initial_state, goal_state)
        while not plan.is_goal_reached():
            for action in self.actions:
                if action.preconditions.issubset(plan.initial_state):
                    plan.add_action(action)
                    plan.initial_state.update(action.effects)
                    if plan.is_goal_reached():
                        break
            else:
                print("No further actions can be applied.")
                break
        return plan


# Define actions
actions = [
    Action("Pick up key", preconditions={"at door"}, effects={"has key"}),
    Action("Unlock door", preconditions={"has key"}, effects={"door unlocked"}),
    Action("Open door", preconditions={"door unlocked"}, effects={"door open"}),
    Action("Walk through door", preconditions={"door open"}, effects={"at garden"})
]

# Create a planner
planner = POPPlanner(actions)

# Define initial state and goal state
initial_state = {"at door"}
goal_state = {"at garden"}

# Generate the plan
plan = planner.plan(initial_state, goal_state)
print("Final Plan:", plan)
