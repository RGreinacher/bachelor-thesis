library(readr)
library(pastecs)
library(compute.es)
library(car)
library(WRS2)
library(ez)
library(reshape)
#library(nlme)
library(lme4)
library(Hmisc)




# ##############################################################################
# Prep: Generiere Liste
# - Assistenz-Stufe
# - Richtigkeitsunterschied pro VP
# - Geschwindigkeitsunterschied pro VP
# - Auslassunsunterschied (wie viele Annotationsstellen wurden übersehen) pro VP
# jeweils nach Schema: (mit Assistenz - ohne Assistenz)
# ##############################################################################

data_frame <- read_delim("~/Nextcloud/Uni/Bachelorarbeit/Apps/Auswertung/data/data_frame.csv", ";", escape_double = FALSE, trim_ws = TRUE)
stat.desc(data_frame$age)
subject_id = factor(data_frame$subject_id)
condition <- factor(data_frame$assistance_level)

correctness <- (data_frame$assistance_no_assistance_correctness_difference_block_0_1 + data_frame$assistance_no_assistance_correctness_difference_block_2_3) / 2
correctness_01 <- data_frame$assistance_no_assistance_correctness_difference_block_0_1
correctness_23 <- data_frame$assistance_no_assistance_correctness_difference_block_2_3

tempo <- (data_frame$assistance_no_assistance_correct_time_difference_block_0_1 + data_frame$assistance_no_assistance_correct_time_difference_block_2_3) / 2
tempo_01 <- data_frame$assistance_no_assistance_correct_time_difference_block_0_1
tempo_23 <- data_frame$assistance_no_assistance_correct_time_difference_block_2_3

misses <- ((data_frame$assistance_no_assistance_misses_ratio_difference_block_0_1 + data_frame$assistance_no_assistance_misses_ratio_difference_block_2_3) / 2) * 100.0
misses_01 <- data_frame$assistance_no_assistance_misses_ratio_difference_block_0_1 * 100.0
misses_23 <- data_frame$assistance_no_assistance_misses_ratio_difference_block_2_3 * 100.0

relevant_data <- data.frame(
  subject_id,
  condition,
  correctness,
  correctness_01,
  correctness_23,
  tempo,
  tempo_01,
  tempo_23,
  misses,
  misses_01,
  misses_23
)




# ###############################################################################################################
# Analyse 1a - One Sample T-Test
# Test ob die generelle Differenz (mit Assistenzsystem - ohne Assistenzsystem) pro Stufe signifikant größer 0 ist
# Ergebnis: Die Assistenzsysteme machen in allen drei Dimensionen einen signifikanten Unterschied
# ###############################################################################################################

# Dimension correctness
t.test(relevant_data$correctness[relevant_data$condition == 10])
# t = -0.52058, df = 21, p-value = 0.6081, mean of x = -0.6216478 - ✗
t.test(relevant_data$correctness[relevant_data$condition == 50])
# t = 2.1231, df = 21, p-value = 0.0458, mean of x = 3.669523 - ✓
t.test(relevant_data$correctness[relevant_data$condition == 90])
# t = 4.3667, df = 21, p-value = 0.0002704, mean of x = 6.052875 - ✓ 

# Dimension tempo
t.test(relevant_data$tempo[relevant_data$condition == 10])
# t = 0.76246, df = 21, p-value = 0.4543, mean of x = 0.5139075 - ✗
t.test(relevant_data$tempo[relevant_data$condition == 50])
# t = -2.1511, df = 21, p-value = 0.04326, mean of x = -1.654795 - ✓
t.test(relevant_data$tempo[relevant_data$condition == 90])
# t = -6.4163, df = 21, p-value = 2.327e-06, mean of x = -1.93187 - ✓

# Dimension misses
t.test(relevant_data$misses[relevant_data$condition == 10])
# t = -1.1764, df = 21, p-value = 0.2526, mean of x = -1.549032 - ✗
t.test(relevant_data$misses[relevant_data$condition == 50])
# t = -2.3831, df = 21, p-value = 0.02669, mean of x = -2.798305 - ✓
t.test(relevant_data$misses[relevant_data$condition == 90])
# t = -3.5905, df = 21, p-value = 0.001722, mean of x = -3.93995 - ✓




# ###############################################################################################################
# Analyse 1b - Correlation / Effektstärken
# Test der Effektstärken der Assistenz auf die drei Leistungsdimensionen
# Ergebnis: Die Assistenzsysteme machen in allen drei Dimensionen einen signifikanten Unterschied
# ###############################################################################################################

