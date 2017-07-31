library(readr)
library(pastecs)
library(compute.es)
library(car)
library(WRS2)
library(ez)
library(reshape)
library(Hmisc)

# constants
data_frame <- read_delim("~/Nextcloud/Uni/Bachelorarbeit/Apps/Auswertung/data/data_frame.csv", ";", escape_double = FALSE, trim_ws = TRUE)




# ##############################################################################
# Prep: Generiere Liste
# - Assistenz-Stufe
# - Stress Block 1 & 2, Block 3 & 4, Durchschnitt
# - Monotonie Block 1 & 2, Block 3 & 4, Durchschnitt
# jeweils nach Schema: (mit Assistenz - ohne Assistenz)
# ##############################################################################

relevant_data <- data.frame(
  "VP" = factor(),
  "condition" = factor(),
  "startWithAssistance" = factor(),
  "baseline_stress" = numeric(),
  "stress_overall" = numeric(),
  "stress_01" = numeric(),
  "stress_23" = numeric(),
  "baseline_monotony" = numeric(),
  "monotony_overall" = numeric(),
  "monotony_01" = numeric(),
  "monotony_23" = numeric()
)

for (i in 1:66) {
  data_row = data_frame[i,]
  
  if (data_row$block_0_assistance_present == "True") {
    baseline_stress = (data_row$block_1_questionnaire_stress + data_row$block_3_questionnaire_stress) / 2.0
    stress_01 = data_row$block_0_questionnaire_stress - data_row$block_1_questionnaire_stress
    stress_23 = data_row$block_2_questionnaire_stress - data_row$block_3_questionnaire_stress
    
    baseline_monotony = (data_row$block_1_questionnaire_monotonous + data_row$block_3_questionnaire_monotonous) / 2.0
    monotony_01 = data_row$block_0_questionnaire_monotonous - data_row$block_1_questionnaire_monotonous
    monotony_23 = data_row$block_2_questionnaire_monotonous - data_row$block_3_questionnaire_monotonous
  } else {
    baseline_stress = (data_row$block_0_questionnaire_stress + data_row$block_2_questionnaire_stress) / 2.0
    stress_01 = data_row$block_1_questionnaire_stress - data_row$block_0_questionnaire_stress
    stress_23 = data_row$block_3_questionnaire_stress - data_row$block_2_questionnaire_stress
    
    baseline_monotony = (data_row$block_0_questionnaire_monotonous + data_row$block_2_questionnaire_monotonous) / 2.0
    monotony_01 = data_row$block_1_questionnaire_monotonous - data_row$block_0_questionnaire_monotonous
    monotony_23 = data_row$block_3_questionnaire_monotonous - data_row$block_2_questionnaire_monotonous
  }
  
  relevant_data <- rbind(
    relevant_data,
    data.frame(
      VP = factor(i),
      condition = factor(data_row$assistance_level),
      startWithAssistance = factor(data_row$block_0_assistance_present),
      baseline_stress = baseline_stress,
      stress_overall = (stress_01 + stress_23) / 2,
      stress_01 = stress_01,
      stress_23 = stress_23,
      baseline_monotony = baseline_monotony,
      monotony_overall = (monotony_01 + monotony_23) / 2,
      monotony_01 = monotony_01,
      monotony_23 = monotony_23
    )
  )
}

stat.desc(relevant_data$baseline_stress)
# Median: 4.25, Mean: 4.19

stat.desc(relevant_data$baseline_monotony)
# Median: 3.0, Mean: 3.67




# #####################################################################################################
# Analyse 3a - One Sample T-Test
# Test ob die generelle Differenz (mit Assistenzsystem - ohne Assistenzsystem) signifikant größer 0 ist
# Ergebnis: Die Assistenzsysteme machen in allen drei Dimensionen einen signifikanten Unterschied
# #####################################################################################################

# test ob die Stressdifferenz (mit AS - ohne AS) je Assistenzsysteme signifikant größer ist als 0
t.test(relevant_data$stress_overall[relevant_data$condition == 10])
# t = 0.94144, df = 21, p-value = 0.3572, mean of x = 0.1590909
t.test(relevant_data$stress_overall[relevant_data$condition == 50])
# t = -1.2862, df = 21, p-value = 0.2124, mean of x = -0.3181818
t.test(relevant_data$stress_overall[relevant_data$condition == 90])
# t = -2.8706, df = 21, p-value = 0.009153, mean of x = -0.7045455 



# test ob die Monotoniedifferenz (mit AS - ohne AS) je Assistenzsysteme signifikant größer ist als 0
t.test(relevant_data$monotony_overall[relevant_data$condition == 10])
# t = 0.31774, df = 21, p-value = 0.7538, mean of x = 0.04545455
t.test(relevant_data$monotony_overall[relevant_data$condition == 50])
# t = -1.4052, df = 21, p-value = 0.1746, mean of x = -0.3409091
t.test(relevant_data$monotony_overall[relevant_data$condition == 90])
# t = 0.81182, df = 21, p-value = 0.426, mean of x = 0.2045455 




# ###############################################################################################################
# Analyse 1b - Correlation / Effektstärken
# Test der Effektstärken der Assistenz auf die drei Leistungsdimensionen
# Ergebnis: Die Assistenzsysteme machen in allen drei Dimensionen einen signifikanten Unterschied
# ###############################################################################################################

rcorr(
  as.matrix(
    data.frame(
      data_frame$assistance_level,
      relevant_data$stress_overall
    )
  )
)
# r = -0.33, p = 0.0077 **

