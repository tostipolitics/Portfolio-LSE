## ──────────────────────────────────────────────────────────────

# Function for plotting map Figure 1

## ──────────────────────────────────────────────────────────────

plot_pt_map <- function(
  dat,
  year,
  var_fill    = "votos_sh",
  legend_name = "Percentage of vote share PT",
  scale = 100) {
  
  dat_year <- dplyr::filter(dat, election == year)
  dat_year$fill_col <- dat_year[[var_fill]] 

  ggplot() +
    geom_sf(
      data   = dat_year,
      aes(fill = fill_col),
      colour = NA
    ) +
    scale_fill_distiller(
      name      = legend_name,
      palette   = "OrRd",
      breaks    = scales::pretty_breaks(),
      direction = 1,
      na.value  = "grey20",
      labels    = function(x) x * scale
    ) +
    geom_sf(data = ufs, fill = NA, color = "grey20", linewidth = 0.5) +
    theme_minimal() +
    coord_sf(datum = NA)
}

save_pt_map <- function(
  years,
  dat,
  filename,
  var_fill    = "votos_sh",
  legend_name = "Percentage of vote share PT",
  scale = 100,
  ncol   = 4,
  nrow   = 1,
  height = 4,
  width  = 10,
  dpi    = 1000) {

  maps <- lapply(years, \(y) plot_pt_map(
    dat         = dat,
    year        = y,
    var_fill    = var_fill,
    legend_name = legend_name))

  panel <- ggarrange(
    plotlist      = maps,
    labels        = as.character(years),
    common.legend = TRUE, legend = "bottom",
    ncol          = ncol, nrow = nrow
  )

  ggsave(filename = filename, plot = panel,
         height = height, width = width, dpi = dpi)

  invisible(panel)
}


## ──────────────────────────────────────────────────────────────

# Function for plotting map Figure 3

## ──────────────────────────────────────────────────────────────
plot_and_save_exposure_map <- function(df, years_main, legend_name,
                                       filename,
                                       limits    = c(0, 25),
                                       ncol      = 4,
                                       nrow      = 1,
                                       height    = 4,
                                       width     = 10,
                                       dpi       = 1000) {

  # ── inner helpers ──────────────────────────────────────────────────────
  exposure_at <- function(I_YEAR, y, CE_TYPE) {
    dplyr::if_else(
      CE_TYPE == "A",
      NA_real_,
      pmax(0, pmin(I_YEAR, y) - 1978)
    )
  }

  plot_single <- function(y) {
    df %>%
      dplyr::mutate(MD_Exposure = exposure_at(I_YEAR, y, CE_TYPE)) %>%
      ggplot() +
      geom_sf(aes(fill = MD_Exposure), color = NA) +
      scale_fill_distiller(
        name      = legend_name,
        palette   = "YlGn",
        breaks    = scales::pretty_breaks(),
        direction = 1,
        na.value  = "grey20",
        limits    = limits
      ) +
      geom_sf(data = ufs, fill = NA, color = "grey20", linewidth = 0.35) +
      coord_sf(datum = NA) +
      theme_minimal() +
      theme(legend.position = "bottom")
  }

  # ── build panel & save ─────────────────────────────────────────────────
  maps  <- lapply(years_main, plot_single)

  panel <- ggarrange(
    plotlist      = maps,
    labels        = as.character(years_main),
    common.legend = TRUE, legend = "bottom",
    ncol          = ncol, nrow = nrow
  )

  ggsave(filename = filename, plot = panel,
         height = height, width = width, dpi = dpi)

  invisible(panel)
}


## ──────────────────────────────────────────────────────────────

# Function for the relevance of the instrument: first-stage regression and F-statistics

## ──────────────────────────────────────────────────────────────

