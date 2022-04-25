"""
Lock class for the oracle. Each lock has a number of pins that are cut at a specific depth.
If a pin has multiple cuts, those are known as master pins.
"""

import key

class Lock:
    def __init__(self, num_pins, pin_depth, standard):
        self.num_pins = num_pins
        self.pin_depth = pin_depth
        self.standard = standard
        self.pin_cuts = [[] for i in range(0, num_pins)]

        # For visualization purpose only, for now
        if (standard < 0):
            standard = 0.003
            print("Standard defaulting to 0.003 depth interval...")

    def test(self, key):
        for i, cuts in enumerate(self.pin_cuts):
            if (key.get_bitting(i) in cuts):
                continue
            
            # print("Does not fit.")
            return 0

        # print("Fits.")
        return 1

    def set_cuts(self, cut_list):
        self.num_pins = len(cut_list)
        self.pin_cuts = cut_list
        
        