rcorr(
  as.matrix(
    data.frame(
      data_frame$assistance_level,
      relevant_data$correctness
    )
  )
)
# r = 0.38, p = 0.0018 **

rcorr(
  as.matrix(
    data.frame(
      data_frame$assistance_level,
      relevant_data$tempo
    )
  )
)
# r = -0.33, p = 0.0068 **

rcorr(
  as.matrix(
    data.frame(
      data_frame$assistance_level,
      relevant_data$misses
    )
  )
)
# r = -0.17, p = 0.1603




# ############################################################################################################
# Analyse 2a - ANOVA
# Vergleich der Differenzen (mit Assistenzsystem - ohne Assistenzsystem) zwischen allen drei Gruppen (between)
# also Diff.(90) vs. Diff (50) vs. Diff (10)
# ############################################################################################################

# Dimension correctness
# Wilcox' Robust Statistics, ANOVA based on 20% trimmed means
t1way(correctness ~ condition, data = relevant_data)
# F = 7.758 / df_1 = 2 / df_2 = 25.66 / p = .00232
# ✓ Es gab einen signifikanten Unterschied der Stufen des Assistenzsystems bzgl. der Richtigkeit der Annotationen, F(2, 25.66) = 7.758, p < .01


# Dimension tempo
# Welch's F; One-way analysis of means (not assuming equal variances)
oneway.test(tempo ~ condition, data = relevant_data)
# F = 5.3995, num df = 2.000, denom df = 35.419, p-value = 0.008979
# ✓ Es gab einen signifikanten Unterschied der Stufen des Assistenzsystems bzgl. der durschnittlichen Annotationsgeschwindigkeit, F(2, 35.419) = 5.3995, p < .05


# Dimension misses
# Standard One-way ANOVA
missesModel <- aov(misses ~ condition, data = relevant_data)
summary(missesModel)
#             Df  Sum Sq  Mean Sq F value Pr(>F)
# condition    2 0.00629 0.003146   0.994  0.376
# Residuals   63 0.19944 0.003166
# ✗ Es gab keinen signifikanten Unterschied der Stufen des Assistenzsystems bzgl. der Anzahl der übersehenen Annotationsstellen, F(2, 63) = 0.994, p > .05




# ############################################################################################################
# Analyse 2b - Blöcke als Within Faktor, Assistenz Stufen als Between Faktor
# Kontraste:
# - Blöcke: Delta aus Block 0 und 1 vs. Delta aus Block 2 und 3
# - Assistenz-Stufe: 1. Stufe 10% vs. Stufe 50%
#                    2. Stufe 50% vs. Stufe 90%
# ############################################################################################################

# Dimension correctness
# Transformiere Daten in das long data Format
long_data <- melt(
  relevant_data,
  id = c("subject_id", "condition"),
  measure.vars = c("correctness_01", "correctness_23")
)
names(long_data) <- c("subject_id", "condition", "groups", "delta")
long_data$block <- gl(2, 66, labels = c("01", "23"))

# Definiere Kontraste:
contrasts(long_data$block) <- cbind(
  c(-1, 1)
)
contrasts(long_data$condition) <- cbind(
  c(-1, 1, 0),
  c(0, -1, 1)
)

# Typ 3 ANOVA
correctness_model_t3 = ezANOVA(
  data = long_data,
  dv = .(delta),
  wid = .(subject_id),
  between = .(condition),
  within = .(block),
  type = 3,
  detailed = TRUE
)
correctness_model_t3
#            Effect DFn DFd       SSn      SSd          F           p p<.05        ges
# 1     (Intercept)   1  63 1214.7468 5853.316 13.0744770 0.000596141     * 0.10468473
# 2       condition   2  63 1006.7752 5853.316  5.4180259 0.006741719     * 0.08834549
# 3           block   1  63  141.2123 4535.795  1.9613702 0.166272926       0.01341006
# 4 condition:block   2  63  125.7319 4535.795  0.8731774 0.422614743       0.01195756
# => Haupteffekt der Assistenz-Stufe

# daten transformieren?
long_data$delta_log <- log(long_data$delta + 30) # mögliche Korrektur; keine Änderung an Signifikanzen


# ####################################################################


