import requests
from datetime import datetime as dt


# function to retrieve the league overview
def get_league(league_id,swid,espn_s2,year):
	url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/' + str(year) + '/segments/0/leagues/' + str(league_id)
	r = requests.get(url,cookies={"SWID": swid, "espn_s2": espn_s2})
	d = r.json()
	return d

# function to retrieve teams
def get_teams(league_id,swid,espn_s2,year):
	url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/' + str(year) + '/segments/0/leagues/' + str(league_id)
	r = requests.get(url,cookies={"SWID": swid, "espn_s2": espn_s2},params = {'view' : 'mTeam'})
	d = r.json()
	return d

# class for the league overview object
class League:
	year_now = dt.now().strftime('%Y')
	def __init__(self,league_id,swid,espn_s2,year=year_now):
		self.league = get_league(league_id,swid,espn_s2,year)
		self.gameId = self.league['gameId']
		self.id = self.league['id']
		self.members = self.league['members']
		for i in range(len(self.members)):
			self.members[i] = Member(self.members[i])
		self.scoringPeriodId = self.league['scoringPeriodId']
		self.seasonId = self.league['seasonId']
		self.segmentId = self.league['segmentId']
		self.settings = Settings(self.league['settings']) # class
		self.status = Status(self.league['status']) # class
		self.teams = self.league['teams']
		for i in range(len(self.teams)):
			self.teams[i] = Team(self.teams[i])

# class for a team from the mTeam object
class Team:
	def __init__(self, team):
		self.abbrev = team['abbrev']
		self.currentProjectedRank = team['currentProjectedRank']
		self.divisionId = team['divisionId']
		self.draftDayProjectedRank = team['draftDayProjectedRank']
		self.draftStrategy = team['draftStrategy'] # class
		self.id = team['id']
		self.isActive = team['isActive']
		self.location = team['location']
		self.logo = team['logo']
		self.logoType = team['logoType']
		self.name = team['name']
		self.nickname = team['nickname']
		self.owners = team['owners']
		self.playoffSeed = team['playoffSeed']
		self.points = team['points']
		self.pointsAdjusted = team['pointsAdjusted']
		self.pointsDelta = team['pointsDelta']
		self.primaryOwner = team['primaryOwner']
		self.rankCalculatedFinal = team['rankCalculatedFinal']
		self.rankFinal = team['rankFinal']
		self.record = team['record'] # class
		self.tradeBlock = team['tradeBlock']
		self.transactionCounter = team['transactionCounter'] # class
		self.valuesByStat = team['valuesByStat'] # class
		self.waiverRank = team['waiverRank']
	def __str__(self):
		return self.location + ' ' + self.nickname

# class for draft strategy from the mTeam object
class DraftStrategy:
	def __init__(self, draftStrategy):
		self.futureKeeperPlayerIds = draftStrategy['futureKeeperPlayerIds']
		self.keeperPlayerIds = draftStrategy['keeperPlayerIds']

# class for record statistics from the mTeam object
class Record:
	def __init__(self, record):
		self.away_stats = TeamStats(record['away'])
		self.division_stats = TeamStats(record['division'])
		self.home_stats = TeamStats(record['home'])
		self.overall_stats = TeamStats(record['overall'])

class TeamStats:
	def __init__(self, stats):
		self.games_back = stats['gamesBack']
		self.losses = stats['losses']
		self.percentage = stats['percentage']
		self.points_against = stats['pointsAgainst']
		self.points_for = stats['pointsFor']
		self.streak_length = stats['streakLength']
		self.streak_type = stats['streakType']
		self.ties = stats['ties']
		self.wins = stats['wins']
	def __str__(self):
		points = 'Points For/Against: ' + self.points_for + '/' + self.points_against
		record_sub = 'Record: ' + self.wins + '-' + self.losses
		if self.ties == 0:
			record = record_sub
		else:
			record = record_sub + '-' + self.ties
		return points + '\n' + record

# class for a league member from the league object
class Member:
	def __init__(self, member):
		self.displayName = member['displayName']
		self.id = member['id']
		self.isLeagueManager = member['isLeagueManager']
	def __str__(self):
		return self.displayName

# class for settings from the league object
class Settings:
	def __init__(self, settings):
		self.name = settings['name']

# class for the status from the league object
class Status:
	def __init__(self, status):
		self.currentMatchupPeriod = status['currentMatchupPeriod']
		self.isActive = status['isActive']
		self.latestScoringPeriod = status['latestScoringPeriod']

class Teams:
	year_now = dt.now().strftime('%Y')
	def __init__(self,league_id,swid,espn_s2,year=year_now):
		self.teams = get_teams(league_id,swid,espn_s2,year)
		self.draftDetail = self.teams['draftDetail']
		self.gameId = self.teams['gameId']
		self.members = self.teams['members']
		for i in range(len(self.members)):
			self.members[i] = Member(self.members[i])
		self.scoringPeriodId = self.teams['scoringPeriodId']
		self.seasonId = self.teams['seasonId']
		self.segmentId = self.teams['segmentId']
		self.status = Status(self.teams)
		for i in range(len(self.teams['teams'])):
			self.team = Team(self.teams['teams'][i])

class TeamMember:
	# class to get the league member from mTeam
	def __init__(self, team_member):
		self.displayNam
