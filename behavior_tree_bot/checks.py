def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    my_total = sum(planet.num_ships for planet in state.my_planets()) \
               + sum(fleet.num_ships for fleet in state.my_fleets())
    enemy_total = sum(planet.num_ships for planet in state.enemy_planets()) \
                 + sum(fleet.num_ships for fleet in state.enemy_fleets())
    return my_total > enemy_total * 1.1  # Only return True if we have 10% more ships


def is_planet_under_attack(state):
    """Check if any of our planets are under attack."""
    return any(fleet.destination_planet == planet.ID 
              for planet in state.my_planets()
              for fleet in state.enemy_fleets())


def enemy_has_high_growth_planets(state):
    """Check if enemy has planets with high growth rate (>2)."""
    return any(planet.growth_rate > 2 for planet in state.enemy_planets())


def we_are_losing(state):
    """Check if enemy has more total ships and production."""
    my_ships = sum(planet.num_ships for planet in state.my_planets()) \
               + sum(fleet.num_ships for fleet in state.my_fleets())
    enemy_ships = sum(planet.num_ships for planet in state.enemy_planets()) \
                 + sum(fleet.num_ships for fleet in state.enemy_fleets())
    
    my_growth = sum(planet.growth_rate for planet in state.my_planets())
    enemy_growth = sum(planet.growth_rate for planet in state.enemy_planets())
    
    return enemy_ships > my_ships * 0.8 or enemy_growth > my_growth 


def have_overwhelming_force(state):
    """Check if we have significantly more ships than the enemy."""
    my_ships = sum(planet.num_ships for planet in state.my_planets()) \
               + sum(fleet.num_ships for fleet in state.my_fleets())
    enemy_ships = sum(planet.num_ships for planet in state.enemy_planets()) \
                 + sum(fleet.num_ships for fleet in state.enemy_fleets())
    
    my_growth = sum(planet.growth_rate for planet in state.my_planets())
    enemy_growth = sum(planet.growth_rate for planet in state.enemy_planets())
    
    return my_ships > enemy_ships * 1.5 and my_growth >= enemy_growth  # Considers growth
