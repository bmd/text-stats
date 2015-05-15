library(ggplot2)
library(scales)

# set to directory where you're storing the results
# all other filenames should be consistent
setwd('~/git/text-stats/outputs/20150511-195719_IT10000_SW20_PCT50_chisquare/')

# read in results files
df <- read.csv('self_vs_self_comparisons.csv', header=TRUE)
df2 <- read.csv('text_vs_others_comparisons.csv', header=TRUE)
dfp <- read.csv('praiectus_section_comparisons.csv', header=TRUE)
prae_1_vs_1 <- dfp[dfp$Base.Section == 'praiectus 1' & dfp$Comparison.Section == 'praiectus 1',]
prae_1_vs_2 <- dfp[dfp$Base.Section == 'praiectus 1' & dfp$Comparison.Section == 'praiectus 2',]
prae_1_vs_3 <- dfp[dfp$Base.Section == 'praiectus 1' & dfp$Comparison.Section == 'praiectus 3',]

prae_2_vs_1 <- dfp[dfp$Base.Section == 'praiectus 2' & dfp$Comparison.Section == 'praiectus 1',]
prae_2_vs_2 <- dfp[dfp$Base.Section == 'praiectus 2' & dfp$Comparison.Section == 'praiectus 2',]
prae_2_vs_3 <- dfp[dfp$Base.Section == 'praiectus 2' & dfp$Comparison.Section == 'praiectus 3',]

prae_3_vs_1 <- dfp[dfp$Base.Section == 'praiectus 3' & dfp$Comparison.Section == 'praiectus 1',]
prae_3_vs_2 <- dfp[dfp$Base.Section == 'praiectus 3' & dfp$Comparison.Section == 'praiectus 2',]
prae_3_vs_3 <- dfp[dfp$Base.Section == 'praiectus 3' & dfp$Comparison.Section == 'praiectus 3',]

prae_variables = c(prae_1_vs_1, prae_1_vs_2, prae_1_vs_3, prae_2_vs_1, prae_2_vs_2, prae_2_vs_3, prae_3_vs_1, prae_3_vs_2, prae_3_vs_3)

# make some fucking plots
overlap_plot_fig <- ggplot() + 
	geom_density(
		aes(x=Chi2.Statistic), 
		trim=TRUE,
		color='darkred', 
		fill='darkred', 
		alpha=.25, 
		data=prae_3_vs_3, 
		size=1
	) + 
	geom_density(
		aes(x=Chi2.Statistic), 
		color='deepskyblue4', 
		fill='deepskyblue4', 
		trim=TRUE,
		alpha=.25, 
		data=prae_2_vs_3, 
		size=1
	) +  
	geom_density(
		aes(x=Chi2.Statistic), 
		color='deepskyblue2', 
		fill='deepskyblue2', 
		trim=TRUE,
		alpha=.25, 
		data=prae_3_vs_2, 
		size=1
	) + 
	scale_x_continuous(limits=c(0, 500)) + 
	theme_bw() + 
	scale_y_continuous(labels=percent) + 
	xlab("Chi2 Statistic") + 
	ylab("Density")
ggsave(filename='fig_prae_3_self_comparisons_vs2.png', plot= overlap_plot_fig, width=10, height=7, units="in")
