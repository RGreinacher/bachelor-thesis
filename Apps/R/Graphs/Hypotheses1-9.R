library(readr)
library(ggplot2)
library(Rmisc)
library(ggsignif)




# ##############################################################################
# Prep: Generiere Liste
# - Assistenz-Stufe
# - Richtigkeitsunterschied pro VP
# - Geschwindigkeitsunterschied pro VP
# - Auslassunsunterschied (wie viele Annotationsstellen wurden übersehen) pro VP
# jeweils nach Schema: (mit Assistenz - ohne Assistenz)
# ##############################################################################

data_frame <- read_delim("~/Nextcloud/Uni/Bachelorarbeit/Apps/Auswertung/data/data_frame.csv", ";", escape_double = FALSE, trim_ws = TRUE)

subject_id = factor(data_frame$subject_id)
condition <- factor(data_frame$assistance_level)
startedWithAssistance <- factor(data_frame$block_0_assistance_present)

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
  startedWithAssistance,
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

colorPalette <- c("#EC4F2E", "#7A88A5", "#93B449")
pd <- position_dodge(0.1)
dev.off()




# ##############################################################################
# Bar Chart Correctness
# ##############################################################################
data<-data.frame(relevant_data$correctness, relevant_data$condition)
tgc <- summarySE(data, measurevar="relevant_data.correctness", groupvars=c("relevant_data.condition"))
head(tgc)
by(relevant_data$correctness, relevant_data$condition, stat.desc)

ggplot(
  tgc,
  aes(
    x=relevant_data.condition,
    y=relevant_data.correctness,
    fill=relevant_data.condition
  )
) +
stat_summary(fun.y = mean, geom = "bar") + 
geom_errorbar(
  aes(
    ymin=relevant_data.correctness-se,
    ymax=relevant_data.correctness+se
  ),
  width=.1,
  position = pd
) +
stat_summary(
  aes(
    label = round(..y.., 2)
  ),
  fun.y = mean,
  geom = "text",
  size=4,
  vjust = -0.5,
  hjust = -0.1
) +
geom_hline(yintercept = 0, color = '#BFBFBF') +
geom_signif(
  comparisons = list(
    c("10", "50"),
    c("50", "90")
  ), 
  map_signif_level=TRUE
) +
theme_bw() +
theme(
  panel.background = element_blank(),
  panel.border = element_blank(),
  axis.line = element_line(color = '#BFBFBF'),
  axis.title.x=element_blank(),
  axis.text.x = element_text(size = 11),
  plot.background = element_rect(fill = "transparent",colour = NA)
) +
guides(fill=FALSE) +
scale_fill_manual(
  values=colorPalette
) +
scale_x_discrete(
  labels=c(
    "10%",
    "50% *",
    "90% ***"
  )
) +
ylab("Delta der mittleren Richtigkeit in %")
ggsave(
  "analysis_correctness_contrasts.png",
  bg = "transparent",
  width=5,
  height=5,
  units="in",
  dpi=150
)




# ##############################################################################
# Bar Chart Tempo
# ##############################################################################
data<-data.frame(relevant_data$tempo, relevant_data$condition)
tgc <- summarySE(data, measurevar="relevant_data.tempo", groupvars=c("relevant_data.condition"))
head(tgc)
by(relevant_data$tempo, relevant_data$condition, stat.desc)

ggplot(
  tgc,
  aes(
    x=relevant_data.condition,
    y=relevant_data.tempo,
    fill=relevant_data.condition
  )
) +
stat_summary(fun.y = mean, geom = "bar") + 
geom_errorbar(
  aes(
    ymin=relevant_data.tempo-se,
    ymax=relevant_data.tempo+se
  ),
  width=.1,
  position = pd
) +
stat_summary(
  aes(
    label = round(..y.., 2)
  ),
  fun.y = mean,
  geom = "text",
  size=4,
  vjust = -0.5,
  hjust = -0.1
) +
geom_hline(yintercept = 0, color = '#BFBFBF') +
geom_signif(
  comparisons = list(
    c("10", "50"),
    c("50", "90")
  ), 
  map_signif_level=TRUE
) +
theme_bw() +
theme(
  panel.background = element_blank(),
  panel.border = element_blank(),
  axis.line = element_line(color = '#BFBFBF'),
  axis.title.x=element_blank(),
  axis.text.x = element_text(size = 11),
  plot.background = element_rect(fill = "transparent",colour = NA)
) +
guides(fill=FALSE) +
scale_fill_manual(
  values=colorPalette
) +
scale_x_discrete(
  labels=c(
    "10%",
    "50% *",
    "90% ***"
  )
) +
ylab("Delta der mittleren Annotationsdauer in s")
ggsave(
  "analysis_tempo_contrast.png",
  bg = "transparent",
  width=5,
  height=5,
  units="in",
  dpi=150
)




