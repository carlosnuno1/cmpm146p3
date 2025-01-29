import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True))

    # Target weakest planets (considers incoming enemy fleets)
    def planet_vulnerability(planet):
        return planet.num_ships + \
               sum(fleet.num_ships for fleet in state.enemy_fleets() if fleet.destination_planet == planet.ID) - \
               sum(fleet.num_ships for fleet in state.my_fleets() if fleet.destination_planet == planet.ID)

    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    # Sort planets by weakness and growth
    enemy_planets.sort(key=lambda p: (planet_vulnerability(p), -p.growth_rate))

    target_planets = iter(enemy_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = planet_vulnerability(target_planet) + \
                           state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 5

            # Only attack if we have enough ships and it's worth it
            if my_planet.num_ships > required_ships * 1.1 and my_planet.num_ships > 20:
                issue_order(state, my_planet.ID, target_planet.ID, int(required_ships * 1.1))
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return False
    return True


def spread_to_weakest_neutral_planet(state):
    # Prioritize planets by growth and ship count
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True))

    neutral_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    
    # Find which planet is most effecient to spread to based off distance and growth
    def planet_efficiency(planet, source_planet):
        distance = state.distance(source_planet.ID, planet.ID)
        required_ships = planet.num_ships + 1
        return (planet.growth_rate / (required_ships * distance + 1), -required_ships)

    # Try to spread from each planet
    try:
        my_planet = next(my_planets)
        while True:
            # Sort neutral planets for most effecient based on closest captured planet
            sorted_planets = sorted(neutral_planets, 
                                 key=lambda p: planet_efficiency(p, my_planet),
                                 reverse=True)
            
            if not sorted_planets:
                my_planet = next(my_planets)
                continue

            target_planet = sorted_planets[0]
            required_ships = target_planet.num_ships + 1

            # Only spread if have enough ships and don't leave planet too weak
            if my_planet.num_ships > required_ships * 1.1 and my_planet.num_ships > required_ships + 15:
                issue_order(state, my_planet.ID, target_planet.ID, int(required_ships * 1.1))
                neutral_planets.remove(target_planet)
                if not neutral_planets:
                    return True
            my_planet = next(my_planets)

    except StopIteration:
        return False
    return True


def defend_weakest_planet(state):
    """Sends ships from strongest to weakest friendly planet under attack."""
    my_planets = [planet for planet in state.my_planets()]
    if not my_planets:
        return False
    
    # Getting planet strength and incomingy enemy fleets
    def planet_strength(planet):
        return planet.num_ships \
               + sum(fleet.num_ships for fleet in state.my_fleets() if fleet.destination_planet == planet.ID) \
               - sum(fleet.num_ships for fleet in state.enemy_fleets() if fleet.destination_planet == planet.ID)
    
    weak_planets = [planet for planet in my_planets if planet_strength(planet) < 0]
    strong_planets = [planet for planet in my_planets if planet_strength(planet) > 0]

    if not weak_planets or not strong_planets:
        return False

    for weak_planet in weak_planets:
        needed_ships = abs(planet_strength(weak_planet)) + 1
        
        # Find closest captured strong planet that can help without becoming too weak
        strong_planets.sort(key=lambda p: state.distance(p.ID, weak_planet.ID))
        for strong_planet in strong_planets:
            if planet_strength(strong_planet) > needed_ships + 15:
                issue_order(state, strong_planet.ID, weak_planet.ID, needed_ships)
                return True
                
    return False


def attack_enemy_growth_rate(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships, reverse=True))

    enemy_planets = [planet for planet in state.enemy_planets()
                    if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    # Sort by weakness and growth
    enemy_planets.sort(key=lambda p: (p.growth_rate, -p.num_ships), reverse=True)

    target_planets = iter(enemy_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + \
                           state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1

            # Only attack if have enough ships and won't leave planet too weak
            if my_planet.num_ships > required_ships * 1.1 and my_planet.num_ships > required_ships + 15:
                issue_order(state, my_planet.ID, target_planet.ID, int(required_ships * 1.1))
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        return False
    return True
