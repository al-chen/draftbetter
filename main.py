from urllib import *
import valuemaker
import writer
import datetime
import sys

city_list = ["Atlanta", "Brooklyn", "Boston", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"]
team_list = ["Hawks", "Nets", "Celtics", "Hornets", "Bulls", "Cavaliers", "Mavericks", "Nuggets", "Pistons", "Warriors", "Rockets", "Pacers", "Clippers", "Lakers", "Grizzlies", "Heat", "Bucks", "Timberwolves", "Pelicans", "Knicks", "Thunder", "Magic", "76ers", "Suns", "Trail Blazers", "Kings", "Spurs", "Raptors", "Jazz", "Wizards"]
team_to_abbr = {'Pistons': 'DET', 'Kings': 'SAC', 'Chicago': 'CHI', 'Thunder': 'OKC', 'Warriors': 'GSW', 'Hawks': 'ATL', 'Minnesota': 'MIN', 'Denver': 'DEN', 'Timberwolves': 'MIN', 'Wizards': 'WAS', 'Knicks': 'NYK', 'Indiana': 'IND', 'Golden State': 'GSW', 'Nuggets': 'DEN', 'Hornets': 'CHO', 'Phoenix': 'PHO', 'Cavaliers': 'CLE', 'Sacramento': 'SAC', 'Dallas': 'DAL', 'Utah': 'UTA', 'Heat': 'MIA', 'Clippers': 'LAC', 'Bulls': 'CHI', 'Brooklyn': 'BRK', 'New York': 'NYK', 'Mavericks': 'DAL', 'Pelicans': 'NOP', 'Celtics': 'BOS', 'Trail Blazers': 'POR', 'Atlanta': 'ATL', 'Memphis': 'MEM', 'San Antonio': 'SAS', 'Toronto': 'TOR', 'Magic': 'ORL', 'LA Lakers': 'LAL', 'Charlotte': 'CHO', 'Miami': 'MIA', 'Grizzlies': 'MEM', 'LA Clippers': 'LAC', 'Orlando': 'ORL', 'Detroit': 'DET', 'Philadelphia': 'PHI', 'Pacers': 'IND', 'Rockets': 'HOU', 'Lakers': 'LAL', 'Bucks': 'MIL', 'Raptors': 'TOR', 'Oklahoma City': 'OKC', 'Spurs': 'SAS', 'Houston': 'HOU', '76ers': 'PHI', 'Suns': 'PHO', 'Boston': 'BOS', 'Washington': 'WAS', 'New Orleans': 'NOP', 'Cleveland': 'CLE', 'Milwaukee': 'MIL', 'Portland': 'POR', 'Nets': 'BRK', 'Jazz': 'UTA', 'NY Knicks': 'NYK'}

def getOdds():
	URL = """http://espn.com/nba/lines"""
	html = urlopen(URL).read()
	idx = 0
	glossry_idx = html.find("<h5>Glossary</h5>")

	teams = []
	predicted_pts = []

	while True:
		idx = html.find("""<td colspan="5">""", idx) + 16
		if idx == 15:
			break
		matchup_end = html.find("<", idx)
		if html[idx:matchup_end] == "Daily Lines":
			print("Daily lines are currently available")
			break
		first_team = ""
		running_idx = idx
		while True:
			if first_team in team_to_abbr:
				break
			first_team += html[running_idx]
			running_idx += 1
		if len(first_team) > 30:
			print("First team not found")
			break
		first_abbr = team_to_abbr[first_team]

		second_idx = html.find("at", running_idx) + 3
		second_end = html.find(",", second_idx)
		second_team = html[second_idx:second_end]
		if len(second_team) > 30:
			print("Second team not found")
			break
		second_abbr = team_to_abbr[second_team]

		spread = None
		total = None
		site_idx = second_end
		for sitename in ["BETONLINE.ag", "SportsBetting.ag", "BOVADA", "Fantasy911.com"]:
			site_idx = html.find(sitename, second_end)
			a = html.find("""<td style="text-align:center;">""", site_idx) + 31
			if html[a:a+4] == "EVEN":
				spread = 0.0
			else:
				b = html.find("""<td width="50%">""", a) + 16
				b_end = html.find("<", b)
				b_content = html[b:b_end]
				b_content = b_content.replace("+","",1)
				if not b_content.replace(".","",1).replace("-","",1).isdigit():
					print "Spread Error"
					break
				spread = float(b_content)
			spread_end = html.find("</td>", a) + 36
			if html[spread_end:spread_end+3] == "N/A":
				total = 0.0
				for abbrev in [first_abbr, second_abbr]:
					team_url = "http://www.basketball-reference.com/teams/" + abbrev + "/2015.html" 
					team_html = urlopen(team_url).read()
					ptsg_idx = team_html.find("PTS/G:") + 14
					ptsg_end = team_html.find(" ", ptsg_idx)
					total += float(team_html[ptsg_idx:ptsg_end])
			else:
				c = html.find("""<table cellspacing="1" cellpadding="3" class="tablehead"><tr><td width="50%">""", b_end) + 77
				if html[c:c+3].isdigit():
					total = float(html[c:c+3])
			if spread != None and total != None:
				break
		first_points = second_points = total / 2
		first_points -= spread / 2
		second_points += spread / 2
		teams.append(first_abbr)
		teams.append(second_abbr)
		predicted_pts.append(first_points)
		predicted_pts.append(second_points)
	return teams, predicted_pts

# Run
if __name__ == "__main__":
	teams, predicted_pts = getOdds()
	valuemaker.getValues(teams, predicted_pts)
	exclude = sys.argv[1:] + []
	players, positions, salaries, values = writer.writeIlp(exclude)
	if not players or not positions or not salaries or not values:
		sys.exit("Error")
	ilp = __import__("ilp" + str(datetime.date.today()))
	output = ilp.fun()
	total_salary = 0
	total_value = 0
	print("Lineup")
	for i in output:
		print players[i] + " (" + positions[i] + ")" # - V: " + str(values[i]) + " S: " + str(salaries[i]) + " 1kV/S: " + str(values[i] / salaries[i] * 1000)
		total_salary += salaries[i]
		total_value += values[i]
	print "Total Value: " + str(total_value)
	print "Total Salary: " + str(total_salary)
	# vs = sorted(players, key=lambda x: values[players.index(x)] / salaries[players.index(x)], reverse=True)
	# print vs


