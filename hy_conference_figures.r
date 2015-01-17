library(ggplot2)
library(scales)

# set to directory where you're storing the results
# all other filenames should be consistent
setwd('~/Dropbox/GIT Projects/text-stats/outputs/20150116-210809_IT10000_SW15_PCT50_chisquare/')

# read in results files
df <- read.csv('self_vs_self_comparisons.csv', header=TRUE)
df2 <- read.csv('text_vs_others_comparisons.csv', header=TRUE)
dfp <- read.csv('praiectus_section_comparisons.csv', header=TRUE)
prae_1_vs_2 <- dfp[dfp$Base.Section == 'praiectus 1' & dfp$Comparison.Section == 'praiectus 2',]
prae_1_vs_3 <- dfp[dfp$Base.Section == 'praiectus 1' & dfp$Comparison.Section == 'praiectus 3',]
prae_2_vs_1 <- dfp[dfp$Base.Section == 'praiectus 2' & dfp$Comparison.Section == 'praiectus 1',]
prae_2_vs_3 <- dfp[dfp$Base.Section == 'praiectus 2' & dfp$Comparison.Section == 'praiectus 3',]
prae_3_vs_1 <- dfp[dfp$Base.Section == 'praiectus 3' & dfp$Comparison.Section == 'praiectus 1',]
prae_3_vs_2 <- dfp[dfp$Base.Section == 'praiectus 3' & dfp$Comparison.Section == 'praiectus 2',]
prae_variables = c(prae_1_vs_2, prae_1_vs_3, prae_2_vs_1, prae_2_vs_3, prae_3_vs_1, prae_3_vs_2)
#####
#
# FIGURE 1: Self comparisons
#
#####
# plot text vs text comparisons
fig_1 <- ggplot(data=df) + 
	geom_density(
		aes(x=Chi2.Statistic), 
		trim=TRUE, 
		alpha=0.25, 
		color='deepskyblue4', 
		fill='deepskyblue4', 
		size=1
	) + 
	theme_bw() + 
	theme(legend.position="none") +
	guides(fill=FALSE) +
	xlab("Chi2 Statistic") + 
	ylab("Density") + 
	scale_x_continuous(limits=c(0, 1000)) +
	scale_y_continuous(labels=percent)
ggsave(filename='fig1_self_vs_self_distribution.png', plot=fig_1, width=10, height=7, units="in")


#####
#
# FIGURE 2: Curve Overlaps
#
#####
fig_2 <- ggplot() + 
	geom_density(
		aes(x=Chi2.Statistic), 
		trim=TRUE,
		color='darkred', 
		fill='darkred', 
		alpha=.25, 
		data=df2, 
		size=1
	) + 
	geom_density(
		aes(x=Chi2.Statistic), 
		color='deepskyblue4', 
		fill='deepskyblue4', 
		trim=TRUE,
		alpha=.25, 
		data=df, 
		size=1
	) +  
	scale_x_continuous(limits=c(0, 1000)) + 
	theme_bw() + 
	scale_y_continuous(labels=percent) + 
	xlab("Chi2 Statistic") + 
	ylab("Density")
ggsave(filename='fig2_both_base_distributions.png', plot=fig_2, width=10, height=7, units="in")


fig_3 <- ggplot() + 
	geom_density(
		aes(x=Chi2.Statistic), 
		trim=TRUE,
		color='forestgreen', 
		fill='forestgreen', 
		alpha=.25, 
		data=dfp, 
		size=1
	) + 
	geom_density(
		aes(x=Chi2.Statistic), 
		color='deepskyblue4', 
		fill='deepskyblue4', 
		trim=TRUE,
		alpha=.25, 
		data=df, 
		size=1
	) +  
	scale_x_continuous(limits=c(0, 1000)) + 
	theme_bw() + 
	scale_y_continuous(labels=percent) + 
	xlab("Chi2 Statistic") + 
	ylab("Density")
ggsave(filename='fig3_self_vs_praiectus_summary.png', plot=fig_3, width=10, height=7, units="in")

pv <- prae_3_vs_2
fig_prae <- ggplot() + 
	geom_density(
		aes(x=Chi2.Statistic), 
		trim=TRUE,
		color='forestgreen', 
		fill='forestgreen', 
		alpha=.25, 
		data=pv, 
		size=1
	) + 
	geom_density(
		aes(x=Chi2.Statistic), 
		color='deepskyblue4', 
		fill='deepskyblue4', 
		trim=TRUE,
		alpha=.25, 
		data=df, 
		size=1
	) +  
	scale_x_continuous(limits=c(0, 1000)) + 
	theme_bw() + 
	scale_y_continuous(labels=percent) + 
	xlab("Chi2 Statistic") + 
	ylab("Density")
	ggsave(filename=paste("fig_", deparse(substitute(prae_3_vs_2)), ".png", sep=""), plot=fig_prae, width=10, height=7, units="in")



