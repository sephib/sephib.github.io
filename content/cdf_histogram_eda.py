#%%
msg = "hello"
print(msg)

#%%
import numpy as np
import matplotlib.pyplot as plt

# Generate a mixture of two normal distributions, but with
# very few data points.
np.random.seed(3)
mx1 = np.random.normal(loc=0, scale=1, size=20)
mx2 = np.random.normal(loc=2, scale=1, size=20)
mx = np.concatenate([mx1, mx2, [5], [-4]])  # one outlier

def ecdf(data):
    x, y = np.sort(data), np.arange(1, len(data)+1) / len(data)
    return x, y

fig = plt.figure(figsize=(8, 4))
ax_ecdf = fig.add_subplot(121)
ax_hist = fig.add_subplot(122)
ax_hist.set_title('histogram')

ax_hist.hist(mx)

x, y = ecdf(mx)
ax_ecdf.scatter(x, y)
ax_ecdf.set_title('ecdf')

# %%
# make plot ONLY with bokeh

def make_plot(title, hist, edges, x,  cdf):
    p = figure(title=title, tools='', background_fill_color="#fafafa")
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5)
    p.line(x, cdf, line_color="orange", line_width=2, alpha=0.7, legend_label="CDF")

    p.y_range.start = 0
    p.legend.location = "center_right"
    p.legend.background_fill_color = "#fefefe"
    p.xaxis.axis_label = 'x'
    p.yaxis.axis_label = 'Pr(x)'
    p.grid.grid_line_color="white"
    return p

#%%
# primary = hv.Curve((df.index, df.cdf), label='CDF').opts(width=400, show_grid=True, framewise=True)

secondary =(hv.Histogram((df.index, df["values_in_bin"].tolist()), )).opts(width=400, color='red', show_grid=True, framewise=True, hooks=[plot_secondary])
# primary
secondary

pd.cut(autompg.mpg, bins=30).map(lambda x: x.left)

out, bins  = pd.cut(autompg.mpg, bins=30, include_lowest=True, right=False, retbins=True)
out, bins

label = "Normal Distribution (μ=0, σ=0.5)"
mu, sigma = 0, 0.5

measured = np.random.normal(mu, sigma, 1000)
hist = np.histogram(measured, density=False, bins=50)
pd.DataFrame.from_records(hist).T