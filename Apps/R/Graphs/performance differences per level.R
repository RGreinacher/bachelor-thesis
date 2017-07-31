library(readr)
library(ggplot2)
library(gridExtra)

# constants

data_frame <- read_delim("~/Nextcloud/Uni/Bachelorarbeit/Apps/Auswertung/data/data_frame.csv", ";", escape_double = FALSE, trim_ws = TRUE)
color_coding = c(
  "keine Assistenz" = "#7A88A5",
  "10% Assistenz" = "#BF3865",
  "50% Assistenz" = "#E0B558",
  "90% Assistenz" = "#93B449")
color_coding_block_level = c(
  "1-kA" = "#7A88A5",
  "2-kA" = "#7A88A5",
  "3-kA" = "#7A88A5",
  "4-kA" = "#7A88A5",
  "1-10" = "#BF3865",
  "2-10" = "#BF3865",
  "3-10" = "#BF3865",
  "4-10" = "#BF3865",
  "1-50" = "#E0B558",
  "2-50" = "#E0B558",
  "3-50" = "#E0B558",
  "4-50" = "#E0B558",
  "1-90" = "#93B449",
  "2-90" = "#93B449",
  "3-90" = "#93B449",
  "4-90" = "#93B449")

# box blots / medians for combined blocks

relevant_data <- data.frame(
  "condition" = character(),
  "block" = numeric(),
  "block_condition" = character(),
  "correctness" = numeric())

for (block_id in 0:3) {
  for (subject_id in 1:66) {
    data_row = data_frame[subject_id,]

    datum = data_row[[sprintf('block_%d_correctness', block_id)]]

    if (data_row[[sprintf('block_%d_assistance_present', block_id)]] == "True") {
      condition = data_row$assistance_level
    } else {
      condition = "kA"
    }

    relevant_data <- rbind(
      relevant_data,
      data.frame(
        condition = condition,
        block = (block_id + 1),
        block_condition = sprintf('%d-%s', (block_id + 1), condition),
        correctness = datum))
  }
}

relevant_data$block_condition <- factor(relevant_data$block_condition, levels = c("1-kA", "1-10", "1-50", "1-90", "2-kA", "2-10", "2-50", "2-90", "3-kA", "3-10", "3-50", "3-90", "4-kA", "4-10", "4-50", "4-90"))
ggplot(
  relevant_data,
  aes(
    block_condition,
    correctness,
    colour = block_condition)) +
  geom_boxplot() +
  labs(
    x = "Block Nr. - Stufe der Assistenz",
    y = "Median der Richtigkeiten") +
  scale_color_manual(
    name="Legende",
    values=color_coding_block_level) +
  theme(legend.position="none") +
  ggtitle("Median der Richtigkeiten pro Block, jeweils nach Stufen") +
  ggsave(
    "box_plot_median_correctness_per_block_and_level.png",
    width = 8,
    height = 4.5)



# box blots / medians for combined blocks

relevant_data <- data.frame(
  "condition" = character(),
  "correctness" = numeric())

for (i in 1:66) {
  data_row = data_frame[i,]

  if (data_row$block_0_assistance_present == "True") {
    correctness_with_assistance = data_row$block_0_correctness + data_row$block_2_correctness
    correctness_without_assistance = data_row$block_1_correctness + data_row$block_3_correctness
  } else {
    correctness_with_assistance = data_row$block_1_correctness + data_row$block_3_correctness
    correctness_without_assistance = data_row$block_0_correctness + data_row$block_2_correctness
  }
  
  relevant_data <- rbind(
    relevant_data,
    data.frame(
      condition = sprintf("%d%% Assistenz", data_row$assistance_level), # condition / assistance level
      correctness = (correctness_with_assistance / 2)))
  
  relevant_data <- rbind(
    relevant_data,
    data.frame(
      condition = "keine Assistenz",
      correctness = (correctness_without_assistance / 2)))
}

relevant_data$condition <- factor(relevant_data$condition, levels = c("keine Assistenz", "10% Assistenz", "50% Assistenz", "90% Assistenz"))
ggplot(
  relevant_data,
  aes(
    condition,
    correctness,
    colour = condition)) +
  geom_boxplot() +
  labs(
    x = "Stufen der Assistenz",
    y = "Median der Richtigkeiten") +
  scale_color_manual(
    name="Legende",
    values=color_coding) +
  theme(legend.position="none") +
  ggtitle("Median der Richtigkeiten über alle Blöcke nach Stufen") +
  ggsave(
    "box_plot_median_correctness_per_level.png",
    width = 8,
    height = 4.5)