rcorr(
  as.matrix(
    data.frame(
      data_frame$assistance_level,
      relevant_data$monotony_overall
    )
  )
)
# r = 0.06, p = 0.6135




# ############################################################################################################
# Analyse 3b - ANOVA
# Vergleich der Differenzen (mit Assistenzsystem - ohne Assistenzsystem) zwischen allen drei Gruppen (between)
# also Diff.(90) vs. Diff (50) vs. Diff (10)
# ############################################################################################################

# Annahmen prüfen: Normalverteilung & Varianz-Homogenität
shapiro.test(relevant_data$stress_overall) # p = 0.0008145; ✗ significantly not normal!
by(relevant_data$stress_overall, relevant_data$condition, shapiro.test)
# 10%: p = 0.4958 => ✓ not sign.
# 50%: p = 0.228 => ✓ not sign.
# 90%: p = 0.0004931 => ✗ sign.!

leveneTest(relevant_data$stress_overall, relevant_data$condition)
# Pr 0.2447 > 0.05; ✓ variances not significantly different
# => Using Wilcox' Anova

t1way(stress_overall ~ condition, data = relevant_data)
# F = 4.1712 / df_1 = 2 / df_2 = 23.47 / p = .02818
# ✓ Es gab einen signifikanten Unterschied der Stufen des Assistenzsystems bzgl. des durchschnittlich empfundenen Stresses, F(2, 23.47) = 4.1712, p < .05

shapiro.test(relevant_data$monotony_overall) # p = 0.009248; ✗ significantly not normal!
by(relevant_data$monotony_overall, relevant_data$condition, shapiro.test)

t1way(monotony_overall ~ condition, data = relevant_data)


# ############################################################################################################
# Analyse 3c - Post Hoc
# Wilcox' robuste post hoc Analyse
# ############################################################################################################

mcppb20(stress_overall ~ condition, data = relevant_data, tr = .2, crit = .05, nboot = 2000)
#            psihat ci.lower ci.upper p-value
# 10 vs. 50 0.39286 -0.14286  1.00000  0.2320 - ✗ nicht signifikant
# 10 vs. 90 0.67857  0.32143  1.10714  0.0035 - ✓ signifikant
# 50 vs. 90 0.28571 -0.28571  0.85714  0.4030 - ✗ nicht signifikant

mcppb20(monotony_overall ~ condition, data = relevant_data, tr = .2, crit = .05, nboot = 2000)
#             psihat ci.lower ci.upper p-value
# 10 vs. 50  0.07143 -0.35714  0.64286  0.7455
# 10 vs. 90 -0.17857 -0.64286  0.21429  0.4705
# 50 vs. 90 -0.25000 -0.92857  0.21429  0.3810




# ############################################################################################################
# Analyse 3d - Blöcke
# Mixed Anova: Faktor System (90, 50, 10 - between) und Messwiederholung (1. vs. 2. Block - within)
# ############################################################################################################

# Dimension stress
# transform data to long format
long_data <- melt(relevant_data, id = c("VP", "condition"), measure.vars = c("stress_01", "stress_23"))
names(long_data) <- c("VP", "condition", "groups", "delta")
long_data$block <- gl(2, 66, labels = c("01", "23"))

# define contrast; just comparing delta of block 0 and 1 against delta of block 2 and 3 => only one contrast
contrasts(long_data$block) <- cbind(
  c(-1, 1)
)

stressModel <- ezANOVA(
  data = long_data,
  dv = .(delta),
  wid = .(VP),
  between = .(condition),
  within = .(block),
  type = 3,
  detailed = TRUE
)
stressModel
#                                Effect DFn DFd         SSn       SSd           F           p p<.05          ges
# 1                         (Intercept)   1  60 10.93939394 108.72727  6.03678930 0.016919578     * 0.0618256551
# 2                           condition   2  60 16.46969697 108.72727  4.54431438 0.014532500     * 0.0902599020
# 3                 startWithAssistance   1  60 29.12121212 108.72727 16.07023411 0.000171243     * 0.1492467774
# 5                               block   1  60  0.48484848  57.27273  0.50793651 0.478796076       0.0029122679
# ... keine Interaktionseffekte
# => Haupteffekt der condition (10 / 50 / 90); davon war auszugehen
# => Haupteffekt der Bedingung "startWithAssistance" - Wow, das hätte ich nicht gedacht!

# Mal genauer rein sehen:
startedWithAssistance <- stat.desc(relevant_data$stress_overall[relevant_data$startWithAssistance == "True"])
notStartedWithAssistance <- stat.desc(relevant_data$stress_overall[relevant_data$startWithAssistance == "False"])
startedWithAssistance["mean"] # -0.7575758 => weniger Belastung mit AS
notStartedWithAssistance["mean"] # 0.1818182 => mehr melastung mit AS

# Unterschied gibt es nur um Durchschnitt der Stress-Werte; nicht signifikant bei exklusiver Betrachtung des letzten Block-Deltas:
startedWithAssistance <- stat.desc(relevant_data$stress_23[relevant_data$startWithAssistance == "True"])
notStartedWithAssistance <- stat.desc(relevant_data$stress_23[relevant_data$startWithAssistance == "False"])
t.test(startedWithAssistance, notStartedWithAssistance)
# t = -1.0407, df = 25.991, p-value = 0.3076

t.test(
  relevant_data$stress_overall[relevant_data$condition == 10],
  relevant_data$stress_overall[relevant_data$condition == 50]
)

t.test(
  relevant_data$stress_overall[relevant_data$condition == 50],
  relevant_data$stress_overall[relevant_data$condition == 90]
)

