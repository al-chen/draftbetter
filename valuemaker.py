from bs4 import BeautifulSoup
from urllib import *
import heapq
import math
import glob
import os
import datetime
import csv


# contest_link = 'https://www.draftkings.com/contest/draftteam/6633768'

# html = urlopen(contest_link).read()
# soup = BeautifulSoup(html)

# type_index = html.find("contestTypeId")
# type_end = html.find(",", type_index)
# contestTypeId = html[type_index+14:type_end].strip()
# print contestTypeId

# id_index = html.find("draftGroupId", type_end)
# id_end = html.find(",", id_index)
# draftGroupId = html[id_index+13:id_end].strip()
# print draftGroupId

# contest_values = urlopen("https://www.draftkings.com/lineup/getavailableplayerscsv?contestTypeId=" + contestTypeId + "&draftGroupId=" + draftGroupId)
# cr = csv.reader(contest_values)
# for row in cr:
# 	print row

# teams = ['GSW', 'HOU']
# predicted_pts = [109.25, 104.75]
# for i in range(0,len(teams),2):
# 	away_team = teams[i]
# 	home_team = teams[i+1]
# 	away_predicted = predicted_pts[i]
# 	home_predicted = predicted_pts[i+1]

# 	year = str(datetime.date.today().year)
# 	if datetime.date.today().month >= 8:
# 		year += 1
# 	away_url = "http://www.basketball-reference.com/teams/" + away_team + "/" + year + ".html" 
# 	away_html = urlopen(away_url).read()
# 	# soup = BeautifulSoup(html)

# 	pts_index = away_html.find("PTS/G") + 14
# 	pts_end = away_html.find(" ", pts_index)
# 	away_ptsg = float(away_html[pts_index:pts_end])

# 	pts_index = away_html.find("Opp PTS/G") + 18
# 	pts_end = away_html.find(" ", pts_index)
# 	away_opp_ptsg = float(away_html[pts_index:pts_end])

# 	pts_index = away_html.find("Off Rtg") + 20
# 	pts_end = away_html.find(" ", pts_index)
# 	away_off_rtg = float(away_html[pts_index:pts_end])

# 	pts_index = away_html.find("Def Rtg") + 20
# 	pts_end = away_html.find(" ", pts_index)
# 	away_def_rtg = float(away_html[pts_index:pts_end])

# 	home_url = "http://www.basketball-reference.com/teams/" + home_team + "/" + year + ".html" 
# 	home_html = urlopen(home_url).read()
# 	# soup = BeautifulSoup(html)

# 	pts_index = home_html.find("PTS/G") + 14
# 	pts_end = home_html.find(" ", pts_index)
# 	home_ptsg = float(home_html[pts_index:pts_end])

# 	pts_index = home_html.find("Opp PTS/G") + 18
# 	pts_end = home_html.find(" ", pts_index)
# 	home_opp_ptsg = float(home_html[pts_index:pts_end])

# 	pts_index = home_html.find("Off Rtg") + 20
# 	pts_end = home_html.find(" ", pts_index)
# 	home_off_rtg = float(home_html[pts_index:pts_end])

# 	pts_index = home_html.find("Def Rtg") + 20
# 	pts_end = home_html.find(" ", pts_index)
# 	home_def_rtg = float(home_html[pts_index:pts_end])

# 	away_factor = 0.5
# 	home_factor = 0.5
# 	# away_predicted, away_ptsg, home_opp_ptsg
# 	if away_predicted > away_ptsg:
# 		if away_ptsg > home_opp_ptsg:
# 			away_factor = 0.0
# 			home_factor = 1.0



# def getValues(teams, predicted_pts, contest_link):


