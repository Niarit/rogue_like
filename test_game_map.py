from unittest import TestCase
from engine import Engine
import entity_factories
import copy


class TestGameMap(TestCase):
    def test_in_bounds(self):
        player = copy.deepcopy(entity_factories.player)
        engine = Engine(player=player)
        from game_map import GameMap
        game_map = GameMap(engine, 5, 5)
        self.assertFalse(game_map.in_bounds(5, 6))
