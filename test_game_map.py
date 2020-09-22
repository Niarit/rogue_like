from unittest import TestCase


class TestGameMap(TestCase):
    def test_in_bounds(self):
        from game_map import GameMap
        game_map = GameMap(5, 5)
        self.assertFalse(game_map.in_bounds(5, 6))