def getValues(teams, predicted_pts):
	dic = {0:0}
	for i in range(1,11):
		dic[i] = dic[i-1] + math.pow(3,i-1)
	dic[11] = dic[10]
	total = dic[10]
	value_map = {}

	for a in range(len(teams)):
		team_abbrev = teams[a]
		team_predicted_pts = predicted_pts[a]
		year = str(datetime.date.today().year)
		if datetime.date.today().month >= 8:
			year += 1
		URL = "http://www.basketball-reference.com/teams/" + team_abbrev + "/" + year + ".html" 
		html = urlopen(URL).read()
		# html = str(BeautifulSoup(html))
		off_rtg_idx = html.find("Off Rtg") + 20
		off_rtg = ""
		while True:
			if html[off_rtg_idx] == " ":
				off_rtg = float(off_rtg)
				break
			off_rtg += html[off_rtg_idx]
			off_rtg_idx += 1
		num_poss = 100 * team_predicted_pts / off_rtg

		start_idx = html.find("""style="">Per 100 Poss</h2>""")
		end_idx = html.find("""style="">Advanced</h2>""")
		searchspace = html[start_idx:end_idx]
		name_idx = 0
		while True:
			name_idx = searchspace.find(""".html">""", name_idx) + 7
			if name_idx == 6:
				break
			name_end = searchspace.find("</a>", name_idx)
			name = searchspace[name_idx:name_end]

			age, next_idx = findStat(searchspace, name_idx)
			# age = int(age)
			g, next_idx = findStat(searchspace, next_idx)
			# g = int(g)
			gs, next_idx = findStat(searchspace, next_idx)
			# gs = int(gs)
			mp, next_idx = findStat(searchspace, next_idx)
			fg, next_idx = findStat(searchspace, next_idx)
			fga, next_idx = findStat(searchspace, next_idx)
			fgp, next_idx = findStat(searchspace, next_idx)
			threes_made, next_idx = findStat(searchspace, next_idx)
			threes_att, next_idx = findStat(searchspace, next_idx)
			threes_fgp, next_idx = findStat(searchspace, next_idx)
			twos_made, next_idx = findStat(searchspace, next_idx)
			twos_att, next_idx = findStat(searchspace, next_idx)
			twos_fgp, next_idx = findStat(searchspace, next_idx)
			ft, next_idx = findStat(searchspace, next_idx)
			fta, next_idx = findStat(searchspace, next_idx)
			ftp, next_idx = findStat(searchspace, next_idx)
			orb, next_idx = findStat(searchspace, next_idx)
			drb, next_idx = findStat(searchspace, next_idx)
			trb, next_idx = findStat(searchspace, next_idx)
			ast, next_idx = findStat(searchspace, next_idx)
			stl, next_idx = findStat(searchspace, next_idx)
			blk, next_idx = findStat(searchspace, next_idx)
			tov, next_idx = findStat(searchspace, next_idx)
			pf, next_idx = findStat(searchspace, next_idx)
			pts, next_idx = findStat(searchspace, next_idx)
			ortg, next_idx = findStat(searchspace, next_idx)
			drtg, next_idx = findStat(searchspace, next_idx)
			pred_pts = pts / 100 * num_poss * mp / g / 48
			pred_3p = threes_made / 100 * num_poss * mp / g / 48
			pred_reb = trb / 100 * num_poss * mp / g / 48
			pred_ast = ast / 100 * num_poss * mp / g / 48
			pred_stl = stl / 100 * num_poss * mp / g / 48
			pred_blk = blk / 100 * num_poss * mp / g / 48
			pred_tov = tov / 100 * num_poss * mp / g / 48

			candidates = [pred_pts, pred_reb, pred_ast, pred_blk, pred_stl]
			biggest_3 = heapq.nlargest(3, candidates)
			probability_3 = []
			for i in biggest_3:
				if i > 10.0:
					i = 10.0
				left = int(i)
				right = i - left
				numerator = dic[left] + right * (dic[left+1] - dic[left])
				probability_3.append(numerator / total)
			pred_doubledouble = probability_3[0] * probability_3[1]
			pred_tripledouble = probability_3[0] * probability_3[1] * probability_3[2]
			
			pred_value = pred_pts + (0.5 * pred_3p) + (1.25 * pred_reb) + (1.5 * pred_ast) + (2.0 * pred_stl) + (2.0 * pred_blk) - (0.5 * pred_tov)
			pred_value += (1.5 * pred_doubledouble) + (3.0 * pred_tripledouble)

			# Hard-coded name change
			if name == "Dennis Schr&ouml;der":
				name = "Dennis Schroder"
			elif name == "Patrick Mills":
				name = "Patty Mills"
			value_map[name] = pred_value

			# print "age: " + str(age)
			# print "g: " + str(g)
			# print "gs: " + str(gs)
			# print "mp: " + str(mp)
			# print "fg: " + str(fg)
			# print "fga: " + str(fga)
			# print "fgp: " + str(fgp)
			# print "3m: " + str(threes_made)
			# print "threes_att: " + str(threes_att)
			# print "thress_fgp: " + str(threes_fgp)
			# print "twos_made: " + str(twos_made)
			# print "twos_att: " + str(twos_att)
			# print "twos_fgp: " + str(twos_fgp)
			# print "ft: " + str(ft)
			# print "fta: " + str(fta)
			# print "ftp: " + str(ftp)
			# print "orb: " + str(orb)
			# print "drb: " + str(drb)
			# print "trb: " + str(trb)
			# print "ast: " + str(ast)
			# print "stl: " + str(stl)
			# print "blk: " + str(blk)
			# print "tov: " + str(tov)
			# print "pf: " + str(pf)
			# print "pts: " + str(pts)
			# print "ortg: " + str(ortg)
			# print "drtg: " + str(drtg)

			# print pred_pts
			# print pred_3p
			# print pred_reb
			# print pred_ast
			# print pred_stl
			# print pred_blk
			# print pred_tov

	csvname = max(glob.iglob('DKSalaries' + '*.[Cc][Ss][Vv]'), key=os.path.getctime)
	t = os.path.getctime(csvname)
	fmt = "%Y-%m-%d"
	d = datetime.datetime.fromtimestamp(t)
	if d.strftime(fmt) != datetime.datetime.today().strftime(fmt):
		print("DKSalaries CSV is not updated.")
		return
	valuefile = "values" + str(datetime.date.today())
	with open(valuefile + ".csv", 'wb') as csvValues:
		DKValues = csv.writer(csvValues, delimiter=',')
		with open(csvname, 'rb') as csvDKSalaries:
			DKSalaries = csv.reader(csvDKSalaries, delimiter=',')
			for row in DKSalaries:
				if row[0] == "Position":
					# print(row + ["Predicted Value"])
					DKValues.writerow(row + ["Predicted Value"])
				else:
					name = row[1]
					if name not in value_map:
						print("Player " + name + " is not in value_map.")
						continue
					# print(row + [value_map[name]])
					DKValues.writerow(row + [str(value_map[name])])

def findStat(searchspace, initial_idx):
	idx = searchspace.find("""<td align="right" >""", initial_idx) + 19
	if searchspace[idx:idx+2] == "<a":
		idx = searchspace.find(">", idx) + 1
		# final = searchspace.find(">", idx)
		# link = "http://www.basketball-reference.com"
		# link += searchspace[idx+9:final-1]
		# g_final = searchspace.find("<", final)
		# g = float(searchspace[final+1:g_final])
		# return link, g, final
	if searchspace[idx] == "<":
		return 0.0, idx
	end = searchspace.find("<", idx+1)
	return float(searchspace[idx:end]), end

if __name__ == "__main__":
	teams = ["LAL"]
	predicted_pts = [102.0]
	getValues(teams,predicted_pts)