import unittest
import nba


class Mockurlopen():

    def __init__(self, url):
        print url
        self.url = url

    def read(self):
        if 'teams' in self.url:
            with open('tests/data/nbaTeams.html') as f:
                return f.read()
        elif 'schedule' in self.url:
            with open('tests/data/teamRegSeasonSched.html') as f:
                return f.read()
        elif 'playbyplay' in self.url:
            with open('tests/data/gamePlayByPlay.html') as f:
                return f.read()
        return


class TestNBA(unittest.TestCase):

    def setUp(self):
        self.nba = nba.NBA()
        nba.urllib2.urlopen = Mockurlopen

    def testSmoke(self):
        self.assertIsNotNone(self.nba)

    def testGetTeams(self):
        self.nba.getTeams()
        self.assertEqual(30, len(self.nba.teams))

    def testGetRegularSeasonGameIds(self):
        self.assertEqual(82, len(self.nba.getRegularSeasonGameIds(2015, 'bos')))

    def testPlayByPlay(self):
        self.assertEqual(u'Troy Daniels makes 29-foot  three pointer ', self.nba.getPlayByPlay(400579520)[334]['play'])
