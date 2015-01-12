library(ggplot2)
library(scales)

# set to directory where you're storing the results
# all other filenames should be consistent
setwd('~/Dropbox/GIT Projects/text-stats/outputs/20150111-193235_outputs_10000_iterations_chisquare/')



# read text vs text comparisons
df <- read.csv('text_vs_others_comparisons.csv', header=TRUE)
# plot text vs text comparisons
ggplot(data=df) + 
	geom_density(aes(x=Chi2.Statistic, color=Comparison.Text, fill=Comparison.Text), alpha=.05) + 
	geom_density(aes(x=Chi2.Statistic), size=1.25) + 
	theme_bw() + 
	xlab("Chi2 Statistic") + 
	ylab("Density")


# read self vs self comparisons
df2 <- read.csv('self_vs_self_comparisons.csv', header=TRUE)
# plot self vs self comparisons
ggplot(data=df2) + 
	geom_density(aes(x=Chi2.Statistic, color=Text, fill=Text), alpha=.05) + 
	geom_density(aes(x=Chi2.Statistic), size=1.25) + 
	theme_bw() + 
	xlab("Chi2 Statistic") + 
	ylab("Density")
	
# plt overlap of curves
ggplot() + 
	geom_density(aes(x=Chi2.Statistic), color='#768CCF', fill='#768CCF', alpha=.1, data=df2, size=1.25) + 
	geom_density(aes(x=Chi2.Statistic), color='#B02033', fill='#B02033', alpha=.1, data=df, size=1.25) + 
	geom_area(aes(y = pmin(self_kernel$y, text_kernel$y)), fill='gray60') + 
	scale_x_continuous(limits=c(0, 1000)) + 
	theme_bw() + 
	scale_y_continuous(labels=percent) + 
	xlab("Chi2 Statistic") + 
	ylab("Density") +
	ggtitle("Fig 1: Comparison of Results between Self and Intertext Comparisons")

# figure out area overlap of curves
self_kernel = density(df2$Chi2.Statistic)
text_kernel = density(df$Chi2.Statistic)





