# import functions
setwd('~/git/text-stats/outputs/')
source('../r_src/calculate_kde_overlaps.r')
source('../r_src/utils.r')

# create a variable to store summaries
output <- NULL
output <- as.data.frame(c('Comparisons', 'Curve overlap pct'))

dfp <- read.csv('20150511-195719_IT10000_SW20_PCT50_chisquare/praiectus_section_comparisons.csv')

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

 	# calculate the % overlapping area between the two curves
  	overlap_pct <- CalculateKDEOverlap(prae_1_vs_1$Chi2.Statistic, prae_1_vs_2$Chi2.Statistic)
	print(c('1 vs 1 & 1 vs 2', overlap_pct))
  	overlap_pct <- CalculateKDEOverlap(prae_1_vs_1$Chi2.Statistic, prae_1_vs_3$Chi2.Statistic)
	print(c('1 vs 1 & 1 vs 3', overlap_pct))
  	overlap_pct <- CalculateKDEOverlap(prae_1_vs_2$Chi2.Statistic, prae_1_vs_3$Chi2.Statistic)
	print(c('1 vs 2 & 1 vs 3', overlap_pct))

  	overlap_pct <- CalculateKDEOverlap(prae_2_vs_2$Chi2.Statistic, prae_2_vs_1$Chi2.Statistic)
	print(c('2 vs 2 & 2 vs 1', overlap_pct))
  	overlap_pct <- CalculateKDEOverlap(prae_2_vs_2$Chi2.Statistic, prae_2_vs_3$Chi2.Statistic)
	print(c('2 vs 2 & 2 vs 3', overlap_pct))
  	overlap_pct <- CalculateKDEOverlap(prae_2_vs_1$Chi2.Statistic, prae_2_vs_3$Chi2.Statistic)
	print(c('2 vs 3 & 2 vs 1', overlap_pct))
	
  	overlap_pct <- CalculateKDEOverlap(prae_3_vs_3$Chi2.Statistic, prae_3_vs_1$Chi2.Statistic)
	print(c('3 vs 3 & 3 vs 1', overlap_pct))
  	overlap_pct <- CalculateKDEOverlap(prae_3_vs_3$Chi2.Statistic, prae_3_vs_2$Chi2.Statistic)
	print(c('3 vs 3 & 3 vs 2', overlap_pct))
  	overlap_pct <- CalculateKDEOverlap(prae_3_vs_1$Chi2.Statistic, prae_3_vs_2$Chi2.Statistic)
	print(c('3 vs 1 & 3 vs 2', overlap_pct))		
	
	
	
  	overlap_pct <- CalculateKDEOverlap(prae_2_vs_2$Chi2.Statistic, prae_2_vs_1$Chi2.Statistic)
	output <-rbind(overlap_pct)
  	overlap_pct <- CalculateKDEOverlap(prae_2_vs_2$Chi2.Statistic, prae_2_vs_3$Chi2.Statistic)
	output <-rbind(overlap_pct)
  	overlap_pct <- CalculateKDEOverlap(prae_2_vs_1$Chi2.Statistic, prae_2_vs_3$Chi2.Statistic)
	output <-rbind(overlap_pct)

  	overlap_pct <- CalculateKDEOverlap(prae_3_vs_3$Chi2.Statistic, prae_3_vs_1$Chi2.Statistic)
	output <-rbind(overlap_pct)
  	overlap_pct <- CalculateKDEOverlap(prae_3_vs_3$Chi2.Statistic, prae_3_vs_2$Chi2.Statistic)
	output <-rbind(overlap_pct)
  	overlap_pct <- CalculateKDEOverlap(prae_3_vs_1$Chi2.Statistic, prae_3_vs_2$Chi2.Statistic)
	output <-rbind(overlap_pct)
	

# write result to CSV file
write.csv(output, file = 'curve_overlap_results.csv', row.names = FALSE)
