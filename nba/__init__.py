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
                    elif home_team.split(' ')[1] in row[1].text:
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

    def getBoxScore(self, game_id):

        url = "http://espn.go.com/nba/boxscore?gameId={}".format(game_id)
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html)

        rows = soup.find_all(['thead', 'tbody'])
        away_team = rows[0].th.text
        home_team = rows[6].th.text

        def get_player_dict(soup_row, starter=True):

            ret = {}
            cols = soup_row.find_all('td')
            player = (cols[0].a.get('href').split('/')[-2], cols[0].a.text)
            pos = cols[0].text.split(',')[1].strip()
            if len(cols) < 4:
                return {'player': player, 'pos': pos, 'minutes': 0, 'DNP': cols[1].text}
            minutes = int(cols[1].text)
            fgm, fga = map(int, cols[2].text.split('-'))
            fgm3, fga3 = map(int, cols[3].text.split('-'))
            ftm, fta = map(int, cols[4].text.split('-'))
            oreb = int(cols[5].text)
            dreb = int(cols[6].text)
            reb = int(cols[7].text)
            ast = int(cols[8].text)
            stl = int(cols[9].text)
            blk = int(cols[10].text)
            to = int(cols[11].text)
            pf = int(cols[12].text)
            plus_minus = int(cols[13].text)
            pts = int(cols[6].text)
            ret = {'player': player,
                   'pos': pos,
                   'min': minutes,
                   'min': minutes,
                   'fgm': fgm,
                   'fga': fga,
                   'fgm3': fgm3,
                   'fga3': fga3,
                   'ftm': ftm,
                   'fta': fta,
                   'oreb': oreb,
                   'dreb': dreb,
                   'reb': reb,
                   'ast': ast,
                   'stl': stl,
                   'blk': blk,
                   'to': to,
                   'pf': pf,
                   'plus_minus': plus_minus,
                   'pts': pts,
                   'starter': starter
                   }
            return ret

        away_players = []
        home_players = []

        for player in rows[1].find_all('tr'):
            away_players.append(get_player_dict(player))
        for player in rows[3].find_all('tr'):
            away_players.append(get_player_dict(player, starter=False))

        for player in rows[7].find_all('tr'):
            home_players.append(get_player_dict(player))
        for player in rows[9].find_all('tr'):
            home_players.append(get_player_dict(player, starter=False))

        ret_dict = {}
        ret_dict['away_team'] = away_team
        ret_dict['home_team'] = home_team
        ret_dict['away_players'] = away_players
        ret_dict['home_players'] = home_players

        return ret_dict
