"""
Tests keys on locks and generates random values for bittings and pins.
"""

import random
import itertools

from lock import Lock
from key import Key

def generate_lock(pins, cuts, depth_limit, standard, method):
    lock_cuts = [[] for i in range(pins)]

    for i in range(0, pins):
        for j in range(0, cuts):
            random_number = random.randrange(0, depth_limit)
            lock_cuts[i].append(random_number)

    new_lock = Lock(pins, depth_limit, standard)
    new_lock.set_cuts(lock_cuts)

    return new_lock

def generate_key(bittings, depth_limit, standard):
    key_cuts = [0 for i in range(bittings)]

    for i in range(0, bittings):
        random_number = random.randrange(0, depth_limit)
        key_cuts[i] = (random_number)

    new_key = Key(bittings, depth_limit, standard)
    new_key.set_bittings(key_cuts)

    return new_key

def generate_key_from_set(possible_set, depth_limit, standard):
    bittings = len(possible_set)
    key_cuts = [0 for i in range(bittings)]
    count = 0

    for i in range(0, bittings):
        if (len(possible_set[i]) == 1):
            count += 1

    if (count == bittings):
        return -1


    for i in range(0, bittings):
        random_number = possible_set[i][random.randrange(0, len(possible_set[i]))]
        key_cuts[i] = (random_number)

    new_key = Key(bittings, depth_limit, standard)
    new_key.set_bittings(key_cuts)

    return new_key

def generate_tpp_set(bittings, depth_limit, master_key):
    num_sets = [[] for i in range(0, bittings)]
    master_cuts = master_key.get_bittings()
    key_cuts = master_key.get_bittings()

    for i in range(0, bittings):
        for j in range(0, depth_limit, 2):
            key_cuts[i] += 2
            key_cuts[i] = key_cuts[i] % depth_limit

            if (key_cuts[i] == master_cuts[i]):
                continue

            num_sets[i].append(key_cuts[i])

    combos = list(itertools.product(*num_sets))
    return combos   

# MACS = maximum adjacent cut specification, schlage = 7
def validate_keys(key_set, macs):
    k = key_set.copy()

    for key in key_set:
        for i in range(0, len(key) - 1):
            diff = abs(key[i] - key[i + 1])

            if (diff > macs):
                k.remove(key)
                break

    return k

def create_possible_set(bittings, depth_limit, change_key):
    num_sets = [[] for i in range(0, bittings)]
    change_cuts = change_key.get_bittings()
    key_cuts = change_key.get_bittings()

    for i in range(0, bittings):
        for j in range(0, depth_limit, 2):
            key_cuts[i] += 2
            key_cuts[i] = key_cuts[i] % depth_limit

            if (key_cuts[i] == change_cuts[i]):
                continue


            num_sets[i].append(key_cuts[i])

    return num_sets

def create_possible_set_test(bittings, depth_limit, change_key):
    num_sets = [[] for i in range(0, bittings)]
    key_cuts = change_key.get_bittings()

    for i in range(0, bittings):
        for j in range(0, depth_limit, 2):
            key_cuts[i] += 2
            key_cuts[i] = key_cuts[i] % depth_limit

            num_sets[i].append(key_cuts[i])

    return num_sets

def remove_from_set(bitting_set, possible_set):
    possible_bittings = possible_set.copy()
    num_bittings = len(bitting_set)

    for i in range(0, num_bittings):
        possible_bittings[i] = [x for x in possible_bittings[i] if x != bitting_set[i]]

    return possible_bittings

def display_list(ls):
    length = len(ls)

    for i in range(0, length):
        print(ls[i])

    return

def main():
    """
    Lock and key configuration
    """
    num_pins = 5
    num_cuts = 1
    depth_lock = 10

    num_bittings = 5
    depth_key = 10

    """
    Master key configuration
    """

    master_key_bittings = [0, 5, 2, 7, 4]
    master_key = Key(num_bittings, 10, 0.003)
    master_key.set_bittings(master_key_bittings)

    sample_change_key_bittings = [2, 1, 6, 5, 8]
    sample_change_key = Key(num_bittings, depth_key, 0.003)
    sample_change_key.set_bittings(sample_change_key_bittings)

    keys = generate_tpp_set(num_bittings, depth_key, master_key)
    keys = validate_keys(keys, 7)

    ps = create_possible_set_test(num_bittings, depth_key, sample_change_key)
    new_ps = create_possible_set_test(num_bittings, depth_key, sample_change_key)

    ps_copy = ps.copy()
    new_ps_copy = new_ps.copy()

    ps = remove_from_set(master_key_bittings, ps)

    print("Possible bitting depths:")
    display_list(ps)
    print()


    """
    Statistics
    """
    total_remaining_combos = 0


    """
    Generating random keys
    """
    keys_obtained = 30
    num_iterations = 1000

    for num_keys in range(0, keys_obtained + 1):
        total_remaining_combos = 0

        for j in range(0, num_iterations):
            # Variable reset
            ps = ps_copy.copy()
            new_ps = new_ps_copy.copy()

            ps = remove_from_set(master_key_bittings, ps)

            # RANDOM
            for i in range(0, num_keys):
                k = generate_key_from_set(ps, depth_key, 0.003)
                nk = generate_key_from_set(new_ps, depth_key, 0.003)
                good_key = validate_keys([k.get_bittings()], 7)

                while (len(good_key) <= 0):
                    k = generate_key_from_set(ps, depth_key, 0.003)
                    good_key = validate_keys([k.get_bittings()], 7)

                if (not isinstance(nk, Key)):
                    #print(f"{i} keys generated before finding master key")
                    #display_list(new_ps)
                    break

                new_ps = remove_from_set(k.get_bittings(), new_ps)

            remaining_combinations = len(validate_keys(list(itertools.product(*new_ps)), 7))
            total_remaining_combos += remaining_combinations
            #print(f"Remaining bitting combinations: { remaining_combinations }")

            #display_list(new_ps)
        print(total_remaining_combos / num_iterations)
        #print(f"Average remaining combinations: { total_remaining_combos / num_iterations }")

        #print(f"Number of keys: {len(keys)}")


if __name__ == "__main__":
    main()
