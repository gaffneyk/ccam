

import os
import re
#from ij.io import FileInfo, FileOpener

from ij import IJ 
from ij import WindowManager as WM 
from ij.measure import ResultsTable as RT 
from ij.gui import Plot 

def calcAvgROI():
	image = WM.getCurrentImage() 
	IJ.setAutoThreshold(image, "Default dark");
	IJ.run(image, "Create Selection", "");
	stack = image.getStack() 
	x = [] 
	y = [] 

	IJ.run("Set Measurements...", "mean display redirect=None decimal=5"); 
	IJ.run("Clear Results", "") 
	for i in range(1, stack.getSize() + 1): 
  	      image.setSlice(i) 
  	      IJ.run(image, "Measure", "") 

	table = RT.getResultsTable() 
	counter = table.getCounter() 
	for i in range(0,counter): 
		row =  table.getRowAsString(i) 
		cells = row.split() 
		x.append(i) 
        # the table consists of 3 columns 
        # cells[0]: index 
        # cells[1]: slice name 
        # cells[2]: mean value 
		y.append(float(cells[2])) 

	plot = Plot(image.getTitle(), "slice", "mean", x, y) 
	plot.show() 

def calcAvgNoTable():
	image = WM.getCurrentImage() 
	stack = image.getStack() 
	x = [] 
	y = [] 
	for i in range(1, stack.getSize() + 1): 
		ip = stack.getProcessor(i) 
		stat = ip.getStatistics() 
		x.append(i) 
		y.append(stat.mean) 

	plot = Plot(image.getTitle(), "slice", "mean", x, y) 
	plot.show() 


def doAll():
	input = "/Volumes/ccam/Abhi/ImageJ_sample/2017-05-05/Zdk";
#	output = "/home/fiji/images/";

	images_sequence_dir = str(input)
	fnames = os.listdir(images_sequence_dir)
	fnames.sort(key=natural_keys)
	cnt = 0
	for fname in fnames:
		if fname.endswith(".tif"):
			cnt+= 1
			if cnt > 5:
				break
			IJ.open(input + '/' + fname)
#			FileOpener.open(fname)
			img = WM.getCurrentImage()
			print(repr(img))
 			calcAvgNoTable()
			img.close()

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]




doAll()











