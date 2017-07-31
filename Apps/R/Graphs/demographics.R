library(readr)
library(ggplot2)

data_frame <- read_delim("~/Nextcloud/Uni/Bachelorarbeit/Apps/Auswertung/data/data_frame.csv", ";", escape_double = FALSE, trim_ws = TRUE)
counts <- table(data_frame$sex)
colorPalette <- c("#7A88A5", "#93B449")

# bar chart ob subject sex
data<-data.frame(data_frame$sex, data_frame$age)
ggplot(
  data,
  aes(
    x=data_frame$sex
  )
) +
geom_bar(stat="count") +
theme_bw() +
theme(
  panel.background = element_blank(),
  panel.border = element_blank(),
  axis.line = element_line(color = '#BFBFBF'),
  plot.background = element_rect(fill = "transparent",colour = NA)
) + 
scale_fill_manual(
  values = colorPalette
) +
scale_x_discrete(
  labels=c(
    "männlich",
    "weiblich"
  )
) +
xlab("Geschlechter") +
ylab("Anzahl der Versuchspersonen")
ggsave(
  "demog_sex_studying.png",
  bg = "transparent",
  width=5,
  height=5,
  units="in",
  dpi=100
)

# histogram of subject ages
library(pastecs)
stat.desc(data_frame$age)
data<-data.frame(data_frame$age)
ggplot(
  data,
  aes(
    x=data_frame$age
  )
) +
geom_histogram(
  position="stack",
  alpha=1,
  binwidth=1
) +
theme_bw() +
theme(
  panel.background = element_blank(),
  panel.border = element_blank(),
  axis.line = element_line(color = '#BFBFBF'),
  plot.background = element_rect(fill = "transparent",colour = NA)
) + 
guides(fill=guide_legend(title="Geschlecht")) +
scale_fill_manual(
  values = colorPalette
) + 
scale_y_continuous(breaks = seq(0, 10, 2)) +
xlab("Alter in Jahren") +
ylab("Anzahl der Versuchspersonen")
ggsave(
  "demog_ages.png",
  bg = "transparent",
  width=5,
  height=5,
  units="in",
  dpi=100
)

# histogram of subject ages
data<-data.frame(data_frame$sex, data_frame$age)
ggplot(
  data,
  aes(
    x=data_frame$age,
    group=data_frame$sex,
    fill=data_frame$sex
  )
) +
  geom_histogram(
    position="stack",
    alpha=1,
    binwidth=1
  ) +
  theme_bw() +
  theme(
    panel.background = element_blank(),
    panel.border = element_blank(),
    axis.line = element_line(color = '#BFBFBF'),
    plot.background = element_rect(fill = "transparent",colour = NA)
  ) + 
  guides(fill=guide_legend(title="Geschlecht")) +
  scale_fill_manual(
    values = colorPalette
  ) + 
  scale_y_continuous(breaks = seq(0, 10, 2)) +
  xlab("Alter in Jahren") +
  ylab("Anzahl der Versuchspersonen")
ggsave(
  "demog_ages_sex.png",
  bg = "transparent",
  width=5,
  height=5,
  units="in",
  dpi=100
)

# histogram of studying
data<-data.frame(data_frame$currently_studying, data_frame$age)
ggplot(data,
       aes(x=data_frame$age,
           group=data_frame$currently_studying,
           fill=data_frame$currently_studying)) +
  geom_histogram(position="stack",
                 alpha=1,
                 binwidth=1) +
  theme_bw() +
  guides(fill=guide_legend(title="Studierende"))
ggsave("demog_ages_studying.png")

# histogram of computer experience
data<-data.frame(data_frame$sex, data_frame$experience_computer)
ggplot(data,
       aes(x=data_frame$experience_computer,
           group=data_frame$sex,
           fill=data_frame$sex))+
  geom_histogram(position="stack",
                 alpha=1,
                 binwidth=1)+
  theme_bw() + 
  guides(fill=guide_legend(title="Geschlecht"))
ggsave("demog_ages_computer_exp.png")
