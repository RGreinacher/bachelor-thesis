library(readr)
library(ggplot2)
library(Hmisc)

# constants

data_frame <- read_delim("~/Nextcloud/Uni/Bachelorarbeit/Apps/Auswertung/data/data_frame.csv", ";", escape_double = FALSE, trim_ws = TRUE)
data_frame$assistance_level <- factor(data_frame$assistance_level, levels = c(10, 50, 90))

# mean correctness difference per level
combined_blocks = (data_frame$assistance_no_assistance_correctness_difference_block_0_1 + data_frame$assistance_no_assistance_correctness_difference_block_2_3) / 2
ggplot(
  data_frame,
  aes(
    data_frame$assistance_level,
    combined_blocks)) +
  stat_summary(
    fun.y = mean,
    geom = "bar",
    width = 0.7,
    fill = "White",
    colour = "Black") +
  stat_summary(
    fun.data = mean_cl_normal,
    geom = "errorbar",
    width = 0.2) +
  labs(
    x = "Stufen der Assistenz",
    y = "Durschschn. Richtigkeitsdifferenz") +
  ggtitle("Richtigkeitsunterschiede nach Stufen")
ggsave(
  "bar_chart_mean_correctness_difference_per_level.png",
  width = 5.3,
  height = 3)

# mean processing time difference per level
combined_blocks = (data_frame$assistance_no_assistance_time_difference_block_0_1 + data_frame$assistance_no_assistance_time_difference_block_2_3) / 2
ggplot(
  data_frame,
  aes(
    data_frame$assistance_level,
    combined_blocks)) +
  stat_summary(
    fun.y = mean,
    geom = "bar",
    width = 0.7,
    fill = "White",
    colour = "Black") +
  stat_summary(
    fun.data = mean_cl_normal,
    geom = "errorbar",
    width = 0.2) +
  labs(
    x = "Stufen der Assistenz",
    y = "Durschschn. Bearbeitungszeitdifferenz") +
  ggtitle("Bearbeitungszeitunterschiede nach Stufen")
ggsave(
  "bar_chart_mean_time_difference_per_level.png",
  width = 5.3,
  height = 3)
