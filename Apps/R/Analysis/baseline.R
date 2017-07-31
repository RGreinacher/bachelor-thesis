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

relevant_data <- data.frame(
  "VP" = factor(),
  "condition" = factor(),
  "baseline_correctness" = numeric(),
  "baseline_tempo" = numeric(),
  "baseline_misses" = numeric(),
  "correctness_only_with_assistence" = numeric()
)

for (i in 1:66) {
  data_row = data_frame[i,]
  
  if (data_row$block_0_assistance_present == "True") {
    baseline_correctness = (data_row$block_1_correctness + data_row$block_3_correctness) / 2.0
    correctness_only_with_assistence = (data_row$block_0_correctness + data_row$block_2_correctness) / 2.0

    baseline_tempo = (data_row$block_1_time_avg_per_annotation + data_row$block_3_time_avg_per_annotation) / 2.0
    
    baseline_misses_block_1 = (data_row$block_1_mistake_missed_count / data_row$block_1_total_annotations_count) * 100.0
    baseline_misses_block_3 = (data_row$block_3_mistake_missed_count / data_row$block_3_total_annotations_count) * 100.0
    baseline_misses = (baseline_misses_block_1 + baseline_misses_block_3) / 2.0
  } else {
    baseline_correctness = (data_row$block_0_correctness + data_row$block_2_correctness) / 2.0
    correctness_only_with_assistence = (data_row$block_1_correctness + data_row$block_3_correctness) / 2.0
    
    baseline_tempo = (data_row$block_0_time_avg_per_annotation + data_row$block_2_time_avg_per_annotation) / 2.0
    
    baseline_misses_block_0 = (data_row$block_0_mistake_missed_count / data_row$block_0_total_annotations_count) * 100.0
    baseline_misses_block_2 = (data_row$block_2_mistake_missed_count / data_row$block_2_total_annotations_count) * 100.0
    baseline_misses = (baseline_misses_block_0 + baseline_misses_block_2) / 2.0
  }
  
  relevant_data <- rbind(
    relevant_data,
    data.frame(
      VP = factor(i),
      condition = factor(data_row$assistance_level),
      baseline_correctness = baseline_correctness,
      baseline_tempo = baseline_tempo,
      baseline_misses = baseline_misses,
      correctness_only_with_assistence = correctness_only_with_assistence
    )
  )
}




# ###############################################################################################################
# Analyse 1 - general statistical descriptions
# ###############################################################################################################

stat.desc(relevant_data$baseline_correctness)
# Median: 86.23%, Mean: 83.93%

stat.desc(relevant_data$baseline_tempo)
# Median: 7.86s, Mean: 8.19s

stat.desc(relevant_data$baseline_misses)
# Median: 5.50%, Mean: 7.69%




# ###############################################################################################################
# Analyse 2 - ANOVA for finding differences between conditions
# ###############################################################################################################

t1way(baseline_correctness ~ condition, data = relevant_data)
# ✗ no significant difference

t1way(baseline_tempo ~ condition, data = relevant_data)
# ✗ no significant difference

t1way(baseline_misses ~ condition, data = relevant_data)
# ✗ no significant difference




