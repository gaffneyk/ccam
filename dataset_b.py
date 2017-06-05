
# The module __future__ contains some useful functions:
# https://docs.python.org/2/library/__future__.html
#from __future__ import with_statement, division
# This imports the function random from the module random.
from random import random
# Next we import Java Classes into Jython.
# This is how we can acces the ImageJ API:
# https://imagej.nih.gov/ij/developer/api/allclasses-noframe.html
from ij import IJ, WindowManager, ImagePlus
from ij.gui import GenericDialog
from ij.process import ImageProcessor
from ij.plugin import ImageCalculator
from io.scif.img import IO, SCIFIOImgPlus, ImgOpener
#from io.scif.formats import TIFFFormat
from net.imglib2.img import Img
from net.imglib2.img.array import ArrayImgFactory
from net.imglib2.type.numeric.real import FloatType
from net.imglib2.img.display.imagej import ImageJFunctions
from net.imglib2.view import Views
from array import array
from net.imglib2.algorithm.binary import Thresholder
#from net.imglib2.script.math import Divide
#import inspect


def run_script_old():
	img1 = IJ.openImage('C:/temp/dataset1.tif')
	img2 = IJ.openImage('C:/temp/dataset2.tif')
	img1.show()
	img2.show()
	img1.setPosition(1,1,3)
	img2.setPosition(1,1,3)
	img2Processor = img2.getProcessor()
	img2Processor.setThreshold(6e-7,1.0,ImageProcessor.RED_LUT)
	IJ.run('Create Selection')
#	IJ.run('Image Calculator...',"Divide create 32-bit stack", "dataset1.tif","dataset2.tif")// Bug doesn't change operation
	ic = ImageCalculator()#Using plugin instead of menu
	imp3 = ic.run("Divide create", img1, img2)
	imp3.show()
	imp3.restoreRoi()
	IJ.run("Measure")

def run_script_new():
#	print(inspect.getmembers(scijava))
#	return
	testFiles = ("C:/temp/dataset1.tif","C:/temp/dataset2.tif")

	images = []
	views = []
	thresholds = []
	for testFile in testFiles:
		img = ImgOpener().openImg(testFile,FloatType());
		images.append(img)
		print(repr(img.numDimensions()))
		thedims = array('l',img.numDimensions()*[0])# pre-allocate 'long' array
		img.dimensions(thedims)
		print(repr(thedims))
		view = Views.interval( img, ( 0,0,2 ),( thedims[0]-1,thedims[1]-1,2 ) );
		views.append(view)
		threshold = Thresholder.threshold(img,FloatType(6e-7),True,1)
		threshView = Views.interval( threshold, ( 0,0,2 ),( thedims[0]-1,thedims[1]-1,2 ) );
		thresholds.append(threshView)
	
	dispImgs = []
	for view in views:
		dispImgs.append(ImageJFunctions.show(view))

	dispThresh = []
	for threshold in thresholds:
		dispThresh.append(ImageJFunctions.show(threshold))

	numerand = images[0]
	divisor = images[1]
	result = numerand.factory().create( numerand, numerand.firstElement() );#create img of same type
	cursorNumerand = numerand.cursor();
	cursorDivisor = divisor.cursor();
	cursorResult = result.cursor()

	while cursorNumerand.hasNext():
		cursorNumerand.fwd()
		cursorDivisor.fwd()
		cursorResult.fwd()
		cursorResult.get().set(cursorNumerand.get())
		cursorResult.get().div(cursorDivisor.get())
		#print("%s %s %s %s" % (cursorResult.get(),cursorNumerand.get(),cursorDivisor.get()))

	dispThresh[1].getProcessor().setThreshold(1,255,ImageProcessor.RED_LUT)
	dispThresh[1].getWindow().toFront()
	IJ.run('Create Selection')
	result = ImageJFunctions.show(result,"results")
	result.setC(3)
	result.restoreRoi()
	IJ.run("Measure")
	
#	result = Divide(views[0],views[1]).asImage()
#	print(repr(result))
	return
#	print(repr(img))
#	imgL = IO.openImgs("C:/temp/dataset1.tif")
	
#	blank = IJ.createImage("Blank", "32-bit black", img_size, img_size, 1)
#	List<SCIFIOImgPlus<net.imglib2.type.numeric.real.FloatType>> imgL = IO.openFloatImgs('C:/temp/dataset1.tif')
#	List<SCIFIOImgPlus<net.imglib2.type.numeric.real.FloatType>> imgL = IO.openImgs("C:/temp/dataset1.tif")

#	ImgPlus< FloatType > img = ImgOpener().openImg( 'C:/temp/dataset1.tif', ArrayImgFactory< FloatType >(), FloatType() );
#	TIFFFormat.Reader tfr = TIFFFormat.Reader()
#	tfr.setSource(File('C:/temp/dataset1.tif'))
#	List<SCIFIOImgPlus<T extends net.imglib2.type.numeric.RealType<T>>> imgL = ImgOpener.openImgs(tfr)

	ImageJFunctions.show(img1)
	ImageJFunctions.show(img2)
	img1.setPosition(1,1,3)
	img2.setPosition(1,1,3)
	img2Processor = img2.getProcessor()
	img2Processor.setThreshold(6e-7,1.0,ImageProcessor.RED_LUT)
	IJ.run('Create Selection')
#	IJ.run('Image Calculator...',"Divide create 32-bit stack", "dataset1.tif","dataset2.tif")// Bug doesn't change operation
	ic = ImageCalculator()#Using plugin instead of menu
	imp3 = ic.run("Divide create", img1, img2)
	imp3.show()
	imp3.restoreRoi()
	IJ.run("Measure")

	
if __name__ == '__main__':
	run_script_new()
