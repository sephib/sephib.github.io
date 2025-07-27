# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bokeh.plotting import figure

# %%
np.random.seed(3)
distribution_1 = np.random.normal(loc=0, scale=1, size=20)
distribution_2 = np.random.normal(loc=2, scale=1, size=20)
mixed_data = np.concatenate([distribution_1, distribution_2, [5], [-4]])


def empirical_cdf(data):
    """Calculate empirical cumulative distribution function."""
    sorted_data = np.sort(data)
    cumulative_prob = np.arange(1, len(data) + 1) / len(data)
    return sorted_data, cumulative_prob


fig, (ax_ecdf, ax_hist) = plt.subplots(1, 2, figsize=(12, 4))

ax_hist.hist(mixed_data)
ax_hist.set_title('Histogram')

x_values, y_values = empirical_cdf(mixed_data)
ax_ecdf.scatter(x_values, y_values)
ax_ecdf.set_title('Empirical CDF')

# %%


def create_bokeh_plot(title, histogram_data, bin_edges, x_data, cdf_data):
    """Create a bokeh plot with histogram and CDF overlay."""
    plot = figure(title=title, tools='', background_fill_color="#fafafa")
    
    plot.quad(
        top=histogram_data, 
        bottom=0, 
        left=bin_edges[:-1], 
        right=bin_edges[1:],
        fill_color="navy", 
        line_color="white", 
        alpha=0.5
    )
    
    plot.line(
        x_data, 
        cdf_data, 
        line_color="orange", 
        line_width=2, 
        alpha=0.7, 
        legend_label="CDF"
    )
    
    plot.y_range.start = 0
    plot.legend.location = "center_right"
    plot.legend.background_fill_color = "#fefefe"
    plot.xaxis.axis_label = 'x'
    plot.yaxis.axis_label = 'Pr(x)'
    plot.grid.grid_line_color = "white"
    
    return plot


# %%
NORMAL_DIST_LABEL = "Normal Distribution (μ=0, σ=0.5)"
MU, SIGMA = 0, 0.5

normal_samples = np.random.normal(MU, SIGMA, 1000)
histogram_data, bin_edges = np.histogram(normal_samples, density=False, bins=50)
histogram_df = pd.DataFrame({'histogram': histogram_data, 'bins': bin_edges[:-1]})