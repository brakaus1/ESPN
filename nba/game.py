import urllib2
from bs4 import BeautifulSoup


class Game:

    def __init__(self, gameId):
        self.gameId = gameId

    def getPlayByPlay(self):

                
        html = urllib2.urlopen( "http://www.google.com" ).read()
        soup = BeautifulSoup( html )
        return soup.find_all(class_='mod-data')
