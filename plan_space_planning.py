import time
import matplotlib.pyplot as plt

class Action:
    def __init__(self, name, preconditions, effects):
        self.name = name
        self.preconditions = set(preconditions)
        self.effects = set(effects)

    def __repr__(self):
        return f"{self.name}"

class PlanSpacePlanner:
    def __init__(self, actions):
        self.actions = actions

    def find_plan(self, initial_state, goal_state, max_depth=10):
        return self._search([], initial_state, goal_state, max_depth, 0)

    def _search(self, plan, current_state, goal_state, max_depth, depth):
        if depth > max_depth:
            return None

        if goal_state.issubset(current_state):
            return plan

        for action in self.actions:
            if action.preconditions.issubset(current_state):
                new_state = current_state.union(action.effects)
                new_plan = plan + [action]
                result = self._search(new_plan, new_state, goal_state, max_depth, depth + 1)
                if result is not None:
                    return result

        return None

def run_experiment(max_actions):
    execution_times = []
    num_actions = range(1, max_actions + 1)

    for n in num_actions:
        print(f"\nRunning experiment with {n} actions")
        actions = [Action(f"Action{i}", [f"Precond{i}"], [f"Effect{i}"]) for i in range(n)]

        planner = PlanSpacePlanner(actions)
        initial_state = set(["Precond0"])
        goal_state = set([f"Effect{n-1}"])

        print("Starting plan-space planning")
        start_time = time.time()
        plan = planner.find_plan(initial_state, goal_state)
        end_time = time.time()

        execution_time = end_time - start_time
        print(f"Execution time for {n} actions: {execution_time} seconds")
        execution_times.append(execution_time)

        if plan:
            print(f"Plan found with {len(plan)} steps")
        else:
            print("No plan found")

    return num_actions, execution_times

# Run the experiment
max_actions = 10  # Adjust based on your computational resources
num_actions, execution_times = run_experiment(max_actions)

# Plotting the results
plt.plot(num_actions, execution_times, marker='o')
plt.xlabel('Number of Actions')
plt.ylabel('Execution Time (seconds)')
plt.title('Plan-Space Planning Complexity')
plt.show()
