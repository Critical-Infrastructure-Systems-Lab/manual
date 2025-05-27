---
layout: page
title: Data viz
description: >
  Resources and examples on how to visualize data.
hide_description: true
sitemap: false
permalink: /docs/data-viz
---

## Overview of Data Visualization Tools (R, Python, and Linux)

Data visualization is essential for exploratory analysis, model diagnostics, and communication of results. This section provides a quick overview of common visualization libraries used in scientific computing, organized by programming environment.

---

### Python

Python offers a wide range of libraries for both static and interactive plotting:

- **Matplotlib**: The foundational 2D plotting library for Python. Offers granular control and supports high-quality export for publication.
  - Website: <https://matplotlib.org>

- **Seaborn**: Built on top of Matplotlib, Seaborn simplifies statistical plotting with intuitive syntax and attractive defaults.
  - Website: <https://seaborn.pydata.org>

- **Plotly**: Enables interactive plots in the browser. Supports scatter plots, choropleths, 3D plots, and more.
  - Website: <https://plotly.com/python>

- **Altair**: A declarative library based on Vega-Lite. Best suited for tidy datasets and exploratory visualization.
  - Website: <https://altair-viz.github.io>

- **Bokeh**: Ideal for building interactive visualizations and dashboards. Integrates well with web applications.
  - Website: <https://bokeh.org>

- **PyVista / Mayavi**: Used for advanced 3D and volumetric visualizations, often in engineering and geoscience contexts.
  - Website: <https://pyvista.org>

---

### R

R is known for its expressive plotting ecosystem and is particularly well suited for statistical graphics:

- **ggplot2**: The most popular R visualization package. Based on the Grammar of Graphics and part of the tidyverse.
  - Website: <https://ggplot2.tidyverse.org>

- **lattice**: Offers multi-panel plots using a formula-based syntax. Preceded ggplot2 and still widely used in legacy workflows.
  - Website: <https://cran.r-project.org/web/packages/lattice/index.html>

- **plotly (R)**: Provides interactive visualizations in R. Can convert static `ggplot2` plots into interactive versions with minimal changes.
  - Website: <https://plotly.com>

- **shiny**: Enables the development of interactive web applications in R that can include dynamic plots and user inputs.
  - Website: <https://shiny.posit.co>

- **leaflet (R)**: For creating interactive maps with markers, polygons, and raster overlays.
  - Website: <https://rstudio.github.io/leaflet>

---

### Linux & Command-Line Tools

Command-line tools are efficient for automation and quick diagnostics, especially in headless or remote environments:

- **gnuplot**: A terminal-based plotting tool that supports 2D/3D plotting. Scriptable and highly customizable.
  - Website: <http://www.gnuplot.info>

- **Graphviz**: Visualizes graphs from `.dot` files. Excellent for network diagrams, flowcharts, and dependency trees.
  - Website: <https://graphviz.org>

- **ImageMagick**: Not a plotting tool per se, but widely used for converting, resizing, and compositing images (e.g., building figures programmatically).
  - Website: <https://imagemagick.org>

---



