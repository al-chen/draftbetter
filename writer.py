import csv
import os
import datetime
import glob

cap = 50000

def writeIlp(exclude=[], csvname=None, filename=None, cap=50000):
	# Get most recent csv file of values
	if not csvname:
		csvname = max(glob.iglob('values' + '*.[Cc][Ss][Vv]'), key=os.path.getctime)
		t = os.path.getctime(csvname)
		fmt = "%Y-%m-%d"
		d = datetime.datetime.fromtimestamp(t)
		if d.strftime(fmt) != datetime.datetime.today().strftime(fmt):
			print("values CSV is not updated.")
			return [], [], [], []
	with open(csvname, 'rb') as csvValues:
		DKValues = csv.reader(csvValues, delimiter=',')
		players = []
		positions = []
		salaries = []
		values = []
		for row in DKValues:
			if row[0] == "Position":
				continue
			players.append(row[1])
			positions.append(row[0])
			salaries.append(int(row[2]))
			values.append(float(row[5]))

	# Remove players from exclude list
	for i in exclude:
		if i not in players:
			continue
		exclude_idx = players.index(i)
		players.pop(exclude_idx)
		positions.pop(exclude_idx)
		salaries.pop(exclude_idx)
		values.pop(exclude_idx)

	if not filename:
		filename = "ilp" + str(datetime.date.today())
	f = open(filename + ".py", 'w')
	f.write("from pulp import *\n\n")
	f.write("prob = LpProblem('NoName', LpMaximize)\n\n")

	for i in range(len(players)):
		f.write("p" + str(i) + """ = LpVariable("p""" + str(i) + """", 0, 1, 'Integer')\n""")

	# Objective
	f.write("\nprob += ")
	for i in range(len(players)):
		if i == len(players) - 1:
			f.write("p" + str(i) + "*" + str(values[i]) + "\n\n")
		else:
			f.write("p" + str(i) + "*" + str(values[i]) + " + ")

	# Must have 8 players
	f.write("prob += ")
	for i in range(len(players)):
		if i == len(players) - 1:
			f.write("p" + str(i) + " == 8\n")
		else:
			f.write("p" + str(i) + " + ")

	# At least 1 pg, 1 sg, 1 sf, 1 pf, 1 c
	# At most 3 pg, 3 sg, 3 sf, 3 pf, 2 c
	# At least 3 (pg+sg), 3 (sf+pf)
	# At most 4 (pg+sg), 4 (sf+pf)
	pg_str, sg_str, sf_str, pf_str, c_str = "", "", "", "", ""
	pglst, sglst, sflst, pflst, clst = [], [], [], [], []

	for i in range(len(players)):
		if positions[i] == "PG":
			pglst.append(i)
		elif positions[i] == "SG":
			sglst.append(i)
		elif positions[i] == "SF":
			sflst.append(i)
		elif positions[i] == "PF":
			pflst.append(i)
		elif positions[i] == "C":
			clst.append(i)
		else:
			print("ERROR: NO POSITION")

	for i in range(len(pglst)):
		pg_str += "p" + str(pglst[i])
		if i != len(pglst) - 1:
			pg_str += " + "

	for i in range(len(sglst)):
		sg_str += "p" + str(sglst[i])
		if i != len(sglst) - 1:
			sg_str += " + "

	for i in range(len(sflst)):
		sf_str += "p" + str(sflst[i])
		if i != len(sflst) - 1:
			sf_str += " + "

	for i in range(len(pflst)):
		pf_str += "p" + str(pflst[i])
		if i != len(pflst) - 1:
			pf_str += " + "

	for i in range(len(clst)):
		c_str += "p" + str(clst[i])
		if i != len(clst) - 1:
			c_str += " + "

	for i in [pg_str, sg_str, sf_str, pf_str, c_str]:
		if i == "":
			continue
		f.write("prob += " + i + " >= 1\n")
		if i == c_str:
			f.write("prob += " + i + " <= 2\n")	
		else:
			f.write("prob += " + i + " <= 3\n")

	for i in [pg_str + " + " + sg_str, sf_str + " + " + pf_str]:
		if i == "" or i[-1] == " ":
			continue
		f.write("prob += " + i + " >= 3\n")
		f.write("prob += " + i + " <= 4\n")

	# 0 <= Salary <= Cap (50,000)
	limit = ""
	for i in range(len(players)):
		limit += "p" + str(i) + "*" + str(salaries[i])
		if i != len(players) - 1:
			limit += " + "
	f.write("prob += " + limit + " >= " + str(0) + "\n")
	f.write("prob += " + limit + " <= " + str(cap) + "\n")

	f.write("prob.solve()\n")

	f.write("def fun():\n")
	f.write("    lst = []\n")
	for i in range(len(players)):
		f.write("    if value(p" + str(i) + ") == 1.0:\n")
		f.write("        lst.append(" + str(i) + ")\n")
	f.write("    return lst\n")
	f.close()
	return players, positions, salaries, values

# Run
# if __name__ == "__main__":
# 	exclude = []
# 	players, positions, salaries, values = writeIlp(exclude)
# 	ilp = __import__("ilp" + str(datetime.date.today()))
# 	output = ilp.fun()
# 	total_salary = 0
# 	total_value = 0
# 	for i in output:
# 		print players[i] + " (" + positions[i] + ") - V: " + str(values[i]) + " S: " + str(salaries[i]) + " 1kV/S: " + str(values[i] / salaries[i] * 1000)
# 		total_salary += salaries[i]
# 		total_value += values[i]
# 	print "Total Value: " + str(total_value)
# 	print "Total Salary: " + str(total_salary)
	# vs = sorted(players, key=lambda x: values[players.index(x)] / salaries[players.index(x)], reverse=True)
	# print vs

