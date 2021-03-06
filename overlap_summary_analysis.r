# set environments
BASE_DIR = '~/git/text-stats/outputs'
setwd(BASE_DIR)

# import functions
source('../r_src/calculate_kde_overlaps.r')
source('../r_src/utils.r')

# get all the directories contained in outputs
results_directories <- dir(path = '.')

# create a variable to store summaries
output <- NULL
output <- rbind(output, c('Folder Name', 'Iterations', 'Stopwords', 'Sample Size', 'Method', 'Curve overlap pct'))

# iterate over all sets of results in the results directory
for (d in results_directories) {
  # load data
  p <- read.csv(file.path(d, 'praiectus_section_comparisons.csv'))
	
  # calculate the % overlapping area between the two curves
  overlap_pct <- CalculateKDEOverlap(t$Chi2.Statistic, s$Chi2.Statistic)

  # parse simulation parameters for categorical values
  parameters <- ListRegexMatches(d, '[0-9]{8}-[0-9]{6}_IT([0-9]+)_SW([0-9]+)_PCT([0-9]+)_(.*)')	
  parameters[[length(parameters)+1]] <- overlap_pct

  # return result
  output <- rbind(output, parameters)	
}

# write result to CSV file
write.csv(output, file = 'curve_overlap_results.csv', row.names = FALSE)