# ##############################################################################
# Bar Chart Misses
# ##############################################################################
data<-data.frame(relevant_data$misses, relevant_data$condition)
tgc <- summarySE(data, measurevar="relevant_data.misses", groupvars=c("relevant_data.condition"))
head(tgc)
by(relevant_data$misses, relevant_data$condition, stat.desc)

ggplot(
  tgc,
  aes(
    x=relevant_data.condition,
    y=relevant_data.misses,
    fill=relevant_data.condition
  )
) +
stat_summary(fun.y = mean, geom = "bar") + 
geom_errorbar(
  aes(
    ymin=relevant_data.misses-se,
    ymax=relevant_data.misses+se
  ),
  width=.1,
  position = pd
) +
stat_summary(
  aes(
    label = round(..y.., 2)
  ),
  fun.y = mean,
  geom = "text",
  size=4,
  vjust = -0.5,
  hjust = -0.1
) +
geom_hline(yintercept = 0, color = '#BFBFBF') +
geom_signif(
  comparisons = list(
    c("10", "50"),
    c("50", "90")
  ), 
  map_signif_level=TRUE
) +
theme_bw() +
theme(
  panel.background = element_blank(),
  panel.border = element_blank(),
  axis.line = element_line(color = '#BFBFBF'),
  axis.title.x=element_blank(),
  axis.text.x = element_text(size = 11),
  plot.background = element_rect(fill = "transparent",colour = NA)
) +
guides(fill=FALSE) +
scale_fill_manual(
  values=colorPalette
) +
scale_x_discrete(
  labels=c(
    "10%",
    "50% *",
    "90% **"
  )
) +
ylab("Delta der mittleren Misses in %")
ggsave(
  "analysis_misses_contrasts.png",
  bg = "transparent",
  width=5,
  height=5,
  units="in",
  dpi=150
)




# ##############################################################################
# Questionnaires
# ##############################################################################
relevant_data <- data.frame(
  "VP" = factor(),
  "condition" = factor(),
  "startWithAssistance" = factor(),
  "stress_overall" = numeric(),
  "stress_01" = numeric(),
  "stress_23" = numeric(),
  "monotony_overall" = numeric(),
  "monotony_01" = numeric(),
  "monotony_23" = numeric()
)

for (i in 1:66) {
  data_row = data_frame[i,]

  if (data_row$block_0_assistance_present == "True") {
    stress_01 = data_row$block_0_questionnaire_stress - data_row$block_1_questionnaire_stress
    stress_23 = data_row$block_2_questionnaire_stress - data_row$block_3_questionnaire_stress

    monotony_01 = data_row$block_0_questionnaire_monotonous - data_row$block_1_questionnaire_monotonous
    monotony_23 = data_row$block_2_questionnaire_monotonous - data_row$block_3_questionnaire_monotonous
  } else {
    stress_01 = data_row$block_1_questionnaire_stress - data_row$block_0_questionnaire_stress
    stress_23 = data_row$block_3_questionnaire_stress - data_row$block_2_questionnaire_stress

    monotony_01 = data_row$block_1_questionnaire_monotonous - data_row$block_0_questionnaire_monotonous
    monotony_23 = data_row$block_3_questionnaire_monotonous - data_row$block_2_questionnaire_monotonous
  }

  relevant_data <- rbind(
    relevant_data,
    data.frame(
      VP = factor(i),
      condition = factor(data_row$assistance_level),
      startWithAssistance = factor(data_row$block_0_assistance_present),
      stress_overall = (stress_01 + stress_23) / 2,
      stress_01 = stress_01,
      stress_23 = stress_23,
      monotony_overall = (monotony_01 + monotony_23) / 2,
      monotony_01 = monotony_01,
      monotony_23 = monotony_23
    )
  )
}




