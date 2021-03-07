
def reward(current_robot_path, other_robot_paths, sensing_range, world_map):
    visited_survivors = set()

    #Find the survivors from the other robot paths
    for path in other_robot_paths:
        loc_path = [state.location for state in path]
        new_survivors = world_map.nearby_survivors(loc_path, sensing_range)
        visited_survivors = visited_survivors.union(new_survivors)
    reward_without_curr_robot = len(visited_survivors)
        
    #Find the survivors from the current robot path
    curr_path = [state.location for state in current_robot_path]
    new_survivors = world_map.nearby_survivors(curr_path, sensing_range)
    visited_survivors = visited_survivors.union(new_survivors)
    reward_with_curr_robot = len(visited_survivors)

    score = reward_with_curr_robot - reward_without_curr_robot
    return score

