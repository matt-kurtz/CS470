# Assignment #3
# By: Matthew Kurtz
# AI CS470 SU24

# Since we're dealing with a csv file, pandas is a great library to get that information
import pandas as pd
import random
import time

# Did some google searches for how to extract the data and put it into variables that we need for the CSP
def create_csp_model(data, num_colors):
    variables = list(data.columns)
    # This is a dictionary that keeps track of the domain (so 0 and 1 for the 2 colors)
    domains = {var: list(range(num_colors)) for var in variables}
    # This is another dictionary that tracks the neighbors. We'll go through each entry below to add the neighbors
    neighbors = {var: [] for var in variables}

    for i in range(len(variables)):
        for j in range(i+1, len(variables)):
            if data.iloc[i,j] == 1.0:
                neighbors[variables[i]].append(variables[j])
                neighbors[variables[j]].append(variables[i])
    return variables, domains, neighbors


def dfs_forward_checking_csp(data, num_colors):
    variables, domains, neighbors = create_csp_model(data, num_colors)
    assignments = {}
    assignment_count = 0

    # This function looks at whether or not assigning the variable to a spot will be possible and consistent
    def is_consistent(var, value, assignments, neighbors):
        for neighbor in neighbors[var]:
            if neighbor in assignments and assignments[neighbor] == value:
                return False
        return True

    # Are we making sure that all possible values its neighbor could have aren't eliminated?
    def forward_check(var, value, domains, assignments, neighbors):
        for neighbor in neighbors[var]:
            if neighbor not in assignments:
                if value in domains[neighbor]:
                    domains[neighbor].remove(value)
                    if not domains[neighbor]:
                        return False
        return True

    def backtrack():
        nonlocal assignment_count
        # Base case. Do we have an assignment for every variable?
        if len(assignments) == len(variables):
            return assignments
        # We select our variable here
        var = select_unassigned_variable()
        # This is where we iterate over ever possible color
        for value in domains[var]:
            if is_consistent(var, value, assignments, neighbors):
                assignments[var] = value
                assignment_count += 1
                # backup of the neighbors of the domains of the neighbors
                domains_backup = {neighbor: list(domains[neighbor]) for neighbor in neighbors[var] if neighbor not in assignments}
                # Here's where pruning of the neighbors can happen
                if forward_check(var, value, domains, assignments, neighbors):
                    result = backtrack()
                    if result:
                        return result
                # We clear out assignments since this iteration did not lead to a solution
                del assignments[var]
                # Restore the domains
                for neighbor in domains_backup:
                    domains[neighbor] = domains_backup[neighbor]
        return None

    # This helps us to pick a variable that isn't already assigned
    def select_unassigned_variable():
        for var in variables:
            if var not in assignments:
                return var
        return None

    print(f"Solving with {num_colors} colors using DFS with Forward Checking...")
    start_time = time.time()
    result = backtrack()
    end_time = time.time()
    duration = end_time - start_time

    if result:
        print(f"Solution found: {result}")
    else:
        print(f"No solution found with {num_colors} colors")

    print(f"Time taken: {duration:4f} seconds")
    print(f"Assignments made: {assignment_count}")
    return result

def min_conflicts_csp(data, num_colors, max_steps=10000):
    variables, domains, neighbors = create_csp_model(data, num_colors)
    assignment_count = 0

    # This is how we count the number of conflicts
    def count_conflicts(var, value, assignments):
        count = 0
        for neighbor in neighbors[var]:
            if neighbor in assignments and assignments[neighbor] == value:
                count += 1
        return count


    def min_conflicts():
        nonlocal assignment_count
        # Randomly assign values to all vars
        assignments = {var: random.choice(domains[var]) for var in variables}
        assignment_count += len(assignments)

        # Go through the vars and see/count the amount of conflicts
        for step in range(max_steps):
            conflicted_vars = [var for var in variables if count_conflicts(var, assignments[var], assignments) > 0]

            if not conflicted_vars:
                return assignments  # Solution found

            # Randomly assign a value again
            var = random.choice(conflicted_vars)
            min_conflict_value = min(domains[var], key=lambda val: count_conflicts(var, val, assignments))
            assignments[var] = min_conflict_value
            assignment_count += 1

        return None  # No solution found within the max steps

    print(f"Solving with {num_colors} colors using Min-Conflicts...")
    start_time = time.time()
    result = min_conflicts()
    end_time = time.time()
    duration = end_time - start_time
    if result:
        print(f"Solution found: {result}")
    else:
        print(f"No solution found with {num_colors} colors within {max_steps} steps")
    
    print(f"Time taken: {duration:.4f} seconds")
    print(f"Assignments made: {assignment_count}")
    return result

# For reference v v v v v v v v v v v v v v
# csp_data.columns are the region names
# 
if __name__ == '__main__':
    csp_data = pd.read_csv('CSPData.csv', index_col=0)

    variables, domains, neighbors = create_csp_model(csp_data, 2)
    
    #print("Variables: ", variables)
    #print("Domains: ", domains)
    #print("Neighbors: ", neighbors)

    for num_colors in range(2, 8):
        dfs_forward_checking_csp(csp_data, num_colors)
        min_conflicts_csp(csp_data, num_colors)
        print("\n\n")