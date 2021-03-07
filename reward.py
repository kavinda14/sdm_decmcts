from Simulator import Simulator

def reward(current_robot_path, other_robot_paths, robot, world_map):
    visited_survivors = set()
    #Find the survivors from the other robot paths
    for path in other_robot_paths:
        new_survivors = world_map.nearby_survivors(path, robot.sensing_range)
        visited_survivors = visited_survivors.union(new_survivors)
    score_without_curr_robot = len(visited_survivors)
        
    #Find the survivors from the current robot path
    new_survivors = world_map.nearby_survivors(current_robot_path, robot.sensing_range)
    visited_survivors = visited_survivors.union(new_survivors)
    score_with_curr_robot = len(visited_survivors)

    score = score_with_curr_robot - score_without_curr_robot
    return score

