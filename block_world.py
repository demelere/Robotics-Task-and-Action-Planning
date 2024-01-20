class BlockWorld:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
        print(f"Initialized BlockWorld with initial state: {initial_state} and goal state: {goal_state}")


    def get_successors(self, state):
        """ Generate all possible valid moves from the current state """
        successors = []
        for i in range(len(state)):
            for j in range(len(state)):
                if i != j:
                    new_state = state.copy()
                    new_state[i], new_state[j] = new_state[j], new_state[i]
                    successors.append(new_state)
        print(f"Generated {len(successors)} successors from state {state}")
        return successors

    def goal_test(self, state):
        """ Check if the current state is the goal state """
        is_goal = state == self.goal_state
        if is_goal:
            print(f"Reached goal state: {state}")
        return is_goal
        # return state == self.goal_state
        


class State:
    def __init__(self, block_positions):
        self.block_positions = block_positions

    def __repr__(self):
        return str(self.block_positions)

    def copy(self):
        return State(self.block_positions.copy())


def depth_first_search(problem):
    """ Depth-first search algorithm """
    stack = [problem.initial_state]
    visited = set()
    print("Starting Depth-First Search")

    while stack:
        state = stack.pop()
        print(f"Visiting state: {state}")
        if problem.goal_test(state.block_positions):
            return state

        if state not in visited:
            visited.add(state)
            successors = problem.get_successors(state.block_positions)
            for successor in successors:
                stack.append(State(successor))

    print("No solution found")
    return None


initial_state = State(["A", "B", "C"]) # define the initial state and goal state
goal_state = State(["C", "B", "A"])

problem = BlockWorld(initial_state, goal_state) # create a BlockWorld problem instance

solution = depth_first_search(problem) # perform the search
print("Solution:", solution)
