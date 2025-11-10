import random
import string

import pandas as pd
from variables.people import people as families_dict


def generate_secret_santa(seed: int):
    """
    Generate a Secret Santa assignment from a dictionary of families and their members.

    Args:
        families_dict: Dictionary with family names as keys and lists of people as values
        seed: Random seed for reproducibility (default: 42)

    Returns:
        Dictionary with random 6-character IDs as keys and tuples of (giver, receiver) as values
    """
    print(seed)
    random.seed(seed)

    # Create a mapping of each person to their family
    person_to_family = {}
    all_people = []

    for family, members in families_dict.items():
        for person in members:
            person_to_family[person] = family
            all_people.append(person)

    # Shuffle the people list
    shuffled = all_people.copy()
    random.shuffle(shuffled)

    # Create assignments ensuring no one from same family and no mutual assignments
    assignments = {}
    used_receivers = set()

    for giver in all_people:
        # Find a valid receiver (not from same family, not already used, not the same person)
        valid_receivers = [
            person
            for person in shuffled
            if person_to_family[person] != person_to_family[giver]
            and person not in used_receivers
            and person != giver
        ]

        if not valid_receivers:
            # If no valid receiver found, restart with a new shuffle
            shuffled = all_people.copy()
            random.shuffle(shuffled)
            valid_receivers = [
                person
                for person in shuffled
                if person_to_family[person] != person_to_family[giver]
                and person not in used_receivers
                and person != giver
            ]

        receiver = valid_receivers[0]
        used_receivers.add(receiver)
        assignments[giver] = receiver

    # Generate random IDs and create final result
    result = {}
    givers = {}
    for giver, receiver in assignments.items():
        random_id = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        result[random_id] = receiver
        givers[giver] = random_id

    return result, givers


def get_givers(seed):
    """
    Generate a mapping of givers to their unique IDs.

    Returns:
        Dictionary with givers as keys and their unique IDs as values
    """
    _, givers = generate_secret_santa(seed=seed)
    return givers


def get_assignments(secret_code, seed):
    return generate_secret_santa(seed=seed)[0].get(secret_code, "Code invalide")
