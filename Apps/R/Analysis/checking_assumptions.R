library(readr)
library(car)

# constants
data_frame <- read_delim("~/Nextcloud/Uni/Bachelorarbeit/Apps/Auswertung/data/data_frame.csv", ";", escape_double = FALSE, trim_ws = TRUE)




# ##############################################################################
# Prep: Generiere Liste
# - Assistenz-Stufe
# - Richtigkeitsunterschied pro VP
# - Geschwindigkeitsunterschied pro VP
# - Auslassunsunterschied (wie viele Annotationsstellen wurden übersehen) pro VP
# jeweils nach Schema: (mit Assistenz - ohne Assistenz)
# ##############################################################################

condition <- factor(data_frame$assistance_level)
correctness <- (data_frame$assistance_no_assistance_correctness_difference_block_0_1 + data_frame$assistance_no_assistance_correctness_difference_block_2_3) / 2
tempo <- (data_frame$assistance_no_assistance_time_difference_block_0_1 + data_frame$assistance_no_assistance_time_difference_block_2_3) / 2
misses <- ((data_frame$assistance_no_assistance_misses_ratio_difference_block_0_1 + data_frame$assistance_no_assistance_misses_ratio_difference_block_2_3) / 2) * 100.0
relevant_data <- data.frame(condition, correctness, tempo, misses)




# #################################
# Assumption 1: normal distribution
# test using the Shapiro-Wilk test
# #################################

shapiro.test(relevant_data$correctness) # p = 0.0005368; ✗ significantly not normal!
shapiro.test(relevant_data$tempo) # p = 0.5346; ✓ not significant => normal distributed
shapiro.test(relevant_data$misses) # p = 0.505; ✓ not significant => normal distributed

# going into detail; for comparing groups the distribution in each group is important (Field, A., 5.6.1):
by(relevant_data$correctness, relevant_data$condition, shapiro.test)
# 10%: p = 0.1969 => ✓ not sign.
# 50%: p = 0.02034 => ✗ sign.!
# 90%: p = 0.01493 => ✗ sign.!

by(relevant_data$tempo, relevant_data$condition, shapiro.test)
# 10%: p = 0.6029 => ✓ not sign.
# 50%: p = 0.416 => ✓ not sign.
# 90%: p = 0.05928 => ✓ not sign.

by(relevant_data$misses, relevant_data$condition, shapiro.test)
# 10%: p = 0.4955 => ✗ sign.!
# 50%: p = 0.6343 => ✓ not sign.
# 90%: p = 0.1111 => ✓ not sign.

# Options:
# - transforming the data
# - using Wilcox ANOVA variant




# #####################################
# Assumption 2: Homogenity of variances
# test using Levene's test
# #####################################

leveneTest(relevant_data$correctness, relevant_data$condition)
# Pr 0.703 > 0.05; ✓ variances not significantly different

leveneTest(relevant_data$tempo, relevant_data$condition)
# Pr 0.009416 < 0.05; ✗ variances are significantly different!

leveneTest(relevant_data$misses, relevant_data$condition)
# Pr 0.538 > 0.05; ✓ variances not significantly different

# homogenity of variance assumtion is tenable for correctness & misses, but is violated for tempo!
# double checking the tempo data using Hartley's F_max / the variance ratio
# df = 21, variances = 3
var_max = var(relevant_data$tempo[relevant_data$condition == 10]) # 4.077678
var_min = var(relevant_data$tempo[relevant_data$condition == 90]) # 1.054643 (condition 50 = 3.441604)
ratio = var_max / var_min # 3.866407
# => significant according to Hartley's critical value table (df = 20, variances = 3, ratio should be < 2.95 to be not significant)

# Options:
# - transforming the tempo data
# - going on, doing the Welch or Brown-Forsythe F-tests (https://www.researchgate.net/post/Correct_tests_to_run_when_Homogeneity_of_variance_is_violated_in_ANOVA)
# - Kruskal-Wallis H Test
