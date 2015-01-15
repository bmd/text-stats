
#x <- read.csv()
#y <- read.csv()


set.seed(20791)
# generate test vectors
p <- read.csv('~/git/text-stats/outputs/current_outputs/praiectus_section_comparisons.csv')
t <- read.csv('~/git/text-stats/outputs/current_outputs/text_vs_others_comparisons.csv')
s <- read.csv('~/git/text-stats/outputs/current_outputs/self_vs_self_comparisons.csv')

p1.vs.p3 <- p[p$Base.Section == 'praiectus 3' & p$Comparison.Section == 'praiectus 1',]
p1.vs.p2 <- p[p$Base.Section == 'praiectus 2' & p$Comparison.Section == 'praiectus 1',]
p2 <- p[p$Base.Section == 'praiectus 3' & p$Comparison.Section == 'praiectus 2',]

ks.test(p1.vs.p3$Chi2.Statistic, t$Chi2.Statistic, alternative = 'two.sided')

# test difference between distributions
ks.test(p$Chi2.Statistic, t$Chi2.Statistic, alternative = "two.sided", exact = NULL)
ks.test(p$Chi2.Statistic, s$Chi2.Statistic, alternative = "two.sided", exact = NULL)
ks.test(s$Chi2.Statistic, t$Chi2.Statistic, alternative = "two.sided", exact = NULL)

