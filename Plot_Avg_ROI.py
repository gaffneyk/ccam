# @Dataset data
# @OUTPUT Dataset output
# @DatasetService datasetService
# @DisplayService displayService
# @OpService ops

from net.imagej.axis import Axes
from ij.plugin.frame import RoiManager
from ij.gui import Plot
from net.imglib2.util import Intervals


# Must add ROI to ROI Manager tool (Analyze > Tools > ROI Manager)
# ONLY WORKS WITH RECTANGLES
roi = RoiManager.getInstance().getRoisAsArray()[0]
points = roi.getContainedPoints()

# For plotting mean intensity
mean_intensities = [] # y-axis
slice_indices = [] # x-axis

# For displaying cropped stack
images = []

for z in range(data.max(data.dimensionIndex(Axes.Z))):

	# Crop the image using the ROI
	intervals = Intervals.createMinMax(points[0].x, points[0].y, z, points[-1].x, points[-1].y, z)
	single_frame_cropped = ops.run('transform.crop', data, intervals, True)

	# Add the data to lists
	images.append(single_frame_cropped)
	mean_intensities.append((ops.run('stats.mean', single_frame_cropped)).getRealFloat())
	slice_indices.append(z)

# Display cropped images
images = ops.run('transform.stackView', [images])
output = datasetService.create(images)

# Display plot
plot = Plot('Mean Intensity vs. Slice', 'Slice', 'Mean Intensity', slice_indices, mean_intensities) 
plot.show() 