import urllib2
from bs4 import BeautifulSoup


class NBA:

    def getTeams(self):

        html = urllib2.urlopen('http://espn.go.com/nba/teams').read()
        soup = BeautifulSoup(html)
        self.teams = {}
        for team in soup.find_all(class_='bi'):
            self.teams[team.get('href').split('/')[-2]] = team.text

    def getRegularSeasonGameIds(self, season_year, team_abr):
        url = 'http://espn.go.com/nba/team/schedule/_/name/{team}/year/{season}/seasontype/2'.format(team=team_abr, season=season_year)
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html)
        ret = []
        for game in soup.find_all(class_='score'):
            ret.append(game.a.get('href').split('=')[1])
        return ret

    def getTeamRegularSeasonPlayByPlays(self, season_year, team_abr):
        pbps = []
        for game in self.getRegularSeasonGameIds(season_year, team_abr):
            pbps.append(self.getPlayByPlay(game))
        return pbps

    def getAllSeasonGameIds(self, season):
        game_ids = set([])
        for team in self.getTeams().keys():
            for game_id in self.getRegularSeasonGameIds(season, team):
                game_ids.add(game_id)
        return game_ids

    def getAllSeasonPBPs(self, season):
        pbps = []
        for game in self.getAllSeasonGameIds():
            pbps.append(self.getPlayByPlay(game))
        return pbps

    def getPlayByPlay(self, game_id):

        url = "http://espn.go.com/nba/playbyplay?gameId={}&period=0".format(game_id)
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html)

        away_team = soup.find_all(style='text-align:left;')[0].text + ' ' + soup.find_all(class_="team away")[0].a.text
        home_team = soup.find_all(style='text-align:left;')[1].text + ' ' + soup.find_all(class_="team home")[0].a.text
        period = 1
        ret = []

        for play in soup.find_all(class_=['even', 'odd']):

            row = play.find_all('td')
            row_dict = {}

            if len(row) == 2:

                if 'timeout' in row[1].text.lower():
                    row_dict['play'] = 'timeout'
                    row_dict['period'] = period
                    row_dict['min'], row_dict['sec'] = map(int, row[0].text.split(':'))
                    if 'Official' in row[1].text:
                        row_dict['team'] = 'Official'
                    elif homeTeam.split(' ')[1] in row[1].text:
                        row_dict['team'] = home_team.lower()
                    else:
                        row_dict['team'] = away_team.lower()
                    ret.append(row_dict)
                elif 'quarter' in row[1].text.lower() or 'overtime' in row[1].text.lower():
                    period += 1

            else:
                row_dict['period'] = period
                row_dict['min'], row_dict['sec'] = map(int, row[0].text.split(':'))
                if row[1].text == u'\xa0':
                    row_dict['team'] = home_team.lower()
                    row_dict['play'] = row[3].text
                else:
                    row_dict['team'] = away_team.lower()
                    row_dict['play'] = row[1].text
                ret.append(row_dict)
        return ret
