# @Float(label='Wavelength (nm):', required=true) wavelength
# @Float(label='Angle of incidence (˚):', required=true) theta
# @Dataset data
# @OUTPUT Dataset output
# @DatasetService datasetService
# @DisplayService display
# @OpService ops


from net.imagej.axis import Axes
from net.imglib2.util import Intervals
from net.imglib2.algorithm.labeling.ConnectedComponents import StructuringElement
from net.imglib2.roi.labeling import LabelRegions
import math


# Get first slice
max_x = data.max(data.dimensionIndex(Axes.X))
max_y = data.max(data.dimensionIndex(Axes.Y))
intervals = Intervals.createMinMax(0, 0, 0, max_x, max_y, 0)
first_frame = ops.run('transform.crop', data, intervals, True)

# Subtract lowest pixel value
first_frame = ops.copy().img(first_frame)
i_min = ops.stats().min(first_frame).get()
first_frame = ops.math().subtract(first_frame, i_min)

# Segment slice
blurred = ops.filter().gauss(first_frame, 3)
method_threshold = 'huang'
segmented = ops.run('threshold.%s' % method_threshold, blurred)
segmented = ops.morphology().fillHoles(segmented)

# Get largest region
labeled = ops.run('cca', segmented, StructuringElement.EIGHT_CONNECTED)
max_region = max(LabelRegions(labeled), key=lambda(x): x.size())

# Map intensity to z
z_res = 10.0 # nm/slice
i_max = ops.stats().max(first_frame).get()
z_map = ops.create().img([data.dimension(d) for d in range(first_frame.numDimensions())])
cursor = max_region.localizingCursor()
z_mapRA = z_map.randomAccess()
dataRA = first_frame.randomAccess()

theta = theta * 2 * math.pi / 360 # Angle of incidence in radians
n1 = 1.52 # Refractive index of glass
n2 = 1.38 # Refractive index of cytosol
d_const = wavelength * (n1**2 * math.sin(theta)**2 - n2**2)**(-0.5) / (4 * math.pi)

while cursor.hasNext():
	cursor.fwd()
	z_mapRA.setPosition(cursor)
	dataRA.setPosition(cursor)
	z = int(-d_const * math.log(dataRA.get().get() / i_max) / z_res)
	z_mapRA.get().set(z)

cursor.reset()
max_z = int(ops.stats().max(z_map).get()) + 10
result = ops.create().img([max_x, max_y, max_z])
resultRA = result.randomAccess()

while cursor.hasNext():
	cursor.fwd()
	z_mapRA.setPosition(cursor)
	z_index = int(z_mapRA.get().get())
	position = [cursor.getIntPosition(0), cursor.getIntPosition(1), z_index]
	while position[2] < max_z:
		resultRA.setPosition(position)
		resultRA.get().set(1)
		position[2] += 1

output = datasetService.create(result)





