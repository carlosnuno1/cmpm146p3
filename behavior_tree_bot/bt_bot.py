#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn


# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():
    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    # Defend planets if attacked
    defensive_plan = Sequence(name='Defensive Strategy')
    under_attack = Check(is_planet_under_attack)
    defend = Action(defend_weakest_planet)
    defensive_plan.child_nodes = [under_attack, defend]

    # Spread to neutral planets
    spread_sequence = Sequence(name='Spread Strategy')
    neutral_planet_check = Check(if_neutral_planet_available)
    spread_action = Action(spread_to_weakest_neutral_planet)
    spread_sequence.child_nodes = [neutral_planet_check, spread_action]

    # High attack output with overwhelming force
    overwhelming_attack_plan = Sequence(name='Overwhelming Attack Strategy')
    overwhelming_check = Check(have_overwhelming_force)
    attack = Action(attack_weakest_enemy_planet)
    overwhelming_attack_plan.child_nodes = [overwhelming_check, attack]

    # Catch up strategy when losing
    losing_plan = Sequence(name='Losing Strategy')
    losing_check = Check(we_are_losing)
    spread_action = Action(spread_to_weakest_neutral_planet)
    losing_plan.child_nodes = [losing_check, spread_action]

    # Offensive strategy
    offensive_plan = Sequence(name='Offensive Strategy')
    largest_fleet_check = Check(have_largest_fleet)
    high_growth_check = Check(enemy_has_high_growth_planets)
    attack_growth = Action(attack_enemy_growth_rate)
    offensive_plan.child_nodes = [largest_fleet_check, high_growth_check, attack_growth]

    # Regular attack
    attack_sequence = Sequence(name='Attack Strategy')
    attack_action = Action(attack_weakest_enemy_planet)
    attack_sequence.child_nodes = [largest_fleet_check.copy(), attack_action]

    root.child_nodes = [defensive_plan, spread_sequence, overwhelming_attack_plan, losing_plan, offensive_plan, attack_sequence]

    logging.info('\n' + root.tree_to_string())
    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
