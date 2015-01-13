CalculateKDEOverlap <- function(a, b) {
  # Estimates the overlapping area between the kernel density
  # functions calculated on two vectors.
  #
  # Args:
  #   a: A vector without missing values from which a kernel
  #      density estimate can be produced.
  #   b: A vector without missing values from which a kernel
  #      density estimate can be produced.
  #
  # Returns:
  #   The shared area between the kernel density functions
  #   of a and b. 
  library(sfsmisc)
	
  # ensure that kernels are calculated along a common scale
  upper <- max(c(a, b)) + 1
	
  # generate kernel densities
  da  <- density(a, from = 0, to = upper)
  db  <- density(b, from = 0, to = upper)
  d   <- data.frame(x = da$x, a = da$y, b = db$y)
  d$w <- pmin(d$a, d$b)  # model overlapping region 
	
  # integrate
  area.under.da <- integrate.xy(d$x, d$a)
  area.under.db <- integrate.xy(d$x, d$b)
  intersection  <- integrate.xy(d$x, d$w)

  # return overlapping curve area
  return((2 * intersection) / (area.under.da + area.under.db))
}
