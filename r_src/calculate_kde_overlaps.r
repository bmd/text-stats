kde_overlap <- function(a, b) {
	library(sfsmisc)
	
	# ensure that kernels are calculated along a common scale
	lower <- min(c(a, b)) - 1
	upper <- max(c(a, b)) + 1
	
	# generate kernel densities
	da <- density(a, from=lower, to=upper)
	db <- density(b, from=lower, to=upper)
	d <- data.frame(x=da$x, a=da$y, b=db$y)
	
	# calculate intersection densities
	d$w <- pmin(d$a, d$b)
	
	# integrate
	total <- integrate.xy(d$x, d$a) + integrate.xy(d$x, d$b)
	intersection <- integrate.xy(d$x, d$w)
	
	# return % of each curve overlapping
	return(intersection/total)
}

