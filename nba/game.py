import urllib2
from bs4 import BeautifulSoup


class Game:

    def __init__(self, gameId):
        self.gameId = gameId

    def getPlayByPlay(self):

        html = urllib2.urlopen("http://www.google.com").read()
        soup = BeautifulSoup(html)

        awayTeam = soup.find_all(style='text-align:left;')[0].text + ' ' + soup.find_all(class_="team away")[0].a.text
        homeTeam = soup.find_all(style='text-align:left;')[1].text + ' ' + soup.find_all(class_="team home")[0].a.text
        period = 1
        ret = []

        for play in soup.find_all(class_=['even', 'odd']):

            row = play.find_all('td')
            rowDict = {}

            if len(row) == 2:

                if 'timeout' in row[1].text.lower():
                    rowDict['play'] = 'timeout'
                    rowDict['period'] = period
                    rowDict['min'], rowDict['sec'] = map(int, row[0].text.split(':'))
                    if 'Official' in row[1].text:
                        rowDict['team'] = 'Official'
                    elif homeTeam.split(' ')[1] in row[1].text:
                        rowDict['team'] = homeTeam.lower()
                    else:
                        rowDict['team'] = awayTeam.lower()
                    ret.append(rowDict)
                elif 'quarter' in row[1].text.lower() or 'overtime' in row[1].text.lower():
                    period += 1

            else:
                rowDict['period'] = period
                rowDict['min'], rowDict['sec'] = map(int, row[0].text.split(':'))
                if row[1].text == '\xa0':
                    rowDict['team'] = homeTeam.lower()
                    rowDict['play'] = row[3].text
                else:
                    rowDict['team'] = awayTeam.lower()
                    rowDict['play'] = row[1].text
                ret.append(rowDict)
        return ret
