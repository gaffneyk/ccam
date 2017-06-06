# @Dataset data
# @OUTPUT Dataset output
# @OpService ops
# @DatasetService datasetService
# @DisplayService displayService

# Subtract the first frame of a stack to all the frames of the given stack along the TIME axis.
# It removes the static elements from a stack. Usefull when you are studying moving objects.
 
from net.imglib2.util import Intervals
from net.imagej.axis import Axes
 
# Convert input
converted = ops.convert().float32(data)
 
# Get the frame to subtract out
z_idx = 1 # Change this to choose frame
intervals = Intervals.createMinMax(0, 0, z_idx, data.getWidth() - 1, data.getHeight() - 1, z_idx)
frame = ops.transform().crop(converted, intervals)
t_dim = data.dimensionIndex(Axes.Z) # Should actually be TIME but our images use Z
 
# Allocate output memory (wait for hybrid CF version of slice)
subtracted = ops.create().img(converted)
 
# Create the op
sub_op =  ops.op("math.subtract", frame, frame)
 
# Setup the fixed axis
fixed_axis = [d for d in range(0, data.numDimensions()) if d != t_dim]
 
# Run the op
ops.slice(subtracted, converted, sub_op, fixed_axis)
 
# Clip image to the input type
clipped = ops.create().img(subtracted, data.getImgPlus().firstElement())
clip_op = ops.op("convert.clip", data.getImgPlus().firstElement(), subtracted.firstElement())
ops.convert().imageType(clipped, subtracted, clip_op)

# Create output Dataset
output = datasetService.create(clipped)
