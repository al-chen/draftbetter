from urllib import *

def check(team_abbrev):
	URL = "http://www.basketball-reference.com/teams/" + team_abbrev + "/2015.html" 
	html = urlopen(URL).read()
	# html = str(BeautifulSoup(html))

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
		good = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.-' "
		for i in name:
			if i not in good:
				print name
				break

abbreviations = ["ATL", "BRK", "BOS", "CHO", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHO", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"]
for i in abbreviations:
	print i
	check(i)