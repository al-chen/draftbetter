import odds
import valuemaker
import writer
import datetime
import sys

# Run
if __name__ == "__main__":
	teams, predicted_pts = odds.getOdds()
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


