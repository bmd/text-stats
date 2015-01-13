library(sfsmisc)
library(stringr)

# set environments
BASE_DIR = '~/git/text-stats/outputs'
setwd(BASE_DIR)

# function to calculate KDE overlaps
source('../r_src/calculate_kde_overlaps.r')

# pattern match to extract iterations and stopword data, etc
determine_simulation_parameters_from_file_name <- function (name) {
	library(stringr)
	
	# define regex
	expr <- '[0-9]{8}-[0-9]{6}_IT([0-9]+)_SW([0-9]+)_PCT([0-9]+)_(.*)'
	# extract matches 
	matches <- str_match_all(name, expr)
	
	return (unlist(matches))
}

# get all the directories contained in outputs
results_directories <- dir(path='.')

# create a variable to store summaries
output <- NULL
output <- rbind(output, c('Folder Name', 'Iterations', 'Stopwords', 'Sample Size', 'Method', 'Curve overlap pct'))

# iterate over all sets of results in the results directory
for (d in results_directories) {
	# load data
	t <- read.csv(file.path(d, 'text_vs_others_comparisons.csv'))
	s <- read.csv(file.path(d, 'self_vs_self_comparisons.csv'))
	
	# calculate per-curve overlap %:
	# because the area under both curves is 1, this overlap = % overlap.
	# 2* this result gets the total overlap area (area under both curves)  
	overlap_pct = CalculateKDEOverlap(t$Chi2.Statistic, s$Chi2.Statistic)
	
	# parse simulation parameters for categorical values
	parameters <- determine_simulation_parameters_from_file_name(d)	
	parameters[[length(parameters)+1]] <- overlap_pct

	# return result
	output <- rbind(output, parameters)
	
}

# write result to CSV file
write.csv(output, file='curve_overlap_results.csv', row.names=FALSE)
