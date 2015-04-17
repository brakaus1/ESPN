import urllib2
from bs4 import BeautifulSoup


class Game:

    def __init__(self, gameId):
        self.gameId = gameId

    def getPlayByPlay(self):

        e = 'http://espn.go.com/nba/boxscore?gameId=400579520'
        return
