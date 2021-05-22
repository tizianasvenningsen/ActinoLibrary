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

wb2 = xlwt.Workbook()
ws2 = wb2.add_sheet('Sheet 1') 
first = True
row = 1

def process(path):
	global first
	global row
	print("\t"+path)
	for f in os.scandir(path):
		if f.is_dir():
			process(f.path)
	for filename in os.listdir(path):
		if filename.endswith(".xls") and "means" not in filename and "stddev" not in filename:
			book = xlrd.open_workbook(path+"/"+filename)
			sheets = book.sheets()
			goneWrong = False
			for sheet in sheets:
				if sheet.nrows == 1:
					continue
				for j in range(0, sheet.ncols):
					# label
					if j == 0:
						val = sheet.cell(1, 0).value
						try:
							trunc = val[0: val.rfind('-')]
							if first:
								ws.write(0, 0, 'label')
								ws2.write(0, 0, 'label')
							ws.write(row, 0, trunc)
							ws2.write(row, 0, trunc)
						except:
							print("probably still in picking format: ",filename,i,j)
					# sample
					elif j == 1:
						val = sheet.cell(1, 1).value
						#val = val[0:val.find(' ')]
						ws.write(row, 1, val)
						ws2.write(row, 1, val)
						if first:
							ws.write(0, 1, 'sample')
							ws2.write(0, 1, 'sample')
					# ID
					elif j == 2:
						val = sheet.cell(1, 2).value
						trunc = val[0: val.rfind('-')]
						ws.write(row, 2, trunc)
						ws2.write(row, 2, trunc)
						if first:
							ws.write(0, 2, 'ID')
							ws2.write(0, 2, 'ID')
					# everything else
					else:
						summ = 0
						num = 0
						for i in range(0 if first else 1, sheet.nrows):
							val = sheet.cell(i,j).value
							if i == 0:
								ws.write(0, j, val)
								ws2.write(0, j, val)
							elif not isinstance(val, str):
								summ += val
								num += 1
						if num > 0:
							mean = summ / num
							ws.write(row, j, mean)
							s = 0
							for i in range(1, sheet.nrows):
								val = sheet.cell(i,j).value
								if not isinstance(val, str):
									s += (mean - sheet.cell(i,j).value) ** 2
							s = sqrt(s / num)
							ws2.write(row, j, s)
						else:
							goneWrong = True
				first = False
			if sheet.nrows > 1:
				if goneWrong:
					del ws.rows[row]
					del ws2.rows[row]
				else:
					row += 1

print('Processing folders:')
process(path)

out = "/Users/tizianasvenningsen/Dropbox/Uni/Bachelor projekt/Matlap + python/SharedAnalysis"
time = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
wb.save(out+"/means_"+time+".xls")
wb2.save(out+"/stddev_"+time+".xls")

print('--------------------------')
print('Processing done.')
print('Timestamp: '+time)