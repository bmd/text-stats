ListRegexMatches <- function(s, regexp) {
  #  Wraps stringr.str_match_all() to return all captured matches
  #  from s when evaluated against regexp.
  #
  #  Args:
  #    s: The string to match against.
  #    regexp: A regular expression with 0 or more capture
  #            groups.
  #  Returns:
  #    A one-dimensional list of matches.
  library(stringr)
	
  matches <- unlist(str_match_all(s, regexp))
	
  return (matches)
}
