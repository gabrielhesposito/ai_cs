# # with open('pdinout.csv') as f:
# #    for line in f:
# #         print line;
# #         exit(0);
import re

def clean_csv():
	handle = open('clean_csv.csv','w')
	with open('dirty.csv') as f:
		for line in f:
			p = re.compile(r'\s+')
			new = p.sub(',', line)
			new = new[:-1]
			handle.write(new)
			handle.write('\n')

clean_csv()
	