plot_and_save_first_stage <- function(
  df,
  years_main,
  Z,
  D,
  filename,
  height = 2.25, width = 2.5, dpi = 1000) {

  Z <- rlang::ensym(Z)
  D <- rlang::ensym(D)

  # ── derive panel filenames ─────────────────────────────────────────────
  filename_A <- paste0(filename, "A.jpeg")
  filename_B <- paste0(filename, "B.jpeg")
  filename_C <- paste0(filename, "C.jpeg")

  # ── Panel A: Correlation ───────────────────────────────────────────────
  f_2A <- df %>%
    dplyr::filter(CE_TYPE != "A") %>%
    ggplot(aes(x = !!Z, y = !!D)) +
    geom_jitter(alpha = .4, width = .5, height = .5, size = 2, color = "grey60") +
    geom_abline(intercept = 0, slope = 1, color = "black",
                linetype = "dashed", linewidth = .2) +
    geom_smooth(method = lm, color = "black", se = FALSE, linewidth = .8) +
    labs(x = "Mandated Retirement", y = "First JPII Appointment") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 90, vjust = .5))

  ggsave(filename_A, f_2A, height = height, width = width, dpi = dpi)

  # ── First-stage estimates across all years ─────────────────────────────
  years_all <- 1979:max(df[[rlang::as_string(Z)]], na.rm = TRUE)

  first_stage <- lapply(years_all, function(i) {
    idx     <- df$CE_TYPE != "A"
    z_vals  <- df[[rlang::as_string(Z)]][idx]
    d_vals  <- df[[rlang::as_string(D)]][idx]
    I_years <- ifelse(z_vals < i, z_vals - 1978, i - 1978)
    Expos   <- ifelse(d_vals < i, d_vals - 1978, i - 1978)
    fit     <- estimatr::lm_robust(Expos ~ I_years)
    out     <- broom::tidy(fit)[2, c("estimate", "conf.low", "conf.high")]
    fstat   <- unname(fit$fstatistic[1])
    cbind(out, fstat = fstat, year = i)
  }) %>%
    dplyr::bind_rows() %>%
    dplyr::mutate(outcome_years = !(year %in% years_main))

  # ── Panel B: Main Estimate ─────────────────────────────────────────────
  f_2B <- ggplot(first_stage, aes(x = year, y = estimate, color = outcome_years)) +
    geom_point() +
    geom_errorbar(aes(ymin = conf.low, ymax = conf.high), width = 0) +
    scale_color_grey() +
    labs(x = "Year", y = "Estimate") +
    theme_minimal() +
    theme(legend.position = "none",
          axis.text.x = element_text(angle = 90, vjust = .5))

  ggsave(filename_B, f_2B, height = height, width = width, dpi = dpi)

  # ── Panel C: F-Statistic ───────────────────────────────────────────────
  f_2C <- ggplot(first_stage, aes(x = year, y = fstat)) +
    geom_line(color = "grey40") +
    geom_point(aes(color = outcome_years)) +
    scale_color_grey() +
    labs(x = "Year", y = "F-Statistic") +
    theme_minimal() +
    theme(legend.position = "none",
          axis.text.x = element_text(angle = 90, vjust = .5))

  ggsave(filename_C, f_2C, height = height, width = width, dpi = dpi)

  invisible(list(A = f_2A, B = f_2B, C = f_2C, first_stage = first_stage))
}


## ──────────────────────────────────────────────────────────────

# Function to estimate the ITT and 2SLS

## ──────────────────────────────────────────────────────────────

run_itt_2sls <- function(data,
                         y,
                         D,
                         Z,
                         fixed_effects,
                         clusters,
                         years,
                         election_var = "election",
                         label        = "PT vote ") {
  
  itt_list  <- list()
  cace_list <- list()
  
  for (i in years) {
    
    year_data <- data[data[[election_var]] == i, ]
    
    itt_list[[paste0(label, i)]] <- do.call(
      lm_robust,
      list(
        formula       = as.formula(paste(y, "~", Z)),
        fixed_effects = as.formula(paste("~", fixed_effects)),
        clusters      = as.name(clusters),
        data          = quote(year_data)
      )
    )
    
    cace_list[[paste0(label, i)]] <- do.call(
      iv_robust,
      list(
        formula       = as.formula(paste(y, "~", D, "|", Z)),
        fixed_effects = as.formula(paste("~", fixed_effects)),
        clusters      = as.name(clusters),
        data          = quote(year_data)
      )
    )
  }
  
  list(itt = itt_list, cace = cace_list)
}


