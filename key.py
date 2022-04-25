"""
Key class for the oracle. Each key has a number of bittings that are cut at a specific depth.
"""

class Key:
    def __init__(self, num_cuts, bitting_depth, standard):
        self.num_cuts = num_cuts
        self.bitting_depth = bitting_depth
        self.bittings = [0 for i in range(0, num_cuts)]
        
    def get_bitting(self, index):
        return self.bittings[index]

    def get_bittings(self):
        return self.bittings.copy()


    def set_bittings(self, bitting_list):
        self.num_cuts = len(bitting_list)
        self.bittings = bitting_list

    
