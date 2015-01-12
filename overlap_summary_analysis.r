library(sfsmisc)

source('r_src/calculate_kde_overlaps.r')

# set environments
BASE_DIR = 'path/to/outputs/'
setwd(BASE_DIR)

# get all the directories contained in outputs
script_results <- dir(path='.')
for (d in script_results) {
	print(d)
}







df <- read.csv('text_vs_others_comparisons.csv', header=TRUE)
df2 <- read.csv('self_vs_self_comparisons.csv', header=TRUE)

kde_overlap(df$Chi2.Statistic, df2$Chi2.Statistic)