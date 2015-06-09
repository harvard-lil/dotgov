import csv, re
from dateutil.parser import parse

def filter_dot_gov():

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

def add_links_to_ssrn():
	
	rows_with_ssrn_links = []
	dot_gov_addresses = 'results/dot-gov-addresses.csv'
	dot_gov_address_with_ssrn_links = 'results/dot_gov_address_with_ssrn_links.csv'


	with open(dot_gov_addresses, 'rb') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			ssrn_link = "Unknown"
			if "SSRN_ID" in row["Filename"]:
				 m = re.match(r"SSRN_ID(.+)_", row["Filename"])
				 if m:
					ssrn_link = "http://papers.ssrn.com/sol3/papers.cfm?abstract_id={0}".format(m.group(1))

			row["SSRN link"] = ssrn_link
			rows_with_ssrn_links.append(row)



	with open(dot_gov_address_with_ssrn_links, 'a') as csvfile:
		fieldnames = [u'URL in paper', u'Date file was last used', u'Filename', u'SSRN link',]
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()

		for row in rows_with_ssrn_links:
			writer.writerow(row)



add_links_to_ssrn()