# ##############################################################################
# Bar Chart Stress
# ##############################################################################
data<-data.frame(relevant_data$stress_overall, relevant_data$condition)
tgc <- summarySE(data, measurevar="relevant_data.stress_overall", groupvars=c("relevant_data.condition"))
head(tgc)
by(relevant_data$stress_overall, relevant_data$condition, stat.desc)

ggplot(
  tgc,
  aes(
    x=relevant_data.condition,
    y=relevant_data.stress_overall,
    fill=relevant_data.condition
  )
) +
  stat_summary(fun.y = mean, geom = "bar") + 
  geom_errorbar(
    aes(
      ymin=relevant_data.stress_overall-se,
      ymax=relevant_data.stress_overall+se
    ),
    width=.1,
    position = pd
  ) +
  stat_summary(
    aes(
      label = round(..y.., 2)
    ),
    fun.y = mean,
    geom = "text",
    size=4,
    vjust = -0.5,
    hjust = -0.1
  ) +
  geom_hline(yintercept = 0, color = '#BFBFBF') +
  geom_signif(
    comparisons = list(
      c("10", "50"),
      c("50", "90")
    ), 
    map_signif_level=TRUE
  ) +
  theme_bw() +
  theme(
    panel.background = element_blank(),
    panel.border = element_blank(),
    axis.line = element_line(color = '#BFBFBF'),
    axis.title.x=element_blank(),
    axis.text.x = element_text(size = 11),
    plot.background = element_rect(fill = "transparent",colour = NA)
  ) +
  guides(fill=FALSE) +
  scale_fill_manual(
    values=colorPalette
  ) +
  scale_x_discrete(
    labels=c(
      "10%",
      "50%",
      "90% **"
    )
  ) +
  ylab("Delta des mittleren Stresses (1 bis 7)")
ggsave(
  "analysis_stress_overall.png",
  bg = "transparent",
  width=5,
  height=5,
  units="in",
  dpi=150
)




# ##############################################################################
# Bar Chart Monotony
# ##############################################################################
data<-data.frame(relevant_data$monotony_overall, relevant_data$condition)
tgc <- summarySE(data, measurevar="relevant_data.monotony_overall", groupvars=c("relevant_data.condition"))
head(tgc)
by(relevant_data$monotony_overall, relevant_data$condition, stat.desc)

ggplot(
  tgc,
  aes(
    x=relevant_data.condition,
    y=relevant_data.monotony_overall,
    fill=relevant_data.condition
  )
) +
  stat_summary(fun.y = mean, geom = "bar") + 
  geom_errorbar(
    aes(
      ymin=relevant_data.monotony_overall-se,
      ymax=relevant_data.monotony_overall+se
    ),
    width=.1,
    position = pd
  ) +
  stat_summary(
    aes(
      label = round(..y.., 2)
    ),
    fun.y = mean,
    geom = "text",
    size=4,
    vjust = -0.5,
    hjust = -0.1
  ) +
  geom_hline(yintercept = 0, color = '#BFBFBF') +
  theme_bw() +
  theme(
    panel.background = element_blank(),
    panel.border = element_blank(),
    axis.line = element_line(color = '#BFBFBF'),
    axis.title.x=element_blank(),
    axis.text.x = element_text(size = 11),
    plot.background = element_rect(fill = "transparent",colour = NA)
  ) +
  guides(fill=FALSE) +
  scale_fill_manual(
    values=colorPalette
  ) +
  scale_x_discrete(
    labels=c(
      "10%",
      "50%",
      "90%"
    )
  ) +
  ylab("Delta der mittleren Monotonie (1 bis 7)")
ggsave(
  "analysis_monotony_overall.png",
  bg = "transparent",
  width=5,
  height=5,
  units="in",
  dpi=150
)
