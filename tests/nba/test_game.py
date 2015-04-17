import unittest
from nba.game import Game


class TestGame(unittest.TestCase):

    def testSmoke(self):
        e = Game(400579520)
        self.assertIsNotNone(e)
