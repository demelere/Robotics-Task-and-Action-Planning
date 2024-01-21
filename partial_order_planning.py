class Action:
    def __init__(self, name, preconditions, effects):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects

    def __repr__(self):
        return f"{self.name}"


class PartialOrderPlan:
    def __init__(self, initial_state, goal_state):
        self.initial_actions = [Action('Start', [], initial_state)]
        self.final_actions = [Action('Finish', goal_state, [])]
        self.actions = self.initial_actions + self.final_actions
        self.orderings = {('Start', 'Finish')}
        self.causal_links = []
        self.open_preconditions = [(goal, 'Finish') for goal in goal_state]

    def is_consistent(self):
        for link in self.causal_links:
            for action in self.actions:
                if action.name != link[0].name and action.name != link[2].name:
                    if link[2] in action.effects and link[1] in action.preconditions:
                        return False
        return True

    def apply_action(self, action):
        self.actions.append(action)
        for precond in action.preconditions:
            self.open_preconditions.append((precond, action))
        for effect in action.effects:
            for open_precond in self.open_preconditions:
                if effect == open_precond[0]:
                    self.causal_links.append((action, effect, open_precond[1]))
                    self.orderings.add((action.name, open_precond[1].name))
                    self.open_preconditions.remove(open_precond)

    def choose_open_precondition(self):
        return self.open_preconditions[0] if self.open_preconditions else None

    def __repr__(self):
        return f"Actions: {self.actions}, Orderings: {self.orderings}, Causal Links: {self.causal_links}"


class PartialOrderPlanner:
    def __init__(self, actions):
        self.actions = actions

    def plan(self, initial_state, goal_state):
        plan = PartialOrderPlan(initial_state, goal_state)
        while plan.open_preconditions:
            precond = plan.choose_open_precondition()
            if not precond:
                break

            applicable_actions = [action for action in self.actions if precond[0] in action.effects]
            for action in applicable_actions:
                plan.apply_action(action)
                if plan.is_consistent():
                    break
            else:
                print("No applicable or consistent actions found.")
                return None

        return plan


# Define actions
actions = [
    Action("Pick up key", ["at door"], ["has key"]),
    Action("Unlock door", ["has key"], ["door unlocked"]),
    Action("Open door", ["door unlocked"], ["door open"]),
    Action("Walk through door", ["door open"], ["at garden"])
]

# Create a planner
planner = PartialOrderPlanner(actions)

# Define initial state and goal state
initial_state = ["at door"]
goal_state = ["at garden"]

# Generate the plan
plan = planner.plan(initial_state, goal_state)
print("Plan:")
print(plan)
