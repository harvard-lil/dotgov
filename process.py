import os, re, time, csv
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


dir = '/Users/phillipsm/dev_area/dotgov/arn'
results_file = 'results/raw-urls.csv'
#url_pattern = re.compile('(https?://\S+)')
# We don't want to count the self referential links in the footer of
# some of the papers
url_pattern = re.compile('(?<!lectronic copy available at: )(https?://\S+)')

def write_data_to_file(file_name, date, urls):
	with open(results_file, 'a') as csvfile:
		fieldnames = [u'URL in paper', u'Date file was last used', u'Filename',]
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		#writer.writeheader()

		for url in urls:

			row = {'Filename': file_name, 'Date file was last used': date, 'URL in paper': url}
			writer.writerow(row)


def convert_pdf_to_txt(path):
	# Thank you, http://stackoverflow.com/a/26766684
	rsrcmgr = PDFResourceManager()
	retstr = StringIO()
	codec = 'utf-8'
	laparams = LAParams()
	device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

	with open(path, 'rb') as fp:

		#fp = file(path, 'rb')
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		password = ""
		maxpages = 0
		caching = True
		pagenos=set()
		for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,password=password,caching=caching, check_extractable=True):
			interpreter.process_page(page)

		text = retstr.getvalue()

		#fp.close()
	device.close()
	retstr.close()
	return text

number_of_files_processed = 0
number_of_files_with_problems = 0

for fn in os.listdir('./arn'):

	if number_of_files_processed > 1 and (number_of_files_processed + number_of_files_with_problems) % 100 == 0:
		print "\n%i files processed successfully" % number_of_files_processed
		print "%i files processed unsuccessfully\n" % number_of_files_with_problems

	relative_file_path = './arn/%s' % fn
	if os.path.isfile(relative_file_path):

		try:
			text_from_pdf = convert_pdf_to_txt(relative_file_path)
			number_of_files_processed+=1
		except:
			print "Problems processing %s " % relative_file_path
			number_of_files_with_problems+=1
			continue

		print "processing %s" % relative_file_path
		file_last_create_time = time.ctime(os.stat(relative_file_path)[8])
		#print "last modified: %s" % file_last_create_time

		if re.findall(url_pattern, text_from_pdf):
			#print re.findall(url_pattern, text_from_pdf)
			write_data_to_file(fn, file_last_create_time, re.findall(url_pattern, text_from_pdf))



print "Done! Final numbers:\n\n"
print "%i of files processed successfully" % number_of_files_processed
print "%i of files processed unsuccessfully" % number_of_files_with_problems