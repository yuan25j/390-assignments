################################################################################
# prep
################################################################################
rm(list=ls()) 
# load packages
library(plot0) 
# set output path
res_dir <- paste0(getwd(), '/results/')

################################################################################
# figure 1a 
################################################################################
# load -------------------------------------------------------------------------
filepath <- paste0(getwd(), '/data')
filename <- 'data_new.csv'
dt <- MyFread(filename, filepath)

# Compute necessary statistics for plotting
# Adjusted to calculate confidence intervals at more points (e.g., every 5th percentile)

# Create a function to compute mean and confidence intervals at desired intervals
compute_ci <- function(data, col_y, col_x, col_group, interval, ci_level = 0.95) {
  data[, percentile := ntile(get(col_x), 100)]  # Calculate percentiles
  
  # Define the intervals (e.g., every 5th percentile)
  data[, interval_group := floor((percentile - 1) / interval) * interval + interval / 2]
  
  # Compute mean and standard error within each interval and group
  ci_data <- data[, .(
    mean_y = mean(get(col_y), na.rm = TRUE),
    se_y = sd(get(col_y), na.rm = TRUE) / sqrt(.N)
  ), by = .(interval_group, get(col_group))]
  
  # Calculate confidence intervals
  ci_multiplier <- qt(ci_level / 2 + 0.5, df = Inf)
  ci_data[, `:=`(
    ci_lower = mean_y - ci_multiplier * se_y,
    ci_upper = mean_y + ci_multiplier * se_y
  )]
  
  setnames(ci_data, "get", col_group)
  return(ci_data)
}

# Use the function to compute confidence intervals at every 5th percentile
interval_width <- 5  # Adjust interval width as desired
df_ci <- compute_ci(
  data = dt,
  col_y = 'gagne_sum_t',
  col_x = 'risk_score_t',
  col_group = 'race',
  interval = interval_width,
  ci_level = 0.95
)

# Labels and settings for Figure 1a
titlename <- ''
subtitlename <- ''
groupbycolorname <- 'Race'
xname <- 'Percentile of Algorithm Risk Score'
yname <- 'Number of Active Chronic Conditions'
color_scheme <- c("#764885", "#ffa600") 
linetype_scheme <- c('twodash', 'solid') 
group_label <- c("Black", "White")

default_in_percentile <- 97
additional_screen_percentile <- 55

# Plot Figure 1a with enhanced confidence intervals
ga <- ggplot(data = df_ci, aes(
    x = interval_group,
    y = mean_y,
    color = race,
    linetype = race,
    group = race
  )) +
  theme_bw() +
  labs(
    title = titlename,
    subtitle = subtitlename,
    color = groupbycolorname,
    x = xname,
    y = yname
  ) +
  scale_x_continuous(
    breaks = seq(0, 100, 10),
    limits = c(0, 100)
  ) +
  scale_y_continuous(
    breaks = seq(0, max(df_ci$mean_y + df_ci$se_y), 1)
  ) +
  scale_color_manual(
    values = color_scheme,
    labels = group_label,
    name = groupbycolorname
  ) +
  scale_linetype_manual(
    values = linetype_scheme,
    labels = group_label,
    name = groupbycolorname
  ) +
  theme(
    legend.key.size = grid::unit(5, "lines"),
    legend.key.height = grid::unit(1, "lines"),
    legend.position = 'bottom',
    aspect.ratio = 1
  ) +
  geom_point(size = 2) +
  geom_errorbar(
    aes(
      ymin = ci_lower,
      ymax = ci_upper
    ),
    width = interval_width / 2,
    size = 0.7
  ) +
  geom_smooth(
    method = "glm",
    formula = y ~ x,
    method.args = list(family = gaussian(link = 'log')),
    se = FALSE,
    size = 1
  ) +
  geom_vline(
    xintercept = default_in_percentile,
    colour = "black",
    linetype = "dashed"
  ) +
  geom_text(
    aes(
      x = default_in_percentile,
      y = max(df_ci$mean_y) * 0.9,
      label = "Defaulted into program"
    ),
    colour = "black",
    hjust = 1.1,
    size = 3
  ) +
  geom_vline(
    xintercept = additional_screen_percentile,
    colour = "dark gray",
    linetype = "dashed"
  ) +
  geom_text(
    aes(
      x = additional_screen_percentile,
      y = max(df_ci$mean_y) * 0.8,
      label = "Referred for screen"
    ),
    colour = "dark gray",
    hjust = -0.1,
    size = 3
  )
################################################################################
# figure 1b
################################################################################
source(paste0(getwd(), '/code/figure1/figure1b.R'))

# load -------------------------------------------------------------------------
filepath <- paste0(getwd(), '/results')
filename <- 'figure1b.csv'
dt <- MyFread(filename, filepath)

dt_long <- gather(dt, before_or_after, frac, before:after, factor_key=TRUE)
dt_long$before_or_after <- as.factor(dt_long$before_or_after)

# labels -----------------------------------------------------------------------
titlename <- ''
subtitlename <- ''
groupbycolorname <- ''
xname <- 'Percentile of Algorithm Risk Score'
yname <- 'Fraction Black'
color_scheme1 <- c('#b54984', '#ff7547') 
linetype_scheme1 <- c('solid', 'dashed') 
group_label1 <- c("Original", "Simulated")

program_size <- 90

dt_long <- as.data.table(dt_long)
dt_long <- dt_long[percentile >= 55]
# plot ------------------------------------------------------------------------

gb <- ggplot(data = dt_long, 
             aes(x = percentile, y = frac, color = before_or_after, linetype =
                 before_or_after, group = before_or_after)) + 
   theme_bw() + 
   labs(title = titlename, subtitle = subtitlename, color = groupbycolorname, x
        = xname, y = yname) +
   scale_x_continuous(breaks = c(seq(55, 95, 5), 99)) +
   scale_y_continuous(breaks = seq(0, 1, by = 0.05)) +
   scale_color_manual(values = color_scheme1, labels = group_label1, name = groupbycolorname) +
   scale_linetype_manual(values = linetype_scheme1, labels = group_label1, name = groupbycolorname) +
   theme(legend.key.size = grid::unit(5,"lines")) + 
   theme(legend.key.height= grid::unit(1,"lines")) + 
   theme(legend.position = 'bottom') + 
   theme(aspect.ratio = 1) + 
   geom_point(shape = 4) +
   geom_smooth(span = 0.99, se = TRUE, level = 0.95) + 
   geom_vline(aes(xintercept=default_in_percentile), colour="black", linetype="dashed") +
   geom_text(aes(x=default_in_percentile, label="Defaulted into program", y =
                 0.45), colour="black", hjust = 1.2, size = 2) + 
   geom_vline(aes(xintercept=additional_screen_percentile), colour="dark gray",
              linetype="dashed") +
   geom_text(aes(x=additional_screen_percentile, label="Referred for screen", y
                 = 0.45), colour="dark gray", hjust = -0.2, size = 2) 

################################################################################
# export 
################################################################################
# png 
ggsave(paste0(res_dir, 'figure12.png'), grid.arrange(ga, gb, ncol = 2, respect=TRUE), width = 14, height = 7)
# eps 
ggsave(paste0(res_dir, 'figure12.eps'), device="eps", grid.arrange(ga, gb, ncol = 2, respect=TRUE), width = 14, height = 7)
