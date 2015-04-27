import csv
from dateutil.parser import parse

year_counts = {}

rows_with_dot_gov_addresses = []
results_file = 'results/raw-urls.csv'
dot_gov_addresses = 'results/dot-gov-addresses.csv'

with open(results_file, 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		if ".gov" in row["URL in paper"]:
			rows_with_dot_gov_addresses.append(row)
			p = parse(row["Date file was last used"])
			if p.year in year_counts:
				year_counts[p.year]+=1
			else:
				year_counts[p.year]=0



with open(dot_gov_addresses, 'a') as csvfile:
	fieldnames = [u'URL in paper', u'Date file was last used', u'Filename',]
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()

	for row in rows_with_dot_gov_addresses:
		writer.writerow(row)


print year_counts