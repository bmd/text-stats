library(sfsmisc)

# set environments
BASE_DIR = 'path/to/outputs/'
setwd(BASE_DIR)

# include fxn to calculate overlap of KDE curves
source('r_src/calculate_kde_overlaps.r')

# pattern match to extract iterations and stopword data, etc
determine_simulation_parameters_from_file_name <- function (name) {
	regex = '.*'
	r <- list(d.match(regex))
	return (r)
}

# get all the directories contained in outputs
results_directories <- dir(path='.')

# create a variable to store summaries
output <- data.frame(
	row.names=c('Folder Name', 'Iterations', 'Stopwords', 'Sample Size', 'Curve overlap %'),
	header=TRUE
)

# iterate over all sets of results in the results directory
for (d in results_directories) {
	# load data
	t <- read.csv('text_vs_others_comparisons.csv')
	s <- read.csv('self_vs_self_comparisons.csv')
	
	# calculate per-curve overlap %:
	# because the area under both curves is 1, this overlap = % overlap.
	# 2* this result gets the total overlap area (area under both curves)  
	overlap_pct = kde_overlap(t$Chi2.Statistic, s$Chi2.Statistic)
	
	# parse simulation parameters for categorical values
	names <- determine_simulation_parameters_from_file_name(d)
	final <- cbind(names, overlap_pct)
	
	# append row to final output 
	output <- rbind(output, final)
}

write.csv(output)
