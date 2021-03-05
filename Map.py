import math
import numpy as np

class Map:
    def __init__(self, robots):
        """
        Inputs:
            robot: list of robot objects from Robot.py
        """
        #TODO: Change these values later?
        self.bounds = (0,10)
        self.num_survivors = 50
        self.num_hotspots = 10
        diff = self.bounds[1]*0.1

        #Randomly place people in the environment
        rand_x = np.random.uniform(self.bounds[0]+diff, self.bounds[1]-diff, size=self.num_hotspots)
        rand_y = np.random.uniform(self.bounds[0]+diff, self.bounds[1]-diff, size=self.num_hotspots)
        self.hotspots = [(rand_x[i], rand_y[i]) for i in range(0, len(rand_x))]

        self.survivor_locs = list()
        for i in range(0, self.num_survivors):
            hotspot_id = np.random.randint(0, self.num_hotspots)
            hotspot_loc = self.hotspots[hotspot_id]

            rand_diff_x = np.random.uniform(-0.5, 0.5)
            rand_diff_y = np.random.uniform(-0.5, 0.5)
            survivor_loc = (hotspot_loc[0]+rand_diff_x, hotspot_loc[1]+rand_diff_y)
            self.survivor_locs.append(survivor_loc)

        #TODO: Add in logic for barriers

    def nearby_survivors(self, robots):
        visited_states = set()
        for r in robots:
            r_loc = r.get_loc()
            for s_loc in self.survivor_locs:
                distance = self.euclidean_distance(r_loc, s_loc)
                if distance <= r.sensing_range:
                    visited_states.add(s_loc)
        return visited_states

    @staticmethod
    def euclidean_distance(p1, p2):
        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]

        return math.sqrt((y2-y1)**2 + (x2-x1)**2)