## ──────────────────────────────────────────────────────────────

# Function to generate table of ITT and 2SLS

## ──────────────────────────────────────────────────────────────

make_itt_2sls_table <- function(itt_list,
                                cace_list,
                                years,
                                label      = "PT vote ",
                                D_var      = "Exposure",
                                D_label    = "Exposure",
                                Z_var      = "Retirement_Years",
                                Z_label    = "Mandated Exposure",
                                title      = "<b>Outcome: PT Presidential Vote Share</b>",
                                output_dir,
                                file_name) {

  yr_cols <- as.character(years)

  # ── Extract stats from ITT models ──────────────────────────────────────────
  meta <- tibble(
    col          = yr_cols,
    outcome_mean = sapply(years, \(y) mean(itt_list[[paste0(label, y)]]$fitted.values)),
    n_obs        = sapply(years, \(y) itt_list[[paste0(label, y)]]$nobs),
    n_cl         = sapply(years, \(y) itt_list[[paste0(label, y)]]$nclusters)
  )

  # ── Panel A — 2SLS ─────────────────────────────────────────────────────────
  panel_A <- modelsummary(
    setNames(lapply(years, \(y) cace_list[[paste0(label, y)]]), yr_cols),
    coef_map  = setNames(D_label, D_var),
    gof_omit  = ".*",
    estimate  = "{estimate}{stars}",
    statistic = "({std.error})",
    stars     = TRUE,
    output    = "data.frame"
  ) %>% select(-any_of(c("part", "statistic")))

  # ── Panel B — ITT ──────────────────────────────────────────────────────────
  panel_B <- modelsummary(
    setNames(lapply(years, \(y) itt_list[[paste0(label, y)]]), yr_cols),
    coef_map  = setNames(Z_label, Z_var),
    gof_omit  = ".*",
    estimate  = "{estimate}{stars}",
    statistic = "({std.error})",
    stars     = TRUE,
    output    = "data.frame"
  ) %>% select(-any_of(c("part", "statistic")))

  # Blank SE row labels
  panel_A$term[seq(2, nrow(panel_A), by = 2)] <- ""
  panel_B$term[seq(2, nrow(panel_B), by = 2)] <- ""

  # ── Helpers ────────────────────────────────────────────────────────────────
  make_row <- function(label, values) {
    tibble(term = label) %>%
      bind_cols(as_tibble(setNames(as.list(values), yr_cols)))
  }

  sep <- function(label) make_row(label, rep("", length(yr_cols)))

  # ── Bottom rows ────────────────────────────────────────────────────────────
  bottom_rows <- bind_rows(
    make_row("Outcome Mean",     formatC(meta$outcome_mean, format = "f", digits = 1)),
    make_row("Num. Obs.",        formatC(meta$n_obs, format = "d", big.mark = ",")),
    make_row("Num. of Clusters", as.character(meta$n_cl))
  )

  # ── Assemble ───────────────────────────────────────────────────────────────
  full_df <- bind_rows(
    sep("<b>Panel A: 2SLS</b>"),
    panel_A,
    sep("<b>Panel B: Reduced Form (ITT)</b>"),
    panel_B,
    bottom_rows
  )

  # ── Render ─────────────────────────────────────────────────────────────────
  html_path <- file.path(output_dir, paste0(file_name, ".html"))
  jpeg_path <- file.path(output_dir, paste0(file_name, ".jpeg"))

  datasummary_df(
    full_df,
    title            = title,
    escape           = FALSE,
    add_header_above = c(" " = 1, setNames(rep(1, length(yr_cols)), yr_cols)),
    output           = html_path
  )

  webshot2::webshot(
    url = html_path,
    file = jpeg_path,
    zoom = 2,
    vwidth = 900,
    vheight  = 420,
    cliprect = "viewport"
  )

  invisible(full_df)
}

## ──────────────────────────────────────────────────────────────

# Function to estimate the ITT of two variables: placebo treatment tests

## ──────────────────────────────────────────────────────────────

