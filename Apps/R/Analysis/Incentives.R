library(readr)
library(pastecs)
library(compute.es)
library(car)
library(WRS2)
library(ez)
library(reshape)
library(nlme)

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

subject_id = factor(data_frame$subject_id)
condition <- factor(data_frame$assistance_level)
incentive <- factor(data_frame$reward)

correctness <- (data_frame$assistance_no_assistance_correctness_difference_block_0_1 + data_frame$assistance_no_assistance_correctness_difference_block_2_3) / 2
tempo <- (data_frame$assistance_no_assistance_time_difference_block_0_1 + data_frame$assistance_no_assistance_time_difference_block_2_3) / 2
misses <- ((data_frame$assistance_no_assistance_misses_ratio_difference_block_0_1 + data_frame$assistance_no_assistance_misses_ratio_difference_block_2_3) / 2) * 100.0

relevant_data <- data.frame(
  subject_id,
  condition,
  incentive,
  correctness,
  tempo,
  misses
)




# ############################################################################################################
# ANOVA
# ############################################################################################################

# Standard One-way ANOVA
summary(aov(correctness ~ incentive, data = relevant_data))
summary(aov(tempo ~ incentive, data = relevant_data))
summary(aov(misses ~ incentive, data = relevant_data))
# ✗ Es gab keinen signifikanten Unterschiede









