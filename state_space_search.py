import time
import matplotlib.pyplot as plt

class BlockWorld:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def get_successors(self, state):
        successors = []
        for i in range(len(state)):
            for j in range(len(state)):
                if i != j:
                    new_state = state.copy()
                    new_state[i], new_state[j] = new_state[j], new_state[i]
                    successors.append(new_state)
        return successors

    def goal_test(self, state):
        return state == self.goal_state


class State:
    def __init__(self, block_positions):
        self.block_positions = block_positions

    def copy(self):
        return State(self.block_positions.copy())


def depth_first_search(problem):
    stack = [problem.initial_state]
    visited = set()

    while stack:
        state = stack.pop()
        print(f"Visiting state: {state.block_positions}")

        if problem.goal_test(state.block_positions):
            print("Goal state reached!")
            return state

        if state not in visited:
            visited.add(state)
            successors = problem.get_successors(state.block_positions)
            for successor in successors:
                stack.append(State(successor))

    print("No solution found")
    return None


def run_experiment(max_blocks):
    execution_times = []
    num_blocks = range(1, max_blocks + 1)

    for n in num_blocks:
        print(f"\nRunning experiment with {n} blocks")
        blocks = [chr(65 + i) for i in range(n)]  # create block labels (e.g. A, B, C, ...)
        initial_state = State(blocks)
        goal_state = State(blocks[::-1])  # reverse the block order for the goal state

        problem = BlockWorld(initial_state, goal_state)

        print("Starting depth-first search")
        start_time = time.time()
        depth_first_search(problem)
        end_time = time.time()

        execution_time = end_time - start_time
        print(f"Execution time for {n} blocks: {execution_time} seconds\n")
        execution_times.append(execution_time)

    return num_blocks, execution_times


# run the experiment
max_blocks = 10  # adjust according to computational resources
num_blocks, execution_times = run_experiment(max_blocks)

# plot exp results
plt.plot(num_blocks, execution_times, marker='o')
plt.xlabel('Number of Blocks')
plt.ylabel('Execution Time (seconds)')
plt.title('State-Space Search Complexity')
plt.show()