# Dimension tempo
# Transformiere Daten in das long data Format
long_data <- melt(
  relevant_data,
  id = c("subject_id", "condition"),
  measure.vars = c("tempo_01", "tempo_23")
)
names(long_data) <- c("subject_id", "condition", "groups", "delta")
long_data$block <- gl(2, 66, labels = c("01", "23"))

# Definiere Kontraste:
contrasts(long_data$block) <- cbind(
  c(-1, 1)
)
contrasts(long_data$condition) <- cbind(
  c(-1, 1, 0),
  c(0, -1, 1)
)

# Typ 3 ANOVA
tempo_model_t3 = ezANOVA(
  data = long_data,
  dv = .(delta),
  wid = .(subject_id),
  between = .(condition),
  within = .(block),
  type = 3,
  detailed = TRUE
)
tempo_model_t3
#            Effect DFn DFd        SSn      SSd          F           p p<.05          ges
# 1     (Intercept)   1  63 138.480308 1050.347 8.3060729 0.005397164     * 0.089417799
# 2       condition   2  63 157.840730 1050.347 4.7336571 0.012154835     * 0.100660596
# 3           block   1  63   3.703331  359.861 0.6483333 0.423737734       0.002619210
# 4 condition:block   2  63   9.518937  359.861 0.8332287 0.439376271       0.006704766
# => Haupteffekt der Assistenz-Stufe


# ####################################################################


# Dimension misses
# Transformiere Daten in das long data Format
long_data <- melt(
  relevant_data,
  id = c("subject_id", "condition"),
  measure.vars = c("misses_01", "misses_23")
)
names(long_data) <- c("subject_id", "condition", "groups", "delta")
long_data$block <- gl(2, 66, labels = c("01", "23"))

# Definiere Kontraste:
contrasts(long_data$block) <- cbind(
  c(-1, 1)
)
contrasts(long_data$condition) <- cbind(
  c(-1, 1, 0),
  c(0, -1, 1)
)

# Typ 3 ANOVA
misses_model_t3 = ezANOVA(
  data = long_data,
  dv = .(delta),
  wid = .(subject_id),
  between = .(condition),
  within = .(block),
  type = 3,
  detailed = TRUE
)
misses_model_t3
#            Effect DFn DFd        SSn      SSd          F            p p<.05         ges
# 1     (Intercept)   1  63 1007.29408 3988.770 15.9095484 0.0001756136     * 0.142855252
# 2       condition   2  63  125.84767 3988.770  0.9938407 0.3758802298       0.020397679
# 3           block   1  63  152.60523 2055.088  4.6782082 0.0343499214     * 0.024627796
# 4 condition:block   2  63   13.00913 2055.088  0.1994015 0.8197359125       0.002147832
# => Haupteffekt des Blocks




# ############################################################################################################
# Analyse 2c - Kontraste mit T-Tests
# Kontraste:
# - Blöcke: Delta aus Block 0 und 1 vs. Delta aus Block 2 und 3
# - Assistenz-Stufe: 1. Stufe 10% vs. Stufe 50%
#                    2. Stufe 50% vs. Stufe 90%
# ############################################################################################################

# Dimension correctness
# Kontrast 10% vs. 50%
t.test(
  relevant_data$correctness[relevant_data$condition == 10],
  relevant_data$correctness[relevant_data$condition == 50]
)
# t = -2.0426, df = 37.328, p-value = 0.0482 ✓
# => ACHTUNG! Nach Bonferroni Korrektur nicht mehr siginfikant => ✗

# Kontrast 50% vs. 90%
t.test(
  relevant_data$correctness[relevant_data$condition == 50],
  relevant_data$correctness[relevant_data$condition == 90]
)
# t = -1.0757, df = 40.109, p-value = 0.2885 ✗


# #########################################################


# Dimension tempo
# Kontrast 10% vs. 50%
t.test(
  relevant_data$tempo[relevant_data$condition == 10],
  relevant_data$tempo[relevant_data$condition == 50]
)
# t = 2.1204, df = 41.287, p-value = 0.04003 - nicht signifikant nach Bonferroni Korrektur (0,05 / 2) ✗

# Kontrast 50% vs. 90%
t.test(
  relevant_data$tempo[relevant_data$condition == 50],
  relevant_data$tempo[relevant_data$condition == 90]
)
# t = 0.3354, df = 27.286, p-value = 0.7399 ✗


# #########################################################


# Dimension misses
# Block 01 vs. Block 23
t.test(
  relevant_data$misses_01,
  relevant_data$misses_23
)
# t = 1.7913, df = 104.41, p-value = 0.07614 ✗




