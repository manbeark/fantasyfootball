from sleeper.api import LeagueAPIClient
from sleeper.api import PlayerAPIClient
from sleeper.enum import Sport
from sleeper.model import (
    League,
    Roster,
    User,
    Matchup,
    PlayoffMatchup,
    Transaction,
    TradedPick,
    SportState,
)
import pandas as pd
from datetime import datetime as dt
import time
from brianpack import nfl
import locale


# dynasty league_id 960167583481688064
locale.setlocale( locale.LC_ALL, '' )

def update_header():
    week = nfl.current_week()
    period = nfl.week_period()
    if period == 1:
        if week == 1:
            return 'Today we kick off Week 1 of the 2023 season! Here are the matchups, remember to check your lineups:\n'
        else:
            return 'Today, Week ' + current_week() + ' begins! Check your lineups, here are the matchups:\n'
    elif period == 2:
        return 'We are heading towards 1pm kickoff! Make sure your lineups are in! Below are the matchups as they stand now:\n'
    elif period == 3:
        return 'The 1pm games are wrapping up, check the scores below:\n'
    elif period == 4:
        return 'The 4pm games are wrapping up, check the scores below:\n'
    elif period == 5:
        return "It's Monday morning, Week " + current_week() + ' is nearly over. Check the scores below:\n'
    elif period == 6:
        return "Remember to check out the final game of the week tonight!"
    elif period == 7:
        return "This week's games are now complete. Check the final scores, and earnings below:\n"
    elif period == 8:
        #return "It's Wednesday. This means that Waivers have cleared. SET YOUR LINEUP!\nAlso, see the season money totals below:\n"
        return "See the season money totals below:\n"
    elif period == 9:
        return "Check our first set of scores below:\n"

def week_data(league_id, week=nfl.current_week()):
    league = LeagueAPIClient.get_league(league_id=league_id)
    users = LeagueAPIClient.get_users_in_league(league_id=league_id)
    rosters = LeagueAPIClient.get_rosters(league_id=league_id)
    matchups = LeagueAPIClient.get_matchups_for_week(league_id=league_id,week=week)
    scoring_list = []
    for i in range(len(users)):
        # get the user id
        user_id = users[i].user_id
        # try to get team name
        try:
            team_name = users[i].metadata['team_name']
        # if it does not exist, it raises exception, so we use 'team ' + display name
        except:
            team_name = users[i].display_name
        # for each roster in the list of rosters
        for i in range(len(rosters)):
            # if the user owns the roster
            if user_id == rosters[i].owner_id:
                # get the roster id they own
                roster = rosters[i].roster_id
            # else check the next roster
            else:
                continue
        # for each matchup in list
        for i in range(len(matchups)):
            # check to see if user owns the roster
            if roster == matchups[i].roster_id:
                match_id = matchups[i].matchup_id
                points = matchups[i].points
        # add all of our details to the list using a list (so we get list of lists for dataframe)
        scoring_list.append([user_id, team_name, roster, match_id, points])
    headers = ['User_Id', 'Team_Name', 'Roster_Id', 'Matchup_Id', 'Points']
    df = pd.DataFrame(scoring_list, columns=headers)
    return df

def update_scoring(league_id, week=nfl.current_week()):
    df = week_data(league_id, week=week)
    matchup_message = []
    for i in range(1,7):
        match = df.loc[df['Matchup_Id'] == i]
        match = match.reset_index()
        x = str(match.at[0,'Team_Name']) + ' (' + str(match.at[0,'Points']) + ')'
        y = str(match.at[1,'Team_Name']) + ' (' + str(match.at[1,'Points']) + ')'
        matchup_message.append(x + ' vs. ' + y)
    # concoct one message
    message = ''
    for i in range(len(matchup_message)):
        message = message + matchup_message[i] + '\n'
    return message

def calculate_money(league_id, week=nfl.current_week()):
    df = week_data(league_id, week=week)
    for i in range(len(df.index)):
        if df.at[i, 'Points'] >= 120 and df.at[i, 'Points'] < 145:
            z = 1.0
        elif df.at[i, 'Points'] >= 145 and df.at[i, 'Points'] < 170:
            z = 2.5
        elif df.at[i, 'Points'] >= 170 and df.at[i, 'Points'] < 195:
            z = 5
        elif df.at[i, 'Points'] >= 195 and df.at[i, 'Points'] < 220:
            z = 7.5
        elif df.at[i, 'Points'] >= 220:
            z = 10
        else:
            z = 0
        df.at[i, 'Money'] = z
    matchup_message = []
    for i in range(1,7):
        match = df.loc[df['Matchup_Id'] == i]
        match = match.reset_index()
        x = str(match.at[0,'Team_Name']) + ' (' + str(match.at[0,'Points']) + ', $' + str(match.at[0,'Money']) + ')'
        y = str(match.at[1,'Team_Name']) + ' (' + str(match.at[1,'Points']) + ', $' + str(match.at[1,'Money']) + ')'
        matchup_message.append(x + ' vs. ' + y)
    # concoct one message
    message = ''
    for i in range(len(matchup_message)):
        message = message + matchup_message[i] + '\n'
    return message

def calculate_season_money(league_id):
    if nfl.current_week() > 14 or nfl.current_week == -1: # if current week is after Week 14
        week = 14 # just make it Week 14
    else: # else
        week = nfl.current_week() # use the current week
    for i in range(1,week + 1): # for each week
        df = week_data(league_id, week=i) # get the week data
        for j in range(len(df.index)): # for each row in the week data
            if df.at[j, 'Points'] >= 120 and df.at[j, 'Points'] < 145: # scoring 1
                z = 1.0
            elif df.at[j, 'Points'] >= 145 and df.at[j, 'Points'] < 170: # scoring 2.5
                z = 2.5
            elif df.at[j, 'Points'] >= 170 and df.at[j, 'Points'] < 195: # scoring 5
                z = 5
            elif df.at[j, 'Points'] >= 195 and df.at[j, 'Points'] < 220: # scoring 7.5
                z = 7.5
            elif df.at[j, 'Points'] >= 220: # scoring 10
                z = 10
            else: # scoring 0
                z = 0
            df.at[j, 'Week ' + str(i)] = z # assign the money total to the row
            if i == 1 and j == 0: # if its the first week
                money = df # use the df you just created as the template
            elif i > 1 and j == 0: # if its the second week but first of that week
                values = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
                money.insert(len(money.columns), 'Week ' + str(i), value=values) # insert a new column of zeros
                money.at[j, 'Week ' + str(i)] = z
            else:
                money.at[j, 'Week ' + str(i)] = z
    money.insert(5, 'Money Total', 0.0)
    for i in range(len(money.index)):
        total = 0
        for j in range(7,len(money.columns) + 1):
            total = total + money.at[i, 'Week ' + str(j - 6)]
        money.at[i, 'Money Total'] = total
    money.sort_values(by='Money Total',ascending=False,ignore_index=True,inplace=True)
    money.reset_index()
    money_message = []
    for i in range(len(money.index)):
        money_message.append(money.at[i, 'Team_Name'] + ': ' + locale.currency(money.at[i, 'Money Total'],grouping=True))
    message = ''
    for i in range(len(money_message)):
        message = message + '\n' + money_message[i]
    return message

def get_transactions(league_id, week=nfl.current_week()):
    return LeagueAPIClient.get_transactions(league_id=league_id, week=nfl.current_week())

def get_players():
    return PlayerAPIClient.get_all_players(sport=Sport.NFL)