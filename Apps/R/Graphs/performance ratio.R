library(readr)
library(ggplot2)

# constants

data_frame <- read_delim("~/Nextcloud/Uni/Bachelorarbeit/Apps/Auswertung/data/data_frame.csv", ";", escape_double = FALSE, trim_ws = TRUE)
color_coding = c(
  "10% Assistenz" = "#BF3865",
  "keine Assistenz" = "#7A88A5",
  "50% Assistenz" = "#E0B558",
  "90% Assistenz" = "#93B449")


# block wise scatter plot

correctness = c(
  data_frame$block_0_correctness,
  data_frame$block_1_correctness,
  data_frame$block_2_correctness,
  data_frame$block_3_correctness)

minutes_per_block = c(
  (data_frame$block_0_time_block / 60),
  (data_frame$block_1_time_block / 60),
  (data_frame$block_2_time_block / 60),
  (data_frame$block_3_time_block / 60))

condition_block_0 <- table(1:66)
condition_block_0[data_frame$block_0_assistance_present == "False"] <- "keine Assistenz"
assistance_level = data_frame$assistance_level[data_frame$block_0_assistance_present == "True"]
condition_block_0[data_frame$block_0_assistance_present == "True"] <- sprintf("%d%% Assistenz", assistance_level)
condicondition_block_2 <- table(1:66)
condition_block_2[data_frame$block_2_assistance_present == "False"] <- "keine Assistenz"
assistance_level = data_frame$assistance_level[data_frame$block_2_assistance_present == "True"]
condition_block_2[data_frame$block_2_assistance_present == "True"] <- sprintf("%d%% Assistenz", assistance_level)
condition_block_3 <- table(1:66)
condition_block_3[data_frame$block_3_assistance_present == "False"] <- "keine Assistenz"
assistance_level = data_frame$assistance_level[data_frame$block_3_assistance_present == "True"]
condition_block_3[data_frame$block_3_assistance_present == "True"] <- sprintf("%d%% Assistenz", assistance_level)
condition = c(
  condition_block_0,
  condition_block_1,
  condition_block_2,
  condition_block_3)

relevant_data = data.frame(condition, correctness, minutes_per_block)
relevant_data$condition <- factor(relevant_data$condition, levels = c("10% Assistenz", "keine Assistenz", "50% Assistenz", "90% Assistenz"))

ggplot(
  relevant_data,
  aes(
    x=correctness,
    y=minutes_per_block,
    color=condition
  )
) +
geom_point(shape=1) + 
geom_smooth(
  method=lm,
  se=FALSE,
  fullrange=FALSE) + 
ggtitle("Blockweise richtige Annotationen im Verhältnis zur Bearbeitungszeit pro Block") +
scale_color_manual(
  name="Legende",
  values=color_coding)
ggsave("scatter_correctness_time_per_block.png")



# subject scatter plot

relevant_data <- data.frame(
  "condition" = character(),
  "correctness" = numeric(),
  "processing_time" = numeric())

for (i in 1:66) {
  data_row = data_frame[i,]

  if (data_row$block_0_assistance_present == "True") {
    correctness_with_assistance = data_row$block_0_correctness + data_row$block_2_correctness
    processing_time_with_assistance = data_row$block_0_time_block + data_row$block_2_time_block

    correctness_without_assistance = data_row$block_1_correctness + data_row$block_3_correctness
    processing_time_without_assistance = data_row$block_1_time_block + data_row$block_3_time_block
  } else {
    correctness_with_assistance = data_row$block_1_correctness + data_row$block_3_correctness
    processing_time_with_assistance = data_row$block_1_time_block + data_row$block_3_time_block

    correctness_without_assistance = data_row$block_0_correctness + data_row$block_2_correctness
    processing_time_without_assistance = data_row$block_0_time_block + data_row$block_2_time_block
  }
  
  relevant_data <- rbind(
    relevant_data,
    data.frame(
      condition = sprintf("%d%% Assistenz", data_row$assistance_level), # condition / assistance level
      correctness = (correctness_with_assistance / 2),
      processing_time = (processing_time_with_assistance / 60)))

    relevant_data <- rbind(
    relevant_data,
    data.frame(
      condition = "keine Assistenz",
      correctness = (correctness_without_assistance / 2),
      processing_time = (processing_time_without_assistance / 60)))
}

relevant_data$condition <- factor(relevant_data$condition, levels = c("10% Assistenz", "keine Assistenz", "50% Assistenz", "90% Assistenz"))

ggplot(
  relevant_data,
  aes(
    x=correctness,
    y=processing_time,
    color=condition)) +
  geom_point(shape=1) + 
  geom_smooth(
    method=lm,
    se=FALSE,
    fullrange=FALSE) + 
  ggtitle("Versuchspersonenweise richtige Annotationen im Verhältnis zur Bearbeitungszeit pro Block") +
  scale_color_manual(
    name="Legende",
    values=color_coding)
ggsave("scatter_correctness_time_per_subject.png")

