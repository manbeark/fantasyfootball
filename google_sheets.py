import gspread, gspread_dataframe as gsdf
import sleeper
import pandas as pd


class Roster:
	def __init__(self, file_name, sheet_name):
		sa = gspread.service_account()
		self.file = sa.open(file_name)
		self.sheet = self.file.worksheet(sheet_name)
		self.dataframe = pd.DataFrame(self.sheet.get_all_records())
		self.dataframe = self.dataframe[0:len(self.dataframe.index) - 4]

	def __str__(self):
		return 'DataFrame containing roster for ' + sheet_name + '.'



# functions for storing data
def dyn_commit_transactions(league_id, file_name, sheet_name, week=nfl.current_week()):
	transactions = sleeper.get_transactions(league_id=league_id, week=week)
	for i in range(len(transactions)): # for each transaction
		if transactions[i].type == "<TransactionType.WAIVER: 'WAIVER'>":
			# do stuff
		elif transactions[i].type == "<TransactionType.TRADE: 'TRADE'>":
			# do stuff
		elif transactions[i].type == "<TransactionType.FREE_AGENT: 'FREE_AGENT'>":
			# do stuff
		else:
			# raise some error 