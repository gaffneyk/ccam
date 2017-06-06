# @String(label="Threshold Method:", required=true, choices={'otsu', 'huang'}) method_threshold
# @Dataset data
# @OUTPUT Dataset output
# @DatasetService datasetService
# @OpService ops

segmented = ops.run('threshold.%s' % method_threshold, data)
output = datasetService.create(segmented)