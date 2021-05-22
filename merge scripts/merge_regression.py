from tkinter.filedialog import askdirectory
import os
from math import sqrt
import xlrd
import xlwt
from datetime import datetime

# Give the location of the file 
path = askdirectory(initialdir='/Users/tizianasvenningsen/Dropbox/Uni/Bachelor projekt/Matlap/Package_IDcfu_Picking/DONE')
wb = xlwt.Workbook()
ws = wb.add_sheet('Sheet 1') 
first = True

row = 0

def process(path):
	global first
	global row
	print("\t"+path)
	for f in os.scandir(path):
		if f.is_dir():
			process(f.path)
	for filename in os.listdir(path):
		print("\t- "+filename)
		if filename.endswith(".xls") and "means" not in filename and "stddev" not in filename:
			book = xlrd.open_workbook(path+"/"+filename)
			sheets = book.sheets()
			goneWrong = False
			for sheet in sheets:
				picking = sheet.cell(0,0).value == 'identified'
				if sheet.nrows == 1:
					continue
				for i in range(0 if first else 1, sheet.nrows):
					if i == 0 or (not picking) or (picking and float(sheet.cell(i,0).value) != 0 and len(sheet.cell(i,1).value) > 0):
						nonnan = False
						for j in range(0, sheet.ncols):
							val = sheet.cell(i,j).value
							if len(str(val)) > 0:
								nonnan = True
								ws.write(row, j, val)
						if nonnan:
							row += 1
							first = False

print('Processing folders:')
process(path)

out = "/Users/tizianasvenningsen/Dropbox/Uni/Bachelor projekt/Matlap + python/SharedAnalysis"
time = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
wb.save(out+"/regression_"+time+".xls")

print('--------------------------')
print('Processing done.')
print('Timestamp: '+time)