placebo_treatment_tables <- function(
    data,
    var_A,          # e.g. "bish_age"
    var_B,          # e.g. "experience"
    label_A,        # e.g. "Bishop Age"
    label_B,        # e.g. "Bishop Experience"
    panel_label_A,  # e.g. "Panel A: Bishop Age"
    panel_label_B,  # e.g. "Panel B: Bishop Experience"
    years,
    fixed_effects  = "UF",
    clusters       = "CE_1978",
    election_var   = "election",
    partido_val    = "PT",
    cargo_val      = "Presidente",
    ce_type_excl   = "A",
    title          = "<b>Outcome: PT Presidential Vote Share</b>",
    output_dir,
    file_name
) {

  # ── Helper ─────────────────────────────────────────────────────────────────
  blank_se_rows <- function(df) {
    df$term[seq(2, nrow(df), by = 2)] <- ""
    df
  }

  # ── Fit ITT models ──────────────────────────────────────────────────────────
  fit_itt <- function(var) {
    models <- list()
    for (i in years) {
      year_data <- data %>%
        filter(
          .data[[election_var]] == i,
          I_YEAR > i,
          partido == partido_val,
          cargo   == cargo_val,
          CE_TYPE != ce_type_excl
        )

      models[[paste0("PT vote ", i)]] <- do.call(
        lm_robust,
        list(
          formula       = as.formula(paste("vote.sh ~", var)),
          fixed_effects = as.formula(paste("~", fixed_effects)),
          clusters      = as.name(clusters),
          data          = quote(year_data)
        )
      )
    }
    models
  }

  models_A <- fit_itt(var_A)
  models_B <- fit_itt(var_B)

  cols <- as.character(years)

  # ── Extract panels via modelsummary ────────────────────────────────────────
  extract_panel <- function(models, var, label) {
    modelsummary(
      setNames(lapply(years, \(y) models[[paste0("PT vote ", y)]]), cols),
      coef_map  = setNames(label, var),
      gof_omit  = ".*",
      estimate  = "{estimate}{stars}",
      statistic = "({std.error})",
      stars     = TRUE,
      output    = "data.frame"
    ) %>%
      select(-any_of(c("part", "statistic"))) %>%
      blank_se_rows()
  }

  panel_A <- extract_panel(models_A, var_A, label_A)
  panel_B <- extract_panel(models_B, var_B, label_B)

  # ── Meta stats ─────────────────────────────────────────────────────────────
  meta <- tibble(
    col          = cols,
    outcome_mean = sapply(years, \(y) mean(models_A[[paste0("PT vote ", y)]]$fitted.values)),
    n_obs        = sapply(years, \(y) models_A[[paste0("PT vote ", y)]]$nobs),
    n_cl         = sapply(years, \(y) models_A[[paste0("PT vote ", y)]]$nclusters)
  )

  # ── Row helpers ────────────────────────────────────────────────────────────
  make_row <- function(label, values) {
    tibble(term = label) %>%
      bind_cols(as_tibble(setNames(as.list(values), cols)))
  }

  sep <- function(label) {
    make_row(paste0("<b>", label, "</b>"), rep("", length(cols)))
  }

  # ── Assemble ───────────────────────────────────────────────────────────────
  bottom_rows <- bind_rows(
    make_row("Outcome Mean",     sprintf("%.1f", meta$outcome_mean)),
    make_row("Num. Obs.",        format(meta$n_obs, big.mark = ",")),
    make_row("Num. of Clusters", as.character(meta$n_cl))
  )

  full_df <- bind_rows(
    sep(panel_label_A), panel_A,
    sep(panel_label_B), panel_B,
    bottom_rows
  )

  # ── Render & save ──────────────────────────────────────────────────────────
  html_path <- file.path(output_dir, paste0(file_name, ".html"))
  jpeg_path <- file.path(output_dir, paste0(file_name, ".jpeg"))

  datasummary_df(
    full_df,
    title            = title,
    escape           = FALSE,
    add_header_above = c(" " = 1, setNames(rep(1, length(cols)), cols)),
    output           = html_path
  )

  webshot2::webshot(
    url      = html_path,
    file     = jpeg_path,
    zoom     = 2,
    vwidth   = 900,
    vheight  = 420,
    cliprect = "viewport"
  )

  invisible(full_df)
}