import unittest
from mock import patch
import nba.game as game

class mockurlopen():

    def __init__(self, url):
        self.url = url

    def read(self):
        with open('tests/data/gamePlayByPlay.html') as f:
            return f.read()


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = game.Game(400579520)

    def testSmoke(self):
        self.assertIsNotNone(self.game)

    def testPlayByPlay(self):
        game.urllib2.urlopen = mockurlopen
        print self.game.getPlayByPlay()
        self.assertEqual( u'Troy Daniels makes 29-foot  three pointer ', self.game.getPlayByPlay()[334]['play'